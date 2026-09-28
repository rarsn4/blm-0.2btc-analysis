#!/usr/bin/env python3
"""Hash all three SEC1 public-key encodings and compare each to the target.
Every replacement is asserted: a missing anchor aborts, it does not no-op."""
import sys

EDITS = []
def ed(f, old, new, n=1): EDITS.append((f, old, new, n))

# ---------------------------------------------------------------- A. hybrid
ed('cyclone_adapter.cuh',
"""__device__ __forceinline__ void secp256k1_xy_from_priv(const uint32_t priv[8],""",
"""// SEC1 2.3.3 hybrid form: 65 bytes carrying X and Y exactly as the
// uncompressed form does, but with the y parity also folded into the lead byte
// (0x06 even, 0x07 odd). Built by overwriting the prefix that
// point_to_uncompressed just wrote, so the limb order is the one that routine
// was already verified to produce rather than a second transcription of it.
__device__ __forceinline__ void point_to_hybrid(const uint64_t X[4],
                                                const uint64_t Y[4],
                                                uint8_t pub[65]) {
#if LIMBS_ARE_BE
    const uint64_t y_ls = Y[3];
#else
    const uint64_t y_ls = Y[0];
#endif
    point_to_uncompressed(X, Y, pub);
    pub[0] = (uint8_t)(0x06u | (uint32_t)(y_ls & 1ULL));
}

__device__ __forceinline__ void secp256k1_xy_from_priv(const uint32_t priv[8],""")

# ------------------------------------------------- B. split derive_multi
ed('solver_cores2.cuh',
"__device__ void derive_multi(const uint8_t seed[64],int p,uint32_t h160[5]){",
"__device__ void derive_multi_key(const uint8_t seed[64],int p,uint32_t k[8]){")

ed('solver_cores2.cuh',
"    hmac_sha512(BSEED,12,seed,64,I);\n    uint32_t k[8];\n",
"    hmac_sha512(BSEED,12,seed,64,I);\n")

ed('solver_cores2.cuh',
"""    uint8_t pub[33];
    secp256k1_pub_from_priv(k,pub);
    hash160_pub(pub,h160);
}""",
"""}

__device__ void derive_multi(const uint8_t seed[64],int p,uint32_t h160[5]){
    uint32_t k[8]; derive_multi_key(seed,p,k);
    uint8_t pub[33];
    secp256k1_pub_from_priv(k,pub);
    hash160_pub(pub,h160);
}

// All three SEC1 encodings of the same leaf public key, each hashed:
//   h3[0] compressed   33 B  0x02 / 0x03
//   h3[1] uncompressed 65 B  0x04
//   h3[2] hybrid       65 B  0x06 / 0x07
// One EC multiply feeds all three -- y is already in hand for the parity byte
// -- so the added cost is two SHA-256 + RIPEMD-160 against PBKDF2's 4096
// SHA-512 compressions. This is unconditional on purpose: making it a config
// option means the next kernel variant silently drops back to compressed-only.
__device__ void derive_multi3(const uint8_t seed[64],int p,uint32_t h3[3][5]){
    uint32_t k[8]; derive_multi_key(seed,p,k);
    uint64_t X[4],Y[4];
    secp256k1_xy_from_priv(k,X,Y);
    uint8_t c[33]; point_to_compressed(X,Y,c);   hash160_pub(c,h3[0]);
    uint8_t u[65]; point_to_uncompressed(X,Y,u); hash160_pub65(u,h3[1]);
    uint8_t y[65]; point_to_hybrid(X,Y,y);       hash160_pub65(y,h3[2]);
}""")

# ------------------------------------------------- C. BIP39 compare loop
ed('solver2.cu',
"""    for (int p = 0; p < d_nPath; ++p) {
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
    }""",
"""    for (int p = 0; p < d_nPath; ++p) {
        uint32_t h3[3][5];
        derive_multi3(seed, p, h3);
        for (int e = 0; e < 3; ++e) {
            if (h3[e][0]==d_target[0]&&h3[e][1]==d_target[1]&&h3[e][2]==d_target[2]
                &&h3[e][3]==d_target[3]&&h3[e][4]==d_target[4]) {
                // hit[1] = path index << 2 | encoding. It used to be the bare
                // path index; show_hit before that printed m/44'/0'/0'/0/0
                // unconditionally, wrong for every config with >1 PATH.
                if (atomicCAS((unsigned long long*)&hit[0],
                              0xFFFFFFFFFFFFFFFFULL,
                              (unsigned long long)gis[t])
                    == 0xFFFFFFFFFFFFFFFFULL) hit[1] = ((uint64_t)p<<2)|(uint64_t)e;
                return;
            }
        }
    }""")

# ------------------------------------------- D. brainwallet: add hybrid
ed('solver2.cu',
"""                for (int pc = 0; pc < 2; ++pc) {
                    if (!(d_brainPub & (1<<pc))) continue;
                    if (pc == 0) { uint8_t pub[33]; point_to_compressed(X,Y,pub);
                                   hash160_pub(pub,h); }
                    else         { uint8_t pub[65]; point_to_uncompressed(X,Y,pub);
                                   hash160_pub65(pub,h); }""",
"""                for (int pc = 0; pc < 3; ++pc) {
                    if (!(d_brainPub & (1<<pc))) continue;
                    if      (pc == 0) { uint8_t pub[33]; point_to_compressed(X,Y,pub);
                                        hash160_pub(pub,h); }
                    else if (pc == 1) { uint8_t pub[65]; point_to_uncompressed(X,Y,pub);
                                        hash160_pub65(pub,h); }
                    else              { uint8_t pub[65]; point_to_hybrid(X,Y,pub);
                                        hash160_pub65(pub,h); }""")

ed('solver2.cu',
"                        uint64_t var = (uint64_t)((sp<<2)|(kd<<1)|pc);",
"                        // pc now needs two bits, so sp and kd shift up one.\n"
"                        uint64_t var = (uint64_t)((sp<<3)|(kd<<2)|pc);")

# --------------------------------------------------------- E. host side
ed('solver_host2.cuh',
"    int  brainPub=3;               // bit0 compressed, bit1 uncompressed",
"    int  brainPub=7;               // bit0 compressed, bit1 uncompressed, bit2 hybrid")

ed('solver_host2.cuh',
'static const char* BRAIN_PUB[2]={"compressed","uncompressed"};',
'static const char* BRAIN_PUB[3]={"compressed","uncompressed","hybrid"};')

ed('solver_host2.cuh',
"""static bool parse_cfg(const char*path,Cfg&cf){""",
"""// Same, over three names. BRAINPUB needs it; the two-name form stays for the
// other keys rather than churning them.
static int parse_bits3(const char*key,const char*a0,const char*a1,const char*a2,int&mask){
    mask=0; char*t;
    while((t=strtok(NULL," \\t\\r\\n"))){
        if(!strcmp(t,a0)) mask|=1;
        else if(!strcmp(t,a1)) mask|=2;
        else if(!strcmp(t,a2)) mask|=4;
        else if(!strcmp(t,"all")||!strcmp(t,"both")) mask|=7;
        else { fprintf(stderr,"%s: expected %s|%s|%s|all, got '%s'\\n",key,a0,a1,a2,t); return 0; }
    }
    if(!mask){ fprintf(stderr,"%s: no value\\n",key); return 0; }
    return 1;
}

static bool parse_cfg(const char*path,Cfg&cf){""")

ed('solver_host2.cuh',
'        else if(key=="BRAINPUB"){ if(!parse_bits("BRAINPUB","compressed","uncompressed",cf.brainPub)){fclose(f);return false;} have_pub=true; }',
'        else if(key=="BRAINPUB"){ if(!parse_bits3("BRAINPUB","compressed","uncompressed","hybrid",cf.brainPub)){fclose(f);return false;} have_pub=true; }')

ed('solver_host2.cuh',
'        printf("\\n  pubkey   : "); for(int i=0;i<2;++i) if(cf.brainPub&(1<<i)) printf("%s ",BRAIN_PUB[i]);',
'        printf("\\n  pubkey   : "); for(int i=0;i<3;++i) if(cf.brainPub&(1<<i)) printf("%s ",BRAIN_PUB[i]);')

ed('solver_host2.cuh',
"        int sp=(int)((info>>2)&1), kd=(int)((info>>1)&1), pb=(int)(info&1);",
"        int sp=(int)((info>>3)&1), kd=(int)((info>>2)&1), pb=(int)(info&3);")

ed('solver_host2.cuh',
"""        printf("path       : %s\\n",
               info<cf.paths.size()?cf.paths[(size_t)info].c_str():"(unknown)");""",
"""        uint64_t pi=info>>2; int enc=(int)(info&3);
        printf("path       : %s\\n",
               pi<cf.paths.size()?cf.paths[(size_t)pi].c_str():"(unknown)");
        printf("pubkey     : %s\\n",enc<3?BRAIN_PUB[enc]:"(unknown)");""")

# ------------------------------------------------------------------ apply
fail=[]
for f, old, new, n in EDITS:
    s=open(f).read()
    c=s.count(old)
    if c!=n: fail.append((f,c,n,old.splitlines()[0][:70]))
if fail:
    print("ABORTED -- anchors not found as expected:")
    for f,c,n,o in fail: print(f"  {f}: found {c}, expected {n}  ::  {o}")
    sys.exit(1)
for f, old, new, n in EDITS:
    s=open(f).read(); open(f,'w').write(s.replace(old,new))
print(f"applied {len(EDITS)} edits across {len(set(e[0] for e in EDITS))} files")
