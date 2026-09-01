// solver2.cu — template-mode BIP39 solver. Supersedes solver.cu.
//
//   Build: nvcc -O3 -arch=sm_89 -I CUDACyclone-main -Xptxas -v solver2.cu -o solver2
//   Run  : ./solver2 --selftest
//          ./solver2 --config t18.conf [--passphrases pw.txt] [--resume N]
//
// WHAT CHANGED FROM solver.cu
//  1. TEMPLATE not permutation. Each slot is an independent mixed-radix digit.
//     Permutation mode could not represent this problem at all: it forbids a
//     word repeating, but two template gaps may legitimately hold the same word.
//  2. VARIABLE LENGTH 12/15/18/21/24. Checksum is words/3 bits, entropy is
//     words*4/3 bytes. 24 words means 1/256 survive, not 1/16.
//  3. HMAC KEY PRE-HASHING. RFC 2104: a key longer than the 128-byte block is
//     replaced by SHA512(key). EVERY 24-word mnemonic exceeds 128 bytes
//     (measured min 135, mean 153, max 172 over 2000 random phrases). Without
//     this, 24-word mode derives plausible garbage with no error anywhere.
//
//  4. BRAINWALLET MODE (SCHEME brainwallet). priv = SHA256(phrase) directly:
//     no checksum, no PBKDF2, no BIP32, no path. Because there is no checksum
//     EVERY candidate reaches the EC stage, so nothing filters a broken
//     pipeline -- a wrong SHA-256 would report "exhausted, no match" exactly
//     like a correct run. --selftest-brain is therefore mandatory, not optional.
//  5. EXTRA WORDS. Brainwallet phrases need not be BIP39. The wordlist tables
//     extend past 2048 so a config can name arbitrary words (EXTRA key). This
//     is required even for the canonical control: "battery" and "staple" are
//     not in the BIP39 list.
//
// Everything else is the code that already passed exact vectors:
//   SHA-512 (7 vectors) / RIPEMD-160 (3) / PBKDF2 (5) / secp256k1 (6, Cyclone).

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <string>
#include <vector>
#include <algorithm>
#include <cuda_runtime.h>
#include "cyclone_adapter.cuh"

#define MAXSLOT 24
#define MAXLIST 64
#define MAXPOOL 128
#define NWORDS  4096      // 2048 BIP39 + up to 2048 EXTRA (brainwallet only)
#define CHARBUF 24576     // BIP39 is 11068 chars; the rest is EXTRA headroom
#define MAXPHRASE 255     // mn[] is 256; parse-time check keeps it true

enum { M_LIT=0, M_LIST=1, M_POOL=2, M_FULL=3 };

__constant__ int      d_slots, d_ckbits, d_entbytes, d_npool;
__constant__ int      d_electrum;   // 0 = BIP39, 1 = Electrum v2
// ---- brainwallet mode. Each is a bitmask of variants to try per candidate.
__constant__ int      d_brain;      // 0 = mnemonic scheme, 1 = brainwallet
__constant__ int      d_brainKD;    // bit0 SHA256          bit1 double-SHA256
__constant__ int      d_brainSp;    // bit0 joined w/ space bit1 joined w/o
__constant__ int      d_brainPub;   // bit0 compressed      bit1 uncompressed
__constant__ uint8_t  d_mode[MAXSLOT];
__constant__ uint16_t d_lit[MAXSLOT];
__constant__ uint16_t d_list[MAXSLOT][MAXLIST];
__constant__ uint8_t  d_listn[MAXSLOT];
__constant__ uint16_t d_pool[MAXPOOL];
__constant__ uint32_t d_radix[MAXSLOT];
__constant__ uint32_t d_saltHi[16], d_saltLo[16], d_saltBits;
__constant__ uint32_t d_target[5];

// full BIP39 wordlist lives in global memory (16 KB of chars would crowd
// constant memory once the tables above are in place)
__device__ char     g_chars[CHARBUF];
__device__ uint16_t g_off[NWORDS];
__device__ uint8_t  g_len[NWORDS];

#include "solver_cores2.cuh"    // SHA-512/256, RIPEMD-160, PBKDF2(+prehash), BIP32

// ---------------------------------------------------------------- template

// Global index -> one BIP39 index per slot. Mixed radix, least-significant slot
// last. Stateless, so shards and resumes from a single uint64.
__device__ __forceinline__ void decode_template(uint64_t gi, uint16_t *bip){
    for (int i = d_slots - 1; i >= 0; --i) {
        uint32_t n = d_radix[i];
        uint32_t c = 0;
        if (n > 1) { c = (uint32_t)(gi % n); gi /= n; }
        switch (d_mode[i]) {
            case M_LIT:  bip[i] = d_lit[i];        break;
            case M_LIST: bip[i] = d_list[i][c];    break;
            case M_POOL: bip[i] = d_pool[c];       break;
            default:     bip[i] = (uint16_t)c;     break;   // M_FULL
        }
    }
}

// words*11 bits = entropy + checksum. checksum = top d_ckbits of SHA256(entropy)
__device__ __forceinline__ bool checksum_ok(const uint16_t *bip){
    uint8_t ent[32];
    uint32_t acc = 0; int nb = 0, o = 0;
    for (int i = 0; i < d_slots; ++i) {
        acc = (acc << 11) | bip[i];
        nb += 11;
        while (nb >= 8 && o < d_entbytes) { nb -= 8; ent[o++] = (uint8_t)(acc >> nb); }
    }
    uint32_t want = acc & ((1u << d_ckbits) - 1u);
    uint32_t h0 = sha256_1blk_h0(ent, d_entbytes);
    return want == (h0 >> (32 - d_ckbits));
}


// Build the phrase from resolved word indices. sep=1 inserts single spaces
// (BIP39/Electrum require it); sep=0 concatenates, which some brainwallet
// tools did and which is therefore a variant worth sweeping.
__device__ __forceinline__ uint32_t build_phrase(const uint16_t *bip, uint8_t *mn, int sep){
    uint32_t ml=0;
    for (int i = 0; i < d_slots; ++i) {
        uint16_t w=bip[i]; uint16_t off=g_off[w]; uint8_t L=g_len[w];
        for (int j = 0; j < L; ++j) mn[ml++] = (uint8_t)g_chars[off+j];
        if (sep && i < d_slots-1) mn[ml++] = ' ';
    }
    return ml;
}
__device__ __forceinline__ uint32_t build_mnemonic(const uint16_t *bip, uint8_t *mn){
    return build_phrase(bip, mn, 1);
}

// Electrum v2 validity: HMAC-SHA512("Seed version", mnemonic) hex prefix.
//   "01..."  standard wallet      "100..." segwit wallet
// Both accepted: the target is a legacy 1-address, which points at standard,
// but a segwit-seeded wallet can still expose legacy addresses at other paths.
// NOTE: there is NO BIP39 checksum here, so phrase length is unconstrained.
__device__ __forceinline__ bool electrum_ok(const uint16_t *bip){
    uint8_t mn[256];
    uint32_t ml = build_mnemonic(bip, mn);
    const uint8_t SV[12]={'S','e','e','d',' ','v','e','r','s','i','o','n'};
    uint8_t I[64];
    hmac_sha512_long(SV,12,mn,ml,I);
    return I[0]==0x01 || (I[0]==0x10 && (I[1]>>4)==0);
}

__global__ void k_filter(uint64_t base, uint64_t count,
                         uint64_t *__restrict__ out, uint32_t *__restrict__ n,
                         uint32_t cap){
    uint64_t t = blockIdx.x*(uint64_t)blockDim.x + threadIdx.x;
    if (t >= count) return;
    uint64_t gi = base + t;
    uint16_t bip[MAXSLOT];
    decode_template(gi, bip);
    // A brainwallet has no checksum: every candidate must reach the EC stage.
    // Acceptance is 1.0, which is why the host caps CHUNK at CAP in this mode.
    if (!d_brain && !(d_electrum ? electrum_ok(bip) : checksum_ok(bip))) return;

    uint32_t mask = __activemask();
    uint32_t leader = __ffs(mask) - 1;
    uint32_t lane = threadIdx.x & 31;
    uint32_t rk = __popc(mask & ((1u << lane) - 1));
    uint32_t s = 0;
    if (lane == leader) s = atomicAdd(n, __popc(mask));
    s = __shfl_sync(mask, s, leader) + rk;
    if (s < cap) out[s] = gi;
}

__global__ void k_derive(const uint64_t *__restrict__ gis, uint32_t count,
                         uint64_t *__restrict__ hit){
    uint32_t t = blockIdx.x*blockDim.x + threadIdx.x;
    if (t >= count) return;
    uint16_t bip[MAXSLOT];
    decode_template(gis[t], bip);

    uint8_t mn[256];
    uint32_t h[5];

    // ------------------------------------------------------------ brainwallet
    // priv = SHA256(phrase). No seed, no CKDpriv, no path. hit[1] records
    // which variant matched, because unlike a BIP32 path the host cannot
    // re-derive it without repeating the EC work.
    if (d_brain) {
        for (int sp = 0; sp < 2; ++sp) {
            if (!(d_brainSp & (1<<sp))) continue;
            uint32_t pl = build_phrase(bip, mn, sp==0 ? 1 : 0);
            for (int kd = 0; kd < 2; ++kd) {
                if (!(d_brainKD & (1<<kd))) continue;
                uint8_t priv[32];
                sha256_long(mn, pl, priv);
                if (kd == 1) { uint8_t tmp[32];
                    for(int i=0;i<32;++i) tmp[i]=priv[i];
                    sha256_long(tmp, 32, priv); }
                uint32_t k[8];
#pragma unroll
                for (int i = 0; i < 8; ++i)
                    k[i]=((uint32_t)priv[i*4]<<24)|((uint32_t)priv[i*4+1]<<16)
                        |((uint32_t)priv[i*4+2]<<8)|priv[i*4+3];
                uint64_t X[4], Y[4];
                secp256k1_xy_from_priv(k, X, Y);       // the one expensive step
                for (int pc = 0; pc < 2; ++pc) {
                    if (!(d_brainPub & (1<<pc))) continue;
                    if (pc == 0) { uint8_t pub[33]; point_to_compressed(X,Y,pub);
                                   hash160_pub(pub,h); }
                    else         { uint8_t pub[65]; point_to_uncompressed(X,Y,pub);
                                   hash160_pub65(pub,h); }
                    if (h[0]==d_target[0]&&h[1]==d_target[1]&&h[2]==d_target[2]
                        &&h[3]==d_target[3]&&h[4]==d_target[4]) {
                        uint64_t var = (uint64_t)((sp<<2)|(kd<<1)|pc);
                        if (atomicCAS((unsigned long long*)&hit[0],
                                      0xFFFFFFFFFFFFFFFFULL,
                                      (unsigned long long)gis[t])
                            == 0xFFFFFFFFFFFFFFFFULL) hit[1] = var;
                        return;
                    }
                }
            }
        }
        return;
    }

    // ------------------------------------------------------- BIP39 / Electrum
    uint32_t ml = build_phrase(bip, mn, 1);
    uint32_t shi[8], slo[8];
    bip39_seed(mn, ml, shi, slo);
    uint8_t seed[64];
#pragma unroll
    for (int i = 0; i < 8; ++i) {
        seed[i*8+0]=(uint8_t)(shi[i]>>24); seed[i*8+1]=(uint8_t)(shi[i]>>16);
        seed[i*8+2]=(uint8_t)(shi[i]>>8);  seed[i*8+3]=(uint8_t)(shi[i]);
        seed[i*8+4]=(uint8_t)(slo[i]>>24); seed[i*8+5]=(uint8_t)(slo[i]>>16);
        seed[i*8+6]=(uint8_t)(slo[i]>>8);  seed[i*8+7]=(uint8_t)(slo[i]);
    }
    for (int p = 0; p < d_nPath; ++p) {
        derive_multi(seed, p, h);
        if (h[0]==d_target[0]&&h[1]==d_target[1]&&h[2]==d_target[2]
            &&h[3]==d_target[3]&&h[4]==d_target[4]) {
            // hit[1] = the PATH INDEX. show_hit used to print m/44'/0'/0'/0/0
            // unconditionally, which is wrong for every config with >1 PATH.
            if (atomicCAS((unsigned long long*)&hit[0],
                          0xFFFFFFFFFFFFFFFFULL,
                          (unsigned long long)gis[t])
                == 0xFFFFFFFFFFFFFFFFULL) hit[1] = (uint64_t)p;
            return;
        }
    }
}

#include "solver_host2.cuh"
