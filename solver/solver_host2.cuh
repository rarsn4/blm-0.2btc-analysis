// solver_host2.cuh — host driver for solver2.cu (template mode).
#pragma once
#define CK(x) do{ cudaError_t e_=(x); if(e_!=cudaSuccess){ \
    fprintf(stderr,"CUDA %s @%d: %s\n",#x,__LINE__,cudaGetErrorString(e_)); exit(1);} }while(0)

// WL holds the 2048 BIP39 words at indices 0..2047, then any EXTRA words a
// brainwallet config declares. Indices past 2047 are unreachable from BIP39 and
// Electrum configs -- widx() refuses them unless allow_extra is set -- so the
// checksum path can never see a word it cannot encode in 11 bits.
static std::vector<std::string> WL;
static size_t N_BIP39 = 0;

static bool load_wl(const char*p){
    FILE*f=fopen(p,"r"); if(!f) return false;
    char b[64];
    while(fgets(b,sizeof b,f)){ std::string w(b);
        while(!w.empty()&&(w.back()=='\n'||w.back()=='\r'||w.back()==' ')) w.pop_back();
        if(!w.empty()) WL.push_back(w); }
    fclose(f); N_BIP39=WL.size(); return WL.size()==2048;
}
static int widx(const std::string&w,bool allow_extra=false){
    size_t lim = allow_extra ? WL.size() : N_BIP39;
    for(size_t i=0;i<lim;++i) if(WL[i]==w) return (int)i;
    return -1;
}
// Register an arbitrary (non-BIP39) word, returning its index. Idempotent.
static int add_extra(const std::string&w){
    int i=widx(w,true); if(i>=0) return i;
    if(WL.size()>=NWORDS){ fprintf(stderr,"more than %d words\n",NWORDS); return -1; }
    WL.push_back(w); return (int)WL.size()-1;
}
static void upload_wl(){
    static char ch[CHARBUF]; static uint16_t off[NWORDS]; static uint8_t len[NWORDS];
    memset(ch,0,sizeof ch); memset(off,0,sizeof off); memset(len,0,sizeof len);
    int o=0;
    for(size_t i=0;i<WL.size();++i){
        if(o+(int)WL[i].size()>CHARBUF){ fprintf(stderr,"word char buffer full\n"); exit(1); }
        off[i]=(uint16_t)o; len[i]=(uint8_t)WL[i].size();
        memcpy(ch+o,WL[i].c_str(),len[i]); o+=len[i]; }
    CK(cudaMemcpyToSymbol(g_chars,ch,sizeof ch));
    CK(cudaMemcpyToSymbol(g_off,off,sizeof off));
    CK(cudaMemcpyToSymbol(g_len,len,sizeof len));
}
static bool b58_h160(const char*s,uint8_t out20[20]){
    static const char*A="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
    uint8_t buf[64]={0}; int n=0;
    for(const char*p=s;*p;++p){ const char*q=strchr(A,*p); if(!q) return false;
        int c=(int)(q-A);
        for(int i=0;i<n;++i){ c+=buf[i]*58; buf[i]=(uint8_t)(c&0xFF); c>>=8; }
        while(c){ if(n>=64) return false; buf[n++]=(uint8_t)(c&0xFF); c>>=8; } }
    for(const char*p=s;*p==A[0];++p){ if(n>=64) return false; buf[n++]=0; }
    if(n<25) return false;
    uint8_t full[64]; for(int i=0;i<n;++i) full[i]=buf[n-1-i];
    memcpy(out20,full+1,20); return true;
}

struct Slot { int mode; int lit; std::vector<int> list; };
struct Cfg {
    int words=0; std::string target,h160;
    std::vector<Slot> slots; std::vector<int> pool;
    std::vector<std::string> paths;
    uint64_t total=1;
    bool electrum=false;
    bool brain=false;              // SCHEME brainwallet
    int  brainKD=1;                // bit0 SHA256, bit1 double-SHA256
    int  brainSp=1;                // bit0 space-joined, bit1 concatenated
    int  brainPub=3;               // bit0 compressed, bit1 uncompressed
};
static const char* BRAIN_KD[2]={"sha256","double-sha256"};
static const char* BRAIN_SP[2]={"space-joined","concatenated"};
static const char* BRAIN_PUB[2]={"compressed","uncompressed"};

// Parse tokens like "sha256 dsha256" into a bitmask over names[2].
static int parse_bits(const char*key,const char*a0,const char*a1,int&mask){
    mask=0; char*t;
    while((t=strtok(NULL," \t\r\n"))){
        if(!strcmp(t,a0)) mask|=1;
        else if(!strcmp(t,a1)) mask|=2;
        else if(!strcmp(t,"both")) mask|=3;
        else { fprintf(stderr,"%s: expected %s|%s|both, got '%s'\n",key,a0,a1,t); return 0; }
    }
    if(!mask){ fprintf(stderr,"%s: no value\n",key); return 0; }
    return 1;
}

static bool parse_cfg(const char*path,Cfg&cf){
    FILE*f=fopen(path,"r"); if(!f){fprintf(stderr,"cannot open %s\n",path); return false;}
    char line[2048];
    // SLOT / POOL / EXTRA are all resolved AFTER the file is read, because
    // SCHEME and EXTRA may appear anywhere in it and both change which words
    // are legal. Resolving POOL inline (as this used to) meant an EXTRA word
    // in a POOL line was rejected purely because of line order.
    std::vector<std::pair<int,std::string>> raw;
    std::vector<std::string> raw_pool, raw_extra;
    bool have_kd=false, have_sp=false, have_pub=false;
    while(fgets(line,sizeof line,f)){
        char*p=line; while(*p==' '||*p=='\t')++p;
        if(*p=='#'||*p=='\n'||*p=='\r'||!*p) continue;
        char*k=strtok(p," \t\r\n"); if(!k) continue;
        std::string key(k);
        if(key=="WORDS"){ cf.words=atoi(strtok(NULL," \t\r\n")); }
        else if(key=="TARGET"){ cf.target=strtok(NULL," \t\r\n"); }
        else if(key=="HASH160"){ cf.h160=strtok(NULL," \t\r\n"); }
        else if(key=="SCHEME"){ char*v=strtok(NULL," \t\r\n");
            if(v){ cf.electrum = (strcmp(v,"electrum")==0);
                   cf.brain    = (strcmp(v,"brainwallet")==0);
                   if(!cf.electrum && !cf.brain && strcmp(v,"bip39")){
                       fprintf(stderr,"SCHEME must be bip39|electrum|brainwallet (got '%s')\n",v);
                       fclose(f); return false; } } }
        else if(key=="BRAINHASH"){ if(!parse_bits("BRAINHASH","sha256","dsha256",cf.brainKD)){fclose(f);return false;} have_kd=true; }
        else if(key=="BRAINSPACE"){ if(!parse_bits("BRAINSPACE","yes","no",cf.brainSp)){fclose(f);return false;} have_sp=true; }
        else if(key=="BRAINPUB"){ if(!parse_bits("BRAINPUB","compressed","uncompressed",cf.brainPub)){fclose(f);return false;} have_pub=true; }
        else if(key=="EXTRA"){ char*t; while((t=strtok(NULL," \t\r\n"))) raw_extra.push_back(t); }
        else if(key=="POOL"){ char*t; while((t=strtok(NULL," \t\r\n"))) raw_pool.push_back(t); }
        else if(key=="PATH"){ char*v=strtok(NULL," \t\r\n");
            if(v) cf.paths.push_back(std::string(v)); }
        else if(key=="SLOT"){ int n=atoi(strtok(NULL," \t\r\n"));
            char*v=strtok(NULL," \t\r\n"); if(!v){fprintf(stderr,"SLOT %d has no value\n",n); fclose(f); return false;}
            raw.push_back({n,std::string(v)}); }
        else fprintf(stderr,"warning: unknown key '%s'\n",key.c_str());
    }
    fclose(f);
    (void)have_kd; (void)have_sp; (void)have_pub;

    if(cf.brain && cf.electrum){ fprintf(stderr,"SCHEME cannot be both\n"); return false; }
    if(!cf.brain && !raw_extra.empty()){
        fprintf(stderr,"EXTRA words require SCHEME brainwallet -- a non-BIP39 word\n"
                       "cannot be encoded in the 11 bits the checksum needs.\n"); return false; }
    if(!cf.brain && (have_kd||have_sp||have_pub)){
        fprintf(stderr,"BRAINHASH/BRAINSPACE/BRAINPUB require SCHEME brainwallet\n"); return false; }
    if(cf.brain && !cf.paths.empty())
        fprintf(stderr,"warning: PATH ignored -- a brainwallet has no derivation path\n");

    for(auto&w:raw_extra){ if(add_extra(w)<0) return false; }

    if(!cf.electrum && !cf.brain && cf.words!=12&&cf.words!=15&&cf.words!=18&&cf.words!=21&&cf.words!=24){
        fprintf(stderr,"WORDS must be 12/15/18/21/24 for BIP39 (got %d)\n",cf.words); return false; }
    if(cf.electrum && (cf.words<3||cf.words>MAXSLOT)){
        fprintf(stderr,"WORDS must be 3..%d for electrum (got %d)\n",MAXSLOT,cf.words); return false; }
    if(cf.brain && (cf.words<1||cf.words>MAXSLOT)){
        fprintf(stderr,"WORDS must be 1..%d for brainwallet (got %d)\n",MAXSLOT,cf.words); return false; }

    for(auto&t:raw_pool){
        int i=widx(t,cf.brain);
        if(i<0){fprintf(stderr,"POOL '%s' not %s\n",t.c_str(),cf.brain?"a known word (add it with EXTRA)":"BIP39"); return false;}
        bool dup=false; for(int q:cf.pool) if(q==i) dup=true;
        if(!dup) cf.pool.push_back(i);
    }

    cf.slots.assign(cf.words,Slot{M_LIT,-1,{}});
    std::vector<bool> seen(cf.words,false);
    for(auto&pr:raw){
        int n=pr.first-1;
        if(n<0||n>=cf.words){ fprintf(stderr,"SLOT %d out of range\n",pr.first); return false; }
        seen[n]=true;
        std::string v=pr.second;
        if(v=="@POOL"){ cf.slots[n].mode=M_POOL; }
        else if(v=="@FULL"){ cf.slots[n].mode=M_FULL; }
        else if(v.find('|')!=std::string::npos){
            cf.slots[n].mode=M_LIST; size_t s2=0;
            while(s2<=v.size()){ size_t e=v.find('|',s2); if(e==std::string::npos) e=v.size();
                std::string w=v.substr(s2,e-s2);
                int i=widx(w,cf.brain); if(i<0){fprintf(stderr,"'%s' not %s\n",w.c_str(),cf.brain?"a known word (add it with EXTRA)":"BIP39"); return false;}
                cf.slots[n].list.push_back(i); s2=e+1; }
            if(cf.slots[n].list.size()>MAXLIST){fprintf(stderr,"slot %d list too long\n",pr.first); return false;}
        } else {
            int i=widx(v,cf.brain); if(i<0){fprintf(stderr,"'%s' not %s\n",v.c_str(),cf.brain?"a known word (add it with EXTRA)":"BIP39"); return false;}
            cf.slots[n].mode=M_LIT; cf.slots[n].lit=i;
        }
    }
    for(int i=0;i<cf.words;++i) if(!seen[i]){ fprintf(stderr,"SLOT %d missing\n",i+1); return false; }
    if(cf.pool.size()>MAXPOOL){fprintf(stderr,"POOL too big\n"); return false;}

    // mn[] on the device is 256 bytes. EXTRA words have no 8-char BIP39 bound,
    // so the worst-case phrase length is checked here rather than assumed.
    size_t worst=0;
    for(int i=0;i<cf.words;++i){
        size_t m=0;
        if(cf.slots[i].mode==M_LIT) m=WL[cf.slots[i].lit].size();
        else if(cf.slots[i].mode==M_LIST){ for(int q:cf.slots[i].list) m=std::max(m,WL[q].size()); }
        else if(cf.slots[i].mode==M_POOL){ for(int q:cf.pool)          m=std::max(m,WL[q].size()); }
        else { for(size_t q=0;q<N_BIP39;++q) m=std::max(m,WL[q].size()); }
        worst+=m+1;
    }
    if(worst>MAXPHRASE){
        fprintf(stderr,"worst-case phrase %zu bytes exceeds %d\n",worst,MAXPHRASE); return false; }
    return true;
}

// "m/44'/0'/0'/0/0" -> {0x8000002C,0x80000000,0x80000000,0,0}
static bool parse_path(const std::string&s,uint32_t out[6],int&n){
    n=0; size_t i=0;
    if(s.size()<1||(s[0]!='m'&&s[0]!='M')) return false;
    i=1;
    while(i<s.size()){
        if(s[i]!='/') return false;
        ++i; uint64_t v=0; bool any=false;
        while(i<s.size()&&s[i]>='0'&&s[i]<='9'){ v=v*10+(s[i]-'0'); ++i; any=true; }
        if(!any) return false;
        if(i<s.size()&&(s[i]=='\''||s[i]=='h'||s[i]=='H')){ v+=0x80000000ULL; ++i; }
        if(n>=6) return false;
        out[n++]=(uint32_t)v;
    }
    return n>0;
}
static void upload_paths(Cfg&cf){
    if(cf.brain){                 // no seed, no CKDpriv, nothing to derive
        int np=0; CK(cudaMemcpyToSymbol(d_nPath,&np,sizeof(int)));
        printf("paths          : (none -- brainwallet)\n");
        return;
    }
    if(cf.paths.empty()) cf.paths.push_back("m/44'/0'/0'/0/0");
    if(cf.paths.size()>8){ fprintf(stderr,"max 8 PATH lines\n"); exit(1); }
    uint32_t P[8][6]={{0}}; uint8_t L[8]={0};
    for(size_t i=0;i<cf.paths.size();++i){
        int n=0;
        if(!parse_path(cf.paths[i],P[i],n)){ fprintf(stderr,"bad PATH '%s'\n",cf.paths[i].c_str()); exit(1); }
        L[i]=(uint8_t)n;
    }
    int np=(int)cf.paths.size();
    CK(cudaMemcpyToSymbol(d_path,P,sizeof P));
    CK(cudaMemcpyToSymbol(d_pathLen,L,sizeof L));
    CK(cudaMemcpyToSymbol(d_nPath,&np,sizeof(int)));
    printf("paths          : ");
    for(auto&s:cf.paths) printf("%s ",s.c_str());
    printf("\n");
}

static void upload_cfg(const Cfg&cf){
    uint8_t mode[MAXSLOT]={0}; uint16_t lit[MAXSLOT]={0};
    uint16_t list[MAXSLOT][MAXLIST]={{0}}; uint8_t listn[MAXSLOT]={0};
    uint32_t radix[MAXSLOT]={0};
    for(int i=0;i<cf.words;++i){
        mode[i]=(uint8_t)cf.slots[i].mode;
        lit[i]=(uint16_t)(cf.slots[i].lit<0?0:cf.slots[i].lit);
        listn[i]=(uint8_t)cf.slots[i].list.size();
        for(size_t j=0;j<cf.slots[i].list.size();++j) list[i][j]=(uint16_t)cf.slots[i].list[j];
        radix[i]= cf.slots[i].mode==M_LIT?1u
                : cf.slots[i].mode==M_LIST?(uint32_t)cf.slots[i].list.size()
                : cf.slots[i].mode==M_POOL?(uint32_t)cf.pool.size() : 2048u;
    }
    uint16_t pool[MAXPOOL]={0};
    for(size_t i=0;i<cf.pool.size();++i) pool[i]=(uint16_t)cf.pool[i];
    int np=(int)cf.pool.size();
    int ck=cf.words/3, eb=cf.words*4/3;
    CK(cudaMemcpyToSymbol(d_mode,mode,sizeof mode));
    CK(cudaMemcpyToSymbol(d_lit,lit,sizeof lit));
    CK(cudaMemcpyToSymbol(d_list,list,sizeof list));
    CK(cudaMemcpyToSymbol(d_listn,listn,sizeof listn));
    CK(cudaMemcpyToSymbol(d_pool,pool,sizeof pool));
    CK(cudaMemcpyToSymbol(d_radix,radix,sizeof radix));
    CK(cudaMemcpyToSymbol(d_slots,&cf.words,sizeof(int)));
    CK(cudaMemcpyToSymbol(d_ckbits,&ck,sizeof(int)));
    CK(cudaMemcpyToSymbol(d_entbytes,&eb,sizeof(int)));
    CK(cudaMemcpyToSymbol(d_npool,&np,sizeof(int)));
    int el=cf.electrum?1:0;
    CK(cudaMemcpyToSymbol(d_electrum,&el,sizeof(int)));
    int br=cf.brain?1:0;
    CK(cudaMemcpyToSymbol(d_brain,&br,sizeof(int)));
    CK(cudaMemcpyToSymbol(d_brainKD,&cf.brainKD,sizeof(int)));
    CK(cudaMemcpyToSymbol(d_brainSp,&cf.brainSp,sizeof(int)));
    CK(cudaMemcpyToSymbol(d_brainPub,&cf.brainPub,sizeof(int)));

    uint32_t tg[5]={0};
    if(!cf.h160.empty()){
        for(int i=0;i<5;++i){ uint32_t v=0;
            for(int j=0;j<8;++j){ char c=cf.h160[i*8+j];
                v=(v<<4)|(uint32_t)(c<='9'?c-'0':(c|32)-'a'+10); }
            tg[i]=v; }
    } else {
        uint8_t h[20];
        if(!b58_h160(cf.target.c_str(),h)){fprintf(stderr,"bad address\n"); exit(1);}
        for(int i=0;i<5;++i) tg[i]=((uint32_t)h[i*4]<<24)|((uint32_t)h[i*4+1]<<16)
                                  |((uint32_t)h[i*4+2]<<8)|h[i*4+3];
    }
    CK(cudaMemcpyToSymbol(d_target,tg,sizeof tg));
    printf("target hash160 : %08x%08x%08x%08x%08x\n",tg[0],tg[1],tg[2],tg[3],tg[4]);
}

static void upload_salt(const std::string&pass, bool electrum=false){
    std::string salt=(electrum?std::string("electrum"):std::string("mnemonic"))+pass;
    if(salt.size()+5>110){fprintf(stderr,"passphrase too long\n"); exit(1);}
    uint8_t blk[128]={0}; memcpy(blk,salt.c_str(),salt.size());
    size_t n=salt.size();
    blk[n+3]=1; blk[n+4]=0x80;                       // INT_BE(1) then pad
    uint32_t hi[16],lo[16];
    for(int i=0;i<16;++i){
        hi[i]=((uint32_t)blk[i*8]<<24)|((uint32_t)blk[i*8+1]<<16)|((uint32_t)blk[i*8+2]<<8)|blk[i*8+3];
        lo[i]=((uint32_t)blk[i*8+4]<<24)|((uint32_t)blk[i*8+5]<<16)|((uint32_t)blk[i*8+6]<<8)|blk[i*8+7];
    }
    hi[15]=0; lo[15]=0;
    uint32_t bits=(uint32_t)((128+n+4)*8);
    CK(cudaMemcpyToSymbol(d_saltHi,hi,sizeof hi));
    CK(cudaMemcpyToSymbol(d_saltLo,lo,sizeof lo));
    CK(cudaMemcpyToSymbol(d_saltBits,&bits,sizeof bits));
}

// info = hit[1]: the path index in BIP39/Electrum mode, or the packed
// brainwallet variant (sp<<2 | kd<<1 | pub) in brainwallet mode.
static void show_hit(const Cfg&cf,uint64_t gi,const std::string&pass,uint64_t info){
    std::vector<int> bip(cf.words);
    uint64_t g=gi;
    for(int i=cf.words-1;i>=0;--i){
        uint32_t n = cf.slots[i].mode==M_LIT?1u
                   : cf.slots[i].mode==M_LIST?(uint32_t)cf.slots[i].list.size()
                   : cf.slots[i].mode==M_POOL?(uint32_t)cf.pool.size():2048u;
        uint32_t c=0; if(n>1){ c=(uint32_t)(g%n); g/=n; }
        bip[i]= cf.slots[i].mode==M_LIT?cf.slots[i].lit
              : cf.slots[i].mode==M_LIST?cf.slots[i].list[c]
              : cf.slots[i].mode==M_POOL?cf.pool[c]:(int)c;
    }
    printf("\n======================================================================\n");
    printf("HIT   index %llu\n",(unsigned long long)gi);
    printf("phrase     : ");
    for(int i=0;i<cf.words;++i) printf("%s%s",WL[bip[i]].c_str(),i<cf.words-1?" ":"\n");
    if(cf.brain){
        int sp=(int)((info>>2)&1), kd=(int)((info>>1)&1), pb=(int)(info&1);
        printf("scheme     : brainwallet\n");
        printf("key        : %s of the %s phrase\n",BRAIN_KD[kd],BRAIN_SP[sp]);
        printf("pubkey     : %s\n",BRAIN_PUB[pb]);
        printf("passphrase : (n/a -- brainwallets take no passphrase)\n");
    } else {
        printf("passphrase : %s\n",pass.empty()?"(none)":pass.c_str());
        // Was hardcoded to m/44'/0'/0'/0/0, which misreported every hit under a
        // config with more than one PATH line. hit[1] carries the real index.
        printf("path       : %s\n",
               info<cf.paths.size()?cf.paths[(size_t)info].c_str():"(unknown)");
    }
    printf("======================================================================\n");
    printf("\nVerify OFFLINE, networking disabled. Do not paste this anywhere.\n");
}

// selftest: both canonical BIP39 vectors through the FULL merged pipeline.
static int selftest(){
    struct T{int w;const char*mn;const char*addr;};
    T ts[2]={
      {12,"abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
          "1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA"},
      {24,"abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art",
          "1KBdbBJRVYffWHWWZ1moECfdVBSEnDpLHi"}};
    int fail=0;
    uint64_t *d_hit,*d_gis;
    CK(cudaMalloc(&d_hit,16)); CK(cudaMalloc(&d_gis,8));
    for(int t=0;t<2;++t){
        Cfg cf; cf.words=ts[t].w; cf.target=ts[t].addr;
        cf.slots.assign(cf.words,Slot{M_LIT,-1,{}});
        std::string s(ts[t].mn); size_t p=0; int i=0;
        while(p<s.size()&&i<cf.words){ size_t e=s.find(' ',p); if(e==std::string::npos) e=s.size();
            cf.slots[i].lit=widx(s.substr(p,e-p)); cf.slots[i].mode=M_LIT; p=e+1; ++i; }
        upload_cfg(cf); upload_paths(cf); upload_salt("",cf.electrum);
        CK(cudaMemset(d_hit,0xFF,16)); CK(cudaMemset(d_gis,0,8));
        k_derive<<<1,1>>>(d_gis,1,d_hit);
        CK(cudaGetLastError()); CK(cudaDeviceSynchronize());
        uint64_t h; CK(cudaMemcpy(&h,d_hit,8,cudaMemcpyDeviceToHost));
        printf("  %2d-word canonical -> %s   %s\n",ts[t].w,ts[t].addr,h==0?"PASS":"*** FAIL ***");
        if(h!=0) fail=1;
    }
    cudaFree(d_hit); cudaFree(d_gis);
    printf("\n%s\n",fail?"*** SELFTEST FAILED -- do not run a sweep. ***"
                        :"SELFTEST PASS -- 12- and 24-word paths both verified.");
    return fail;
}

// ---------------------------------------------------------------- brainwallet
// MANDATORY before any brainwallet sweep. A brainwallet has no checksum, so
// every candidate passes the filter by construction: a wrong SHA-256 produces a
// full run of plausible garbage and reports "exhausted, no match" exactly like a
// correct run. Nothing else in the pipeline would notice.
//
// The canonical vector is only 28 bytes -- ONE SHA-256 block -- so it does not
// exercise the multi-block path that this mode actually needs at 18 and 24
// words. Cases 7-12 are chosen for their lengths:
//   124 bytes  ->  len%64 = 60, forcing the extra compression block (rem>=56)
//   128 bytes  ->  len%64 = 0,  the whole message consumed by the block loop
//   157 bytes  ->  three blocks, the realistic 24-word size
// The uncompressed cases additionally push a 65-byte message through
// sha256_long inside hash160_pub65.
static int selftest_brain(){
    struct T{const char*phrase;const char*addr;int kd;int sp;int pub;const char*why;};
    static const T ts[]={
      {"correct horse battery staple","1C7zdTfnkzmr13HfA2vNm5SJYRK6nEKyq8",0,0,0,"canonical, compressed"},
      {"correct horse battery staple","1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T",0,0,1,"canonical, uncompressed"},
      {"correct horse battery staple","1A95ZB1auLEAXVYorh9wrtzzHpduBUC3oC",1,0,0,"double-SHA256, compressed"},
      {"correct horse battery staple","1MBJcCMAGTjir6xQi3cFYxySCAdAaxUQsU",1,0,1,"double-SHA256, uncompressed"},
      {"correct horse battery staple","1aZamxMGppDGiZahCUoBqUGVRU94JBehf",0,1,0,"no spaces, compressed"},
      {"correct horse battery staple","1KqAv2r2iebeEhkoKonksJwwPczwBjLMXC",0,1,1,"no spaces, uncompressed"},
      {"mechanic verify candy business ozone tomorrow museum sheriff random argue unaware remove figure desk wolf bullet hurry nasty",
       "1H3JMSyEq2woEYLn9u1kG32HJjkQbVNwSw",0,0,0,"124 B, len%64=60 -> extra pad block"},
      {"mechanic verify candy business ozone tomorrow museum sheriff random argue unaware remove figure desk wolf bullet hurry nasty",
       "1Lc5bPdxAZzR5mm5S3swMmcxB83FtKgvLi",0,0,1,"124 B, uncompressed"},
      {"ritual daughter garment casino plastic tank grocery apple inflict electric student slender tribe blood behind bag marine message",
       "1DzFSoymTdd2eP5FFCeRG7y69nbbh18ZjW",0,0,0,"128 B, len%64=0 -> exact blocks"},
      {"ritual daughter garment casino plastic tank grocery apple inflict electric student slender tribe blood behind bag marine message",
       "1BTCdnvSFPL48HaTKqaev6Z2FSANo9Keq8",0,0,1,"128 B, uncompressed"},
      {"banner cricket leopard dinner alone task junior before nasty delay ordinary rapid fever diet bus maximum clip uphold episode throw disorder drive north south",
       "1HVQmcDk3u9RdwbrjNvLRgftYzwAh2fzX9",0,0,0,"157 B, 24 words, 3 blocks"},
      {"banner cricket leopard dinner alone task junior before nasty delay ordinary rapid fever diet bus maximum clip uphold episode throw disorder drive north south",
       "1863f84WJ7fDDWB4XgNWuZqg7uHCNgaSzw",0,0,1,"157 B, uncompressed"}};
    const int NT=(int)(sizeof ts/sizeof ts[0]);
    int fail=0;
    uint64_t *d_hit,*d_gis;
    CK(cudaMalloc(&d_hit,16)); CK(cudaMalloc(&d_gis,8));
    printf("brainwallet selftest -- priv = SHA256(phrase), no PBKDF2, no BIP32\n\n");
    for(int t=0;t<NT;++t){
        Cfg cf; cf.brain=true; cf.target=ts[t].addr;
        cf.brainKD=1<<ts[t].kd; cf.brainSp=1<<ts[t].sp; cf.brainPub=1<<ts[t].pub;
        std::vector<std::string> ws;
        { std::string s(ts[t].phrase); size_t p=0;
          while(p<=s.size()){ size_t e=s.find(' ',p); if(e==std::string::npos) e=s.size();
              ws.push_back(s.substr(p,e-p)); p=e+1; } }
        cf.words=(int)ws.size();
        if(cf.words>MAXSLOT){ fprintf(stderr,"selftest phrase too long\n"); return 1; }
        cf.slots.assign(cf.words,Slot{M_LIT,-1,{}});
        for(int i=0;i<cf.words;++i){
            // "battery" and "staple" are NOT BIP39 -- the canonical control
            // cannot even be assembled without the EXTRA word table.
            int w=add_extra(ws[i]); if(w<0) return 1;
            cf.slots[i].mode=M_LIT; cf.slots[i].lit=w;
        }
        upload_wl();                       // extras may have been appended
        upload_cfg(cf); upload_paths(cf);
        CK(cudaMemset(d_hit,0xFF,16)); CK(cudaMemset(d_gis,0,8));
        k_derive<<<1,1>>>(d_gis,1,d_hit);
        CK(cudaGetLastError()); CK(cudaDeviceSynchronize());
        uint64_t hv[2]; CK(cudaMemcpy(hv,d_hit,16,cudaMemcpyDeviceToHost));
        bool ok = (hv[0]==0);
        uint64_t want=(uint64_t)((ts[t].sp<<2)|(ts[t].kd<<1)|ts[t].pub);
        if(ok && hv[1]!=want){ ok=false;
            fprintf(stderr,"  variant misreported: got %llu want %llu\n",
                    (unsigned long long)hv[1],(unsigned long long)want); }
        printf("  %2d/%d  %-34s %-38s %s\n",t+1,NT,ts[t].why,ts[t].addr,
               ok?"PASS":"*** FAIL ***");
        if(!ok) fail=1;
    }
    cudaFree(d_hit); cudaFree(d_gis);
    printf("\n%s\n",fail
        ?"*** BRAINWALLET SELFTEST FAILED -- a negative from this mode would be meaningless. ***"
        :"BRAINWALLET SELFTEST PASS -- single/multi-block SHA-256, double-SHA256,\n"
         "  space and no-space joins, compressed and uncompressed keys all verified.");
    return fail;
}

int main(int argc,char**argv){
    const char*cfg=nullptr,*pwf=nullptr,*wlf="bip39_en.txt"; uint64_t resume=0;
    bool st=false, stb=false;
    // --chunk / --seam exist for the seam controls, see seam_and_brain_patch.md.
    uint64_t chunk_override=0, seam=0; bool have_seam=false, count_only=false;
    for(int i=1;i<argc;++i){
        if(!strcmp(argv[i],"--config")&&i+1<argc) cfg=argv[++i];
        else if(!strcmp(argv[i],"--passphrases")&&i+1<argc) pwf=argv[++i];
        else if(!strcmp(argv[i],"--wordlist")&&i+1<argc) wlf=argv[++i];
        else if(!strcmp(argv[i],"--resume")&&i+1<argc) resume=strtoull(argv[++i],nullptr,10);
        else if(!strcmp(argv[i],"--chunk")&&i+1<argc) chunk_override=strtoull(argv[++i],nullptr,10);
        else if(!strcmp(argv[i],"--seam")&&i+1<argc){ seam=strtoull(argv[++i],nullptr,10); have_seam=true; }
        else if(!strcmp(argv[i],"--count-only")) count_only=true;
        else if(!strcmp(argv[i],"--selftest")) st=true;
        else if(!strcmp(argv[i],"--selftest-brain")) stb=true;
        else { fprintf(stderr,"unknown arg %s\n",argv[i]); return 1; }
    }
    if(!load_wl(wlf)){ fprintf(stderr,"need 2048-word list in '%s'\n",wlf); return 1; }
    upload_wl();
    if(st)  return selftest();
    if(stb) return selftest_brain();
    if(!cfg){ fprintf(stderr,
        "usage: %s --config F [--passphrases F] [--resume N] [--chunk N] [--seam N]\n"
        "                  [--count-only]\n"
        "       %s --selftest | --selftest-brain\n",argv[0],argv[0]); return 1; }

    Cfg cf; if(!parse_cfg(cfg,cf)) return 1;
    upload_wl();                       // EXTRA words may have been appended
    upload_cfg(cf); upload_paths(cf);
    cf.total=1;
    for(int i=0;i<cf.words;++i){
        uint32_t n = cf.slots[i].mode==M_LIT?1u
                   : cf.slots[i].mode==M_LIST?(uint32_t)cf.slots[i].list.size()
                   : cf.slots[i].mode==M_POOL?(uint32_t)cf.pool.size():2048u;
        cf.total*=n;
    }
    int gaps=0; for(int i=0;i<cf.words;++i) if(cf.slots[i].mode!=M_LIT) ++gaps;
    if(cf.brain){
        int nvar=__builtin_popcount(cf.brainKD)*__builtin_popcount(cf.brainSp);
        int npub=__builtin_popcount(cf.brainPub);
        printf("scheme=BRAINWALLET  words=%d  gaps=%d  pool=%zu  filter=NONE (accept all)\n",
               cf.words,gaps,cf.pool.size());
        printf("  key      : "); for(int i=0;i<2;++i) if(cf.brainKD&(1<<i)) printf("%s ",BRAIN_KD[i]);
        printf("\n  join     : "); for(int i=0;i<2;++i) if(cf.brainSp&(1<<i)) printf("%s ",BRAIN_SP[i]);
        printf("\n  pubkey   : "); for(int i=0;i<2;++i) if(cf.brainPub&(1<<i)) printf("%s ",BRAIN_PUB[i]);
        printf("\n  %d scalar mult%s per candidate, %d hash160 each\n",
               nvar,nvar==1?"":"s",npub);
        if(WL.size()>N_BIP39)
            printf("  extra words: %zu non-BIP39\n",WL.size()-N_BIP39);
    }
    else if(cf.electrum)
        printf("scheme=ELECTRUM v2  words=%d  gaps=%d  pool=%zu  filter=HMAC prefix 01/100\n",
               cf.words,gaps,cf.pool.size());
    else
        printf("scheme=BIP39  words=%d  gaps=%d  pool=%zu  checksum=1/%d\n",
               cf.words,gaps,cf.pool.size(),1<<(cf.words/3));
    printf("space=%llu  expected derivations=%llu\n",(unsigned long long)cf.total,
           (unsigned long long)(cf.brain? cf.total
                              : cf.electrum? cf.total/171
                              : (cf.total>>(cf.words/3))));

    std::vector<std::string> passes;
    if(cf.brain) passes.push_back("");   // a brainwallet takes no passphrase
    else if(pwf){ FILE*f=fopen(pwf,"r"); if(!f){fprintf(stderr,"cannot open %s\n",pwf); return 1;}
        char b[256]; while(fgets(b,sizeof b,f)){ std::string s2(b);
            while(!s2.empty()&&(s2.back()=='\n'||s2.back()=='\r')) s2.pop_back(); passes.push_back(s2);} fclose(f); }
    else passes.push_back("");
    if(cf.brain && pwf) fprintf(stderr,"warning: --passphrases ignored in brainwallet mode\n");
    printf("passphrases=%zu\n",passes.size());

    const uint32_t CAP=1u<<25;
    uint64_t CHUNK = cf.brain    ? (uint64_t)CAP                     // acceptance 1.0
                   : cf.electrum ? (((uint64_t)CAP<<7)/8)*7          // ~1/171 accept
                                 : (((uint64_t)CAP<<(cf.words/3))/8)*7;   // 12.5% headroom: survivor
                                                          // count is binomial, not exact
    if(chunk_override){
        CHUNK=chunk_override;
        // The survivor buffer is fixed at CAP. An oversized chunk does not
        // silently truncate -- k_filter counts every survivor even past the cap
        // and the loop below aborts -- but say so up front rather than after
        // however long the first chunk takes.
        double acc = cf.brain?1.0 : cf.electrum?1.0/171.0 : 1.0/(double)(1u<<(cf.words/3));
        double exp_surv = (double)CHUNK*acc;
        printf("chunk override : %llu  (expected ~%.0f survivors/chunk, cap %u)\n",
               (unsigned long long)CHUNK,exp_surv,CAP);
        if(exp_surv > 0.95*(double)CAP)
            fprintf(stderr,"warning: chunk too large for the %u-entry survivor buffer;\n"
                           "         use --seam to place a boundary instead.\n",CAP);
    }
    if(have_seam)
        printf("seam           : forcing a chunk boundary at global index %llu\n",
               (unsigned long long)seam);
    if(count_only)
        printf("count-only     : filter stage only, no derivation\n");
    printf("\n");

    uint64_t *d_out,*d_hit; uint32_t *d_n;
    CK(cudaMalloc(&d_out,(size_t)CAP*8)); CK(cudaMalloc(&d_n,4)); CK(cudaMalloc(&d_hit,16));

    for(size_t p=0;p<passes.size();++p){
        upload_salt(passes[p],cf.electrum); CK(cudaMemset(d_hit,0xFF,16));
        printf("[%zu/%zu] %s\n",p+1,passes.size(),passes[p].empty()?"(none)":passes[p].c_str());
        uint64_t done=(p==0)?resume:0;
        uint64_t total_surv=0;      // deterministic: chunking must not change it
        double t0=(double)clock()/CLOCKS_PER_SEC, last_rep=-1.0;
        while(done<cf.total){
            uint64_t n=(cf.total-done<CHUNK)?(cf.total-done):CHUNK;
            // Force a boundary exactly at `seam` so the candidate at that index
            // is the FIRST of its chunk (and the one before it the LAST of the
            // previous). This is the off-by-one that a hit planted mid-chunk
            // cannot detect.
            if(have_seam && done<seam && done+n>seam) n=seam-done;
            CK(cudaMemset(d_n,0,4));
            k_filter<<<(unsigned)((n+255)/256),256>>>(done,n,d_out,d_n,CAP);
            CK(cudaGetLastError());
            uint32_t c=0; CK(cudaMemcpy(&c,d_n,4,cudaMemcpyDeviceToHost));
            if(c>CAP){ fprintf(stderr,"\nsurvivor overflow %u>%u (chunk %llu)\n",
                               c,CAP,(unsigned long long)n); return 1; }
            total_surv += c;
            // --count-only stops after the filter. The survivor total is
            // produced entirely by k_filter's base/count arithmetic, which is
            // exactly what the seam test interrogates; the derive stage only
            // decides whether a survivor MATCHES. Skipping it lets the test run
            // at chunk sizes where derive would otherwise get a handful of
            // candidates per launch and starve the GPU for hours.
            if(c && !count_only){ k_derive<<<(unsigned)((c+127)/128),128>>>(d_out,c,d_hit);
                CK(cudaGetLastError()); CK(cudaDeviceSynchronize());
                uint64_t hv[2]; CK(cudaMemcpy(hv,d_hit,16,cudaMemcpyDeviceToHost));
                if(hv[0]!=0xFFFFFFFFFFFFFFFFULL){ show_hit(cf,hv[0],passes[p],hv[1]); return 0; } }
            done+=n;
            double el=(double)clock()/CLOCKS_PER_SEC-t0;
            // Throttle the per-chunk bookkeeping to ~1 Hz. At production chunk
            // sizes a chunk takes seconds, so this changes nothing; at the tiny
            // chunk sizes the seam count test uses, the fopen+fflush per chunk
            // cost more than the GPU work and made --chunk 7 a 19-hour run.
            // Worst case on a crash is losing under a second of progress.
            if(el-last_rep>=1.0 || done>=cf.total){
                last_rep=el;
                printf("  %6.2f%%  %llu/%llu  survivors %llu  %.0f/s\r",100.0*done/cf.total,
                       (unsigned long long)done,(unsigned long long)cf.total,
                       (unsigned long long)total_surv,done/(el>0?el:1));
                fflush(stdout);
                FILE*ck=fopen("progress2.txt","w");
                if(ck){ fprintf(ck,"%zu %llu\n",p,(unsigned long long)done); fclose(ck); }
            }
        }
        // The survivor total is the seam instrument: it is a pure function of
        // the config, so two runs at different --chunk sizes MUST agree exactly.
        // Any difference is the number of candidates lost or duplicated at joins.
        printf("\n  exhausted, no match  (survivors %llu of %llu)\n",
               (unsigned long long)total_surv,(unsigned long long)cf.total);
    }
    printf("\nall passphrases exhausted, no match.\n");
    return 2;
}
