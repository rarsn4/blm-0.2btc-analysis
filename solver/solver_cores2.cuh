// solver_cores.cuh — verified device cores, merged. One change vs the
// standalone files: the PBKDF2 salt block now comes from __constant__ memory
// (d_saltHi/d_saltLo/d_saltBits) instead of being hardcoded, so passphrases are
// a runtime parameter and sweeping 50 of them needs zero recompiles.
//
// Everything else is byte-for-byte the code that passed its vectors:
//   sha512_compress   7 vectors, all padding boundaries
//   ripemd160_32b     3 vectors including hash160(G)
//   bip39_seed        5 vectors including the canonical BIP39 one
#pragma once
// ============================================================ SHA-256
// (moved here from solver.cu: solver2.cu no longer defines these before the
//  include, and sha256_1blk_h0 / hash160_pub below depend on them)

#define R32(x,n) __funnelshift_r((x),(x),(n))
#define B0(x) (R32(x,2)^R32(x,13)^R32(x,22))
#define B1(x) (R32(x,6)^R32(x,11)^R32(x,25))
#define S0(x) (R32(x,7)^R32(x,18)^((x)>>3))
#define S1(x) (R32(x,17)^R32(x,19)^((x)>>10))

__constant__ uint32_t d_K256[64] = {
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};

// SHA-256 over exactly 33 bytes (a compressed pubkey): one block, 0x80 at byte
// 33, bitlen 264. Verified against 3 hash160 vectors including hash160(G).
__device__ void sha256_33b(const uint8_t *in, uint32_t out[8]){
    uint32_t W[64];
#pragma unroll
    for(int i=0;i<8;++i)
        W[i]=((uint32_t)in[i*4]<<24)|((uint32_t)in[i*4+1]<<16)|((uint32_t)in[i*4+2]<<8)|in[i*4+3];
    W[8]=((uint32_t)in[32]<<24)|0x00800000u;
#pragma unroll
    for(int i=9;i<15;++i) W[i]=0u;
    W[15]=264u;
#pragma unroll
    for(int i=16;i<64;++i) W[i]=S1(W[i-2])+W[i-7]+S0(W[i-15])+W[i-16];
    uint32_t a=0x6a09e667,b=0xbb67ae85,c=0x3c6ef372,d=0xa54ff53a;
    uint32_t e=0x510e527f,f=0x9b05688c,g=0x1f83d9ab,h=0x5be0cd19;
#pragma unroll
    for(int i=0;i<64;++i){
        uint32_t t1=h+B1(e)+((e&f)^(~e&g))+d_K256[i]+W[i];
        uint32_t t2=B0(a)+((a&b)^(a&c)^(b&c));
        h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;
    }
    out[0]=0x6a09e667+a;out[1]=0xbb67ae85+b;out[2]=0x3c6ef372+c;out[3]=0xa54ff53a+d;
    out[4]=0x510e527f+e;out[5]=0x9b05688c+f;out[6]=0x1f83d9ab+g;out[7]=0x5be0cd19+h;
}



// ============================================================ SHA-512

#define ROTR_LO(hi,lo,n) __funnelshift_r((lo),(hi),(n))
#define ROTR_HI(hi,lo,n) __funnelshift_r((hi),(lo),(n))
#define ROTRB_LO(hi,lo,n) __funnelshift_r((hi),(lo),(n)-32)
#define ROTRB_HI(hi,lo,n) __funnelshift_r((lo),(hi),(n)-32)

__device__ __forceinline__ void add64(uint32_t &rhi,uint32_t &rlo,
        uint32_t ahi,uint32_t alo,uint32_t bhi,uint32_t blo){
    asm volatile("add.cc.u32 %0,%2,%4;\n\t addc.u32 %1,%3,%5;"
        :"=r"(rlo),"=r"(rhi):"r"(alo),"r"(ahi),"r"(blo),"r"(bhi));
}
__device__ __forceinline__ void acc64(uint32_t &hi,uint32_t &lo,uint32_t bhi,uint32_t blo){
    asm volatile("add.cc.u32 %0,%0,%2;\n\t addc.u32 %1,%1,%3;"
        :"+r"(lo),"+r"(hi):"r"(blo),"r"(bhi));
}

#define BSIG0_LO(h,l) (ROTR_LO(h,l,28)^ROTRB_LO(h,l,34)^ROTRB_LO(h,l,39))
#define BSIG0_HI(h,l) (ROTR_HI(h,l,28)^ROTRB_HI(h,l,34)^ROTRB_HI(h,l,39))
#define BSIG1_LO(h,l) (ROTR_LO(h,l,14)^ROTR_LO(h,l,18)^ROTRB_LO(h,l,41))
#define BSIG1_HI(h,l) (ROTR_HI(h,l,14)^ROTR_HI(h,l,18)^ROTRB_HI(h,l,41))
#define SSIG0_LO(h,l) (ROTR_LO(h,l,1)^ROTR_LO(h,l,8)^__funnelshift_r((l),(h),7))
#define SSIG0_HI(h,l) (ROTR_HI(h,l,1)^ROTR_HI(h,l,8)^((h)>>7))
#define SSIG1_LO(h,l) (ROTR_LO(h,l,19)^ROTRB_LO(h,l,61)^__funnelshift_r((l),(h),6))
#define SSIG1_HI(h,l) (ROTR_HI(h,l,19)^ROTRB_HI(h,l,61)^((h)>>6))

__constant__ uint32_t d_Khi[80]={
0x428a2f98u,0x71374491u,0xb5c0fbcfu,0xe9b5dba5u,0x3956c25bu,0x59f111f1u,0x923f82a4u,0xab1c5ed5u,
0xd807aa98u,0x12835b01u,0x243185beu,0x550c7dc3u,0x72be5d74u,0x80deb1feu,0x9bdc06a7u,0xc19bf174u,
0xe49b69c1u,0xefbe4786u,0x0fc19dc6u,0x240ca1ccu,0x2de92c6fu,0x4a7484aau,0x5cb0a9dcu,0x76f988dau,
0x983e5152u,0xa831c66du,0xb00327c8u,0xbf597fc7u,0xc6e00bf3u,0xd5a79147u,0x06ca6351u,0x14292967u,
0x27b70a85u,0x2e1b2138u,0x4d2c6dfcu,0x53380d13u,0x650a7354u,0x766a0abbu,0x81c2c92eu,0x92722c85u,
0xa2bfe8a1u,0xa81a664bu,0xc24b8b70u,0xc76c51a3u,0xd192e819u,0xd6990624u,0xf40e3585u,0x106aa070u,
0x19a4c116u,0x1e376c08u,0x2748774cu,0x34b0bcb5u,0x391c0cb3u,0x4ed8aa4au,0x5b9cca4fu,0x682e6ff3u,
0x748f82eeu,0x78a5636fu,0x84c87814u,0x8cc70208u,0x90befffau,0xa4506cebu,0xbef9a3f7u,0xc67178f2u,
0xca273eceu,0xd186b8c7u,0xeada7dd6u,0xf57d4f7fu,0x06f067aau,0x0a637dc5u,0x113f9804u,0x1b710b35u,
0x28db77f5u,0x32caab7bu,0x3c9ebe0au,0x431d67c4u,0x4cc5d4beu,0x597f299cu,0x5fcb6fabu,0x6c44198cu};
__constant__ uint32_t d_Klo[80]={
0xd728ae22u,0x23ef65cdu,0xec4d3b2fu,0x8189dbbcu,0xf348b538u,0xb605d019u,0xaf194f9bu,0xda6d8118u,
0xa3030242u,0x45706fbeu,0x4ee4b28cu,0xd5ffb4e2u,0xf27b896fu,0x3b1696b1u,0x25c71235u,0xcf692694u,
0x9ef14ad2u,0x384f25e3u,0x8b8cd5b5u,0x77ac9c65u,0x592b0275u,0x6ea6e483u,0xbd41fbd4u,0x831153b5u,
0xee66dfabu,0x2db43210u,0x98fb213fu,0xbeef0ee4u,0x3da88fc2u,0x930aa725u,0xe003826fu,0x0a0e6e70u,
0x46d22ffcu,0x5c26c926u,0x5ac42aedu,0x9d95b3dfu,0x8baf63deu,0x3c77b2a8u,0x47edaee6u,0x1482353bu,
0x4cf10364u,0xbc423001u,0xd0f89791u,0x0654be30u,0xd6ef5218u,0x5565a910u,0x5771202au,0x32bbd1b8u,
0xb8d2d0c8u,0x5141ab53u,0xdf8eeb99u,0xe19b48a8u,0xc5c95a63u,0xe3418acbu,0x7763e373u,0xd6b2b8a3u,
0x5defb2fcu,0x43172f60u,0xa1f0ab72u,0x1a6439ecu,0x23631e28u,0xde82bde9u,0xb2c67915u,0xe372532bu,
0xea26619cu,0x21c0c207u,0xcde0eb1eu,0xee6ed178u,0x72176fbau,0xa2c898a6u,0xbef90daeu,0x131c471bu,
0x23047d84u,0x40c72493u,0x15c9bebcu,0x9c100d4cu,0xcb3e42b6u,0xfc657e2au,0x3ad6faecu,0x4a475817u};

__device__ void sha512_compress(uint32_t *shi,uint32_t *slo,
                                const uint32_t *bhi,const uint32_t *blo){
    uint32_t whi[16],wlo[16];
#pragma unroll
    for(int i=0;i<16;++i){whi[i]=bhi[i];wlo[i]=blo[i];}
    uint32_t ah=shi[0],al=slo[0],bh=shi[1],bl=slo[1],ch=shi[2],cl=slo[2],dh=shi[3],dl=slo[3];
    uint32_t eh=shi[4],el=slo[4],fh=shi[5],fl=slo[5],gh=shi[6],gl=slo[6],hh=shi[7],hl=slo[7];
    for(int i=0;i<80;++i){
        if(i>=16){
            uint32_t x2h=whi[(i-2)&15],x2l=wlo[(i-2)&15];
            uint32_t xfh=whi[(i-15)&15],xfl=wlo[(i-15)&15];
            acc64(whi[i&15],wlo[i&15],SSIG1_HI(x2h,x2l),SSIG1_LO(x2h,x2l));
            acc64(whi[i&15],wlo[i&15],whi[(i-7)&15],wlo[(i-7)&15]);
            acc64(whi[i&15],wlo[i&15],SSIG0_HI(xfh,xfl),SSIG0_LO(xfh,xfl));
        }
        uint32_t t1h,t1l,t2h,t2l;
        add64(t1h,t1l,hh,hl,BSIG1_HI(eh,el),BSIG1_LO(eh,el));
        acc64(t1h,t1l,(eh&fh)^(~eh&gh),(el&fl)^(~el&gl));
        acc64(t1h,t1l,d_Khi[i],d_Klo[i]);
        acc64(t1h,t1l,whi[i&15],wlo[i&15]);
        add64(t2h,t2l,BSIG0_HI(ah,al),BSIG0_LO(ah,al),
              (ah&bh)^(ah&ch)^(bh&ch),(al&bl)^(al&cl)^(bl&cl));
        hh=gh;hl=gl;gh=fh;gl=fl;fh=eh;fl=el;
        add64(eh,el,dh,dl,t1h,t1l);
        dh=ch;dl=cl;ch=bh;cl=bl;bh=ah;bl=al;
        add64(ah,al,t1h,t1l,t2h,t2l);
    }
    acc64(shi[0],slo[0],ah,al);acc64(shi[1],slo[1],bh,bl);
    acc64(shi[2],slo[2],ch,cl);acc64(shi[3],slo[3],dh,dl);
    acc64(shi[4],slo[4],eh,el);acc64(shi[5],slo[5],fh,fl);
    acc64(shi[6],slo[6],gh,gl);acc64(shi[7],slo[7],hh,hl);
}

__device__ __constant__ uint32_t IVHI[8]={0x6a09e667u,0xbb67ae85u,0x3c6ef372u,0xa54ff53au,
                                          0x510e527fu,0x9b05688cu,0x1f83d9abu,0x5be0cd19u};
__device__ __constant__ uint32_t IVLO[8]={0xf3bcc908u,0x84caa73bu,0xfe94f82bu,0x5f1d36f1u,
                                          0xade682d1u,0x2b3e6c1fu,0xfb41bd6bu,0x137e2179u};


// SHA-256 over a message of len <= 55 bytes (one block). Returns h0 only; the
// BIP39 checksum needs just its top bits. Replaces the 16-byte-only variant so
// 12/15/18/21/24-word phrases all work.
__device__ __forceinline__ uint32_t sha256_1blk_h0(const uint8_t *in, int len){
    uint32_t W[64];
#pragma unroll
    for(int i=0;i<16;++i) W[i]=0u;
    for(int i=0;i<len;++i) W[i>>2] |= ((uint32_t)in[i]) << (24 - 8*(i&3));
    W[len>>2] |= 0x80u << (24 - 8*(len&3));
    W[15] = (uint32_t)(len*8);
#pragma unroll
    for(int i=16;i<64;++i) W[i]=S1(W[i-2])+W[i-7]+S0(W[i-15])+W[i-16];
    uint32_t a=0x6a09e667,b=0xbb67ae85,c=0x3c6ef372,d=0xa54ff53a;
    uint32_t e=0x510e527f,f=0x9b05688c,g=0x1f83d9ab,h=0x5be0cd19;
#pragma unroll
    for(int i=0;i<64;++i){
        uint32_t t1=h+B1(e)+((e&f)^(~e&g))+d_K256[i]+W[i];
        uint32_t t2=B0(a)+((a&b)^(a&c)^(b&c));
        h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;
    }
    return 0x6a09e667u+a;
}

// ============================================================ RIPEMD-160

__constant__ uint8_t d_RL[80]={
0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,
3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12, 1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,
4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13};
__constant__ uint8_t d_RR[80]={
5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12, 6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,
15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13, 8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,
12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11};
__constant__ uint8_t d_SL[80]={
11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8, 7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,
11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5, 11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,
9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6};
__constant__ uint8_t d_SR[80]={
8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6, 9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,
9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5, 15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,
8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11};
__constant__ uint32_t d_KL[5]={0x00000000,0x5A827999,0x6ED9EBA1,0x8F1BBCDC,0xA953FD4E};
__constant__ uint32_t d_KR[5]={0x50A28BE6,0x5C4DD124,0x6D703EF3,0x7A6D76E9,0x00000000};

#define ROL(x,n) __funnelshift_l((x),(x),(n))
__device__ __forceinline__ uint32_t rmdF(int j,uint32_t x,uint32_t y,uint32_t z){
    if(j<16) return x^y^z;
    if(j<32) return (x&y)|(~x&z);
    if(j<48) return (x|~y)^z;
    if(j<64) return (x&z)|(y&~z);
    return x^(y|~z);
}
// RIPEMD-160 is LITTLE-endian, unlike SHA-2: byte-swap in and out.
__device__ void ripemd160_32b(const uint32_t in_be[8],uint32_t out_be[5]){
    uint32_t X[16];
#pragma unroll
    for(int i=0;i<8;++i) X[i]=__byte_perm(in_be[i],0,0x0123);
    X[8]=0x00000080u;
#pragma unroll
    for(int i=9;i<14;++i) X[i]=0u;
    X[14]=256u; X[15]=0u;
    uint32_t h0=0x67452301,h1=0xEFCDAB89,h2=0x98BADCFE,h3=0x10325476,h4=0xC3D2E1F0;
    uint32_t a=h0,b=h1,c=h2,d=h3,e=h4,A=h0,B=h1,C=h2,D=h3,E=h4;
    for(int j=0;j<80;++j){
        uint32_t t=ROL(a+rmdF(j,b,c,d)+X[d_RL[j]]+d_KL[j>>4],d_SL[j])+e;
        a=e;e=d;d=ROL(c,10);c=b;b=t;
        t=ROL(A+rmdF(79-j,B,C,D)+X[d_RR[j]]+d_KR[j>>4],d_SR[j])+E;
        A=E;E=D;D=ROL(C,10);C=B;B=t;
    }
    uint32_t r[5]={h1+c+D,h2+d+E,h3+e+A,h4+a+B,h0+b+C};
#pragma unroll
    for(int i=0;i<5;++i) out_be[i]=__byte_perm(r[i],0,0x0123);
}

__device__ __forceinline__ void hash160_pub(const uint8_t pub[33], uint32_t out[5]){
    uint32_t sh[8]; sha256_33b(pub,sh); ripemd160_32b(sh,out);
}

// ============================================================ PBKDF2

// Salt block comes from constant memory — set per passphrase by the host.
__device__ void bip39_seed(const uint8_t *mn,uint32_t mlen,uint32_t *ohi,uint32_t *olo){
    uint32_t kb[128];
    if(mlen>128){
        // RFC 2104: key longer than the 128-byte block is replaced by its hash.
        // Every 24-word mnemonic hits this (min 135, mean 153, max 172 bytes).
        uint32_t khi[8],klo[8],bh[16],bl[16];
#pragma unroll
        for(int i=0;i<8;++i){khi[i]=IVHI[i];klo[i]=IVLO[i];}
        uint32_t off=0;
        while(off+128<=mlen){
            for(int i=0;i<16;++i){
                const uint8_t*p=mn+off+i*8;
                bh[i]=((uint32_t)p[0]<<24)|((uint32_t)p[1]<<16)|((uint32_t)p[2]<<8)|p[3];
                bl[i]=((uint32_t)p[4]<<24)|((uint32_t)p[5]<<16)|((uint32_t)p[6]<<8)|p[7];
            }
            sha512_compress(khi,klo,bh,bl); off+=128;
        }
        uint8_t tail[256];
        uint32_t rem=mlen-off;
        for(uint32_t i=0;i<256;++i) tail[i]=(i<rem)?mn[off+i]:0u;
        tail[rem]=0x80;
        int nblk=(rem>=112)?2:1;              // 16-byte length field must fit
        uint64_t bits=(uint64_t)mlen*8;
        for(int i=0;i<8;++i) tail[nblk*128-1-i]=(uint8_t)(bits>>(8*i));
        for(int b=0;b<nblk;++b){
            for(int i=0;i<16;++i){
                const uint8_t*p=tail+b*128+i*8;
                bh[i]=((uint32_t)p[0]<<24)|((uint32_t)p[1]<<16)|((uint32_t)p[2]<<8)|p[3];
                bl[i]=((uint32_t)p[4]<<24)|((uint32_t)p[5]<<16)|((uint32_t)p[6]<<8)|p[7];
            }
            sha512_compress(khi,klo,bh,bl);
        }
        for(int i=0;i<128;++i) kb[i]=0u;
#pragma unroll
        for(int i=0;i<8;++i){
            kb[i*8+0]=(khi[i]>>24)&0xFF; kb[i*8+1]=(khi[i]>>16)&0xFF;
            kb[i*8+2]=(khi[i]>>8)&0xFF;  kb[i*8+3]=khi[i]&0xFF;
            kb[i*8+4]=(klo[i]>>24)&0xFF; kb[i*8+5]=(klo[i]>>16)&0xFF;
            kb[i*8+6]=(klo[i]>>8)&0xFF;  kb[i*8+7]=klo[i]&0xFF;
        }
    } else {
        for(int i=0;i<128;++i) kb[i]=(i<(int)mlen)?mn[i]:0u;
    }

    uint32_t ipa_hi[8],ipa_lo[8],opa_hi[8],opa_lo[8],bhi[16],blo[16];
#pragma unroll
    for(int i=0;i<8;++i){ipa_hi[i]=IVHI[i];ipa_lo[i]=IVLO[i];
                         opa_hi[i]=IVHI[i];opa_lo[i]=IVLO[i];}
    for(int i=0;i<16;++i){
        bhi[i]=((kb[i*8+0]^0x36)<<24)|((kb[i*8+1]^0x36)<<16)|((kb[i*8+2]^0x36)<<8)|(kb[i*8+3]^0x36);
        blo[i]=((kb[i*8+4]^0x36)<<24)|((kb[i*8+5]^0x36)<<16)|((kb[i*8+6]^0x36)<<8)|(kb[i*8+7]^0x36);
    }
    sha512_compress(ipa_hi,ipa_lo,bhi,blo);
    for(int i=0;i<16;++i){
        bhi[i]=((kb[i*8+0]^0x5c)<<24)|((kb[i*8+1]^0x5c)<<16)|((kb[i*8+2]^0x5c)<<8)|(kb[i*8+3]^0x5c);
        blo[i]=((kb[i*8+4]^0x5c)<<24)|((kb[i*8+5]^0x5c)<<16)|((kb[i*8+6]^0x5c)<<8)|(kb[i*8+7]^0x5c);
    }
    sha512_compress(opa_hi,opa_lo,bhi,blo);

    // U1: inner block is the host-built salt block (salt || INT(1) || pad || len)
    uint32_t shi[8],slo[8];
#pragma unroll
    for(int i=0;i<8;++i){shi[i]=ipa_hi[i];slo[i]=ipa_lo[i];}
#pragma unroll
    for(int i=0;i<16;++i){bhi[i]=d_saltHi[i];blo[i]=d_saltLo[i];}
    blo[15]=d_saltBits;
    sha512_compress(shi,slo,bhi,blo);

#pragma unroll
    for(int i=0;i<8;++i){bhi[i]=shi[i];blo[i]=slo[i];}
    bhi[8]=0x80000000u;blo[8]=0u;
#pragma unroll
    for(int i=9;i<15;++i){bhi[i]=0u;blo[i]=0u;}
    bhi[15]=0u;blo[15]=1536u;
#pragma unroll
    for(int i=0;i<8;++i){shi[i]=opa_hi[i];slo[i]=opa_lo[i];}
    sha512_compress(shi,slo,bhi,blo);

    uint32_t uhi[8],ulo[8],thi[8],tlo[8];
#pragma unroll
    for(int i=0;i<8;++i){uhi[i]=shi[i];ulo[i]=slo[i];thi[i]=shi[i];tlo[i]=slo[i];}

    for(int it=1;it<2048;++it){
#pragma unroll
        for(int i=0;i<8;++i){bhi[i]=uhi[i];blo[i]=ulo[i];}
        bhi[8]=0x80000000u;blo[8]=0u;
#pragma unroll
        for(int i=9;i<15;++i){bhi[i]=0u;blo[i]=0u;}
        bhi[15]=0u;blo[15]=1536u;
#pragma unroll
        for(int i=0;i<8;++i){shi[i]=ipa_hi[i];slo[i]=ipa_lo[i];}
        sha512_compress(shi,slo,bhi,blo);
#pragma unroll
        for(int i=0;i<8;++i){bhi[i]=shi[i];blo[i]=slo[i];}
        bhi[8]=0x80000000u;blo[8]=0u;
#pragma unroll
        for(int i=9;i<15;++i){bhi[i]=0u;blo[i]=0u;}
        bhi[15]=0u;blo[15]=1536u;
#pragma unroll
        for(int i=0;i<8;++i){shi[i]=opa_hi[i];slo[i]=opa_lo[i];}
        sha512_compress(shi,slo,bhi,blo);
#pragma unroll
        for(int i=0;i<8;++i){uhi[i]=shi[i];ulo[i]=slo[i];thi[i]^=shi[i];tlo[i]^=slo[i];}
    }
#pragma unroll
    for(int i=0;i<8;++i){ohi[i]=thi[i];olo[i]=tlo[i];}
}

// ============================================================ BIP32

// HMAC-SHA512 with an arbitrary key <= 128 bytes. General form: no midstate
// reuse, because the chaincode key changes at every derivation level.
__device__ void hmac_sha512(const uint8_t *key,uint32_t klen,
                            const uint8_t *msg,uint32_t mlen,uint8_t out[64]){
    uint32_t kb[128];
    for(int i=0;i<128;++i) kb[i]=(i<(int)klen)?key[i]:0u;
    uint32_t shi[8],slo[8],bhi[16],blo[16];

    // inner
#pragma unroll
    for(int i=0;i<8;++i){shi[i]=IVHI[i];slo[i]=IVLO[i];}
    for(int i=0;i<16;++i){
        bhi[i]=((kb[i*8+0]^0x36)<<24)|((kb[i*8+1]^0x36)<<16)|((kb[i*8+2]^0x36)<<8)|(kb[i*8+3]^0x36);
        blo[i]=((kb[i*8+4]^0x36)<<24)|((kb[i*8+5]^0x36)<<16)|((kb[i*8+6]^0x36)<<8)|(kb[i*8+7]^0x36);
    }
    sha512_compress(shi,slo,bhi,blo);

    // message is always < 112 bytes here (max 37), so one padded block
    uint8_t blk[128];
    for(uint32_t i=0;i<128;++i) blk[i]=(i<mlen)?msg[i]:0u;
    blk[mlen]=0x80;
    uint64_t bits=(uint64_t)(128+mlen)*8;
    for(int i=0;i<8;++i) blk[127-i]=(uint8_t)(bits>>(8*i));
    for(int i=0;i<16;++i){
        bhi[i]=((uint32_t)blk[i*8]<<24)|((uint32_t)blk[i*8+1]<<16)|((uint32_t)blk[i*8+2]<<8)|blk[i*8+3];
        blo[i]=((uint32_t)blk[i*8+4]<<24)|((uint32_t)blk[i*8+5]<<16)|((uint32_t)blk[i*8+6]<<8)|blk[i*8+7];
    }
    sha512_compress(shi,slo,bhi,blo);

    uint32_t ihi[8],ilo[8];
#pragma unroll
    for(int i=0;i<8;++i){ihi[i]=shi[i];ilo[i]=slo[i];}

    // outer
#pragma unroll
    for(int i=0;i<8;++i){shi[i]=IVHI[i];slo[i]=IVLO[i];}
    for(int i=0;i<16;++i){
        bhi[i]=((kb[i*8+0]^0x5c)<<24)|((kb[i*8+1]^0x5c)<<16)|((kb[i*8+2]^0x5c)<<8)|(kb[i*8+3]^0x5c);
        blo[i]=((kb[i*8+4]^0x5c)<<24)|((kb[i*8+5]^0x5c)<<16)|((kb[i*8+6]^0x5c)<<8)|(kb[i*8+7]^0x5c);
    }
    sha512_compress(shi,slo,bhi,blo);
#pragma unroll
    for(int i=0;i<8;++i){bhi[i]=ihi[i];blo[i]=ilo[i];}
    bhi[8]=0x80000000u;blo[8]=0u;
#pragma unroll
    for(int i=9;i<15;++i){bhi[i]=0u;blo[i]=0u;}
    bhi[15]=0u;blo[15]=1536u;
    sha512_compress(shi,slo,bhi,blo);

#pragma unroll
    for(int i=0;i<8;++i){
        out[i*8+0]=(uint8_t)(shi[i]>>24);out[i*8+1]=(uint8_t)(shi[i]>>16);
        out[i*8+2]=(uint8_t)(shi[i]>>8); out[i*8+3]=(uint8_t)(shi[i]);
        out[i*8+4]=(uint8_t)(slo[i]>>24);out[i*8+5]=(uint8_t)(slo[i]>>16);
        out[i*8+6]=(uint8_t)(slo[i]>>8); out[i*8+7]=(uint8_t)(slo[i]);
    }
}

__constant__ uint32_t d_N[8]={0xFFFFFFFFu,0xFFFFFFFFu,0xFFFFFFFFu,0xFFFFFFFEu,
                              0xBAAEDCE6u,0xAF48A03Bu,0xBFD25E8Cu,0xD0364141u};

__device__ void addmod_n(uint32_t *r,const uint32_t *a,const uint32_t *b){
    uint32_t carry=0;
    for(int i=7;i>=0;--i){
        uint64_t s=(uint64_t)a[i]+b[i]+carry;
        r[i]=(uint32_t)s; carry=(uint32_t)(s>>32);
    }
    uint32_t t[8],borrow=0;
    for(int i=7;i>=0;--i){
        uint64_t s=(uint64_t)r[i]-d_N[i]-borrow;
        t[i]=(uint32_t)s; borrow=(s>>63)?1u:0u;
    }
    if(carry||!borrow){ for(int i=0;i<8;++i) r[i]=t[i]; }
}

// m/44'/0'/0'/0/0. HMAC key at the master step is the ASCII "Bitcoin seed";
// the MESSAGE is the 64-byte seed. Swapping those is the classic BIP32 bug and
// yields a perfectly valid-looking wrong master key.
// Derive one configured path and return its hash160. Paths live in
// __constant__ memory so they are a runtime config option, not a compile-time
// assumption. The master HMAC is recomputed per path, which is cheap: it is one
// HMAC against PBKDF2's 4096 SHA-512 compressions, so N paths cost roughly
// 1 + 0.1*N, not N.
__constant__ uint32_t d_path[8][6];
__constant__ uint8_t  d_pathLen[8];
__constant__ int      d_nPath;

__device__ void derive_multi(const uint8_t seed[64],int p,uint32_t h160[5]){
    const uint8_t BSEED[12]={'B','i','t','c','o','i','n',' ','s','e','e','d'};
    uint8_t I[64];
    hmac_sha512(BSEED,12,seed,64,I);
    uint32_t k[8];
#pragma unroll
    for(int i=0;i<8;++i)
        k[i]=((uint32_t)I[i*4]<<24)|((uint32_t)I[i*4+1]<<16)|((uint32_t)I[i*4+2]<<8)|I[i*4+3];
    uint8_t cc[32];
    for(int i=0;i<32;++i) cc[i]=I[32+i];

    int L=d_pathLen[p];
    for(int lvl=0;lvl<L;++lvl){
        uint32_t idx=d_path[p][lvl];
        uint8_t data[37];
        if(idx&0x80000000u){
            data[0]=0x00;
#pragma unroll
            for(int i=0;i<8;++i){
                data[1+i*4+0]=(uint8_t)(k[i]>>24); data[1+i*4+1]=(uint8_t)(k[i]>>16);
                data[1+i*4+2]=(uint8_t)(k[i]>>8);  data[1+i*4+3]=(uint8_t)(k[i]);
            }
        } else {
            uint8_t pub[33];
            secp256k1_pub_from_priv(k,pub);
            for(int i=0;i<33;++i) data[i]=pub[i];
        }
        data[33]=(uint8_t)(idx>>24); data[34]=(uint8_t)(idx>>16);
        data[35]=(uint8_t)(idx>>8);  data[36]=(uint8_t)(idx);
        hmac_sha512(cc,32,data,37,I);
        uint32_t il[8];
#pragma unroll
        for(int i=0;i<8;++i)
            il[i]=((uint32_t)I[i*4]<<24)|((uint32_t)I[i*4+1]<<16)|((uint32_t)I[i*4+2]<<8)|I[i*4+3];
        addmod_n(k,il,k);
        for(int i=0;i<32;++i) cc[i]=I[32+i];
    }
    uint8_t pub[33];
    secp256k1_pub_from_priv(k,pub);
    hash160_pub(pub,h160);
}

__device__ void derive_bip44_h160(const uint8_t seed[64],uint32_t h160[5]){
    // single-path form kept for the selftest; multipath below
    uint32_t out[5]; derive_multi(seed,0,out);
#pragma unroll
    for(int i=0;i<5;++i) h160[i]=out[i];
}

// ---------------------------------------------------------------- Electrum
// HMAC-SHA512 with a MULTI-BLOCK message. The existing hmac_sha512() pads into
// a single block, valid only for mlen <= 119 -- fine for the 37-byte BIP32
// data it is called with, but 16% of 18-word and 100% of 21/24-word mnemonics
// exceed that. Using it for Electrum would silently corrupt the hash.
__device__ void hmac_sha512_long(const uint8_t *key,uint32_t klen,
                                 const uint8_t *msg,uint32_t mlen,uint8_t out[64]){
    uint32_t kb[128];
    for(int i=0;i<128;++i) kb[i]=(i<(int)klen)?key[i]:0u;
    uint32_t shi[8],slo[8],bh[16],bl[16];
#pragma unroll
    for(int i=0;i<8;++i){shi[i]=IVHI[i];slo[i]=IVLO[i];}
    for(int i=0;i<16;++i){
        bh[i]=((kb[i*8+0]^0x36)<<24)|((kb[i*8+1]^0x36)<<16)|((kb[i*8+2]^0x36)<<8)|(kb[i*8+3]^0x36);
        bl[i]=((kb[i*8+4]^0x36)<<24)|((kb[i*8+5]^0x36)<<16)|((kb[i*8+6]^0x36)<<8)|(kb[i*8+7]^0x36);
    }
    sha512_compress(shi,slo,bh,bl);

    uint32_t off=0;
    while(off+128<=mlen){
        for(int i=0;i<16;++i){
            const uint8_t*p=msg+off+i*8;
            bh[i]=((uint32_t)p[0]<<24)|((uint32_t)p[1]<<16)|((uint32_t)p[2]<<8)|p[3];
            bl[i]=((uint32_t)p[4]<<24)|((uint32_t)p[5]<<16)|((uint32_t)p[6]<<8)|p[7];
        }
        sha512_compress(shi,slo,bh,bl); off+=128;
    }
    uint8_t tail[256];
    uint32_t rem=mlen-off;
    for(uint32_t i=0;i<256;++i) tail[i]=(i<rem)?msg[off+i]:0u;
    tail[rem]=0x80;
    int nblk=(rem>=112)?2:1;
    uint64_t bits=(uint64_t)(128+mlen)*8;
    for(int i=0;i<8;++i) tail[nblk*128-1-i]=(uint8_t)(bits>>(8*i));
    for(int b=0;b<nblk;++b){
        for(int i=0;i<16;++i){
            const uint8_t*p=tail+b*128+i*8;
            bh[i]=((uint32_t)p[0]<<24)|((uint32_t)p[1]<<16)|((uint32_t)p[2]<<8)|p[3];
            bl[i]=((uint32_t)p[4]<<24)|((uint32_t)p[5]<<16)|((uint32_t)p[6]<<8)|p[7];
        }
        sha512_compress(shi,slo,bh,bl);
    }
    uint32_t ihi[8],ilo[8];
#pragma unroll
    for(int i=0;i<8;++i){ihi[i]=shi[i];ilo[i]=slo[i];}
#pragma unroll
    for(int i=0;i<8;++i){shi[i]=IVHI[i];slo[i]=IVLO[i];}
    for(int i=0;i<16;++i){
        bh[i]=((kb[i*8+0]^0x5c)<<24)|((kb[i*8+1]^0x5c)<<16)|((kb[i*8+2]^0x5c)<<8)|(kb[i*8+3]^0x5c);
        bl[i]=((kb[i*8+4]^0x5c)<<24)|((kb[i*8+5]^0x5c)<<16)|((kb[i*8+6]^0x5c)<<8)|(kb[i*8+7]^0x5c);
    }
    sha512_compress(shi,slo,bh,bl);
#pragma unroll
    for(int i=0;i<8;++i){bh[i]=ihi[i];bl[i]=ilo[i];}
    bh[8]=0x80000000u;bl[8]=0u;
#pragma unroll
    for(int i=9;i<15;++i){bh[i]=0u;bl[i]=0u;}
    bh[15]=0u;bl[15]=1536u;
    sha512_compress(shi,slo,bh,bl);
#pragma unroll
    for(int i=0;i<8;++i){
        out[i*8+0]=(uint8_t)(shi[i]>>24);out[i*8+1]=(uint8_t)(shi[i]>>16);
        out[i*8+2]=(uint8_t)(shi[i]>>8); out[i*8+3]=(uint8_t)(shi[i]);
        out[i*8+4]=(uint8_t)(slo[i]>>24);out[i*8+5]=(uint8_t)(slo[i]>>16);
        out[i*8+6]=(uint8_t)(slo[i]>>8); out[i*8+7]=(uint8_t)(slo[i]);
    }
}
