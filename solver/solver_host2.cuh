// solver_host2.cuh — host driver for solver2.cu (template mode).
#pragma once
#define CK(x) do{ cudaError_t e_=(x); if(e_!=cudaSuccess){ \
    fprintf(stderr,"CUDA %s @%d: %s\n",#x,__LINE__,cudaGetErrorString(e_)); exit(1);} }while(0)

static std::vector<std::string> WL;

static bool load_wl(const char*p){
    FILE*f=fopen(p,"r"); if(!f) return false;
    char b[64];
    while(fgets(b,sizeof b,f)){ std::string w(b);
        while(!w.empty()&&(w.back()=='\n'||w.back()=='\r'||w.back()==' ')) w.pop_back();
        if(!w.empty()) WL.push_back(w); }
    fclose(f); return WL.size()==2048;
}
static int widx(const std::string&w){
    for(size_t i=0;i<WL.size();++i) if(WL[i]==w) return (int)i;
    return -1;
}
static void upload_wl(){
    static char ch[16384]; static uint16_t off[2048]; static uint8_t len[2048];
    int o=0;
    for(int i=0;i<2048;++i){ off[i]=(uint16_t)o; len[i]=(uint8_t)WL[i].size();
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
};

static bool parse_cfg(const char*path,Cfg&cf){
    FILE*f=fopen(path,"r"); if(!f){fprintf(stderr,"cannot open %s\n",path); return false;}
    char line[2048];
    std::vector<std::pair<int,std::string>> raw;
    while(fgets(line,sizeof line,f)){
        char*p=line; while(*p==' '||*p=='\t')++p;
        if(*p=='#'||*p=='\n'||*p=='\r'||!*p) continue;
        char*k=strtok(p," \t\r\n"); if(!k) continue;
        std::string key(k);
        if(key=="WORDS"){ cf.words=atoi(strtok(NULL," \t\r\n")); }
        else if(key=="TARGET"){ cf.target=strtok(NULL," \t\r\n"); }
        else if(key=="HASH160"){ cf.h160=strtok(NULL," \t\r\n"); }
        else if(key=="SCHEME"){ char*v=strtok(NULL," \t\r\n");
            if(v) cf.electrum = (strcmp(v,"electrum")==0); }
        else if(key=="POOL"){ char*t; while((t=strtok(NULL," \t\r\n"))){
            int i=widx(t); if(i<0){fprintf(stderr,"POOL '%s' not BIP39\n",t); return false;}
            bool dup=false; for(int q:cf.pool) if(q==i) dup=true;
            if(!dup) cf.pool.push_back(i); } }
        else if(key=="PATH"){ char*v=strtok(NULL," \t\r\n");
            if(v) cf.paths.push_back(std::string(v)); }
        else if(key=="SLOT"){ int n=atoi(strtok(NULL," \t\r\n"));
            char*v=strtok(NULL," \t\r\n"); if(!v){fprintf(stderr,"SLOT %d has no value\n",n); return false;}
            raw.push_back({n,std::string(v)}); }
        else fprintf(stderr,"warning: unknown key '%s'\n",key.c_str());
    }
    fclose(f);
    if(!cf.electrum && cf.words!=12&&cf.words!=15&&cf.words!=18&&cf.words!=21&&cf.words!=24){
        fprintf(stderr,"WORDS must be 12/15/18/21/24 for BIP39 (got %d)\n",cf.words); return false; }
    if(cf.electrum && (cf.words<3||cf.words>MAXSLOT)){
        fprintf(stderr,"WORDS must be 3..%d for electrum (got %d)\n",MAXSLOT,cf.words); return false; }
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
            cf.slots[n].mode=M_LIST; size_t s=0;
            while(s<=v.size()){ size_t e=v.find('|',s); if(e==std::string::npos) e=v.size();
                std::string w=v.substr(s,e-s);
                int i=widx(w); if(i<0){fprintf(stderr,"'%s' not BIP39\n",w.c_str()); return false;}
                cf.slots[n].list.push_back(i); s=e+1; }
            if(cf.slots[n].list.size()>MAXLIST){fprintf(stderr,"slot %d list too long\n",pr.first); return false;}
        } else {
            int i=widx(v); if(i<0){fprintf(stderr,"'%s' not BIP39\n",v.c_str()); return false;}
            cf.slots[n].mode=M_LIT; cf.slots[n].lit=i;
        }
    }
    for(int i=0;i<cf.words;++i) if(!seen[i]){ fprintf(stderr,"SLOT %d missing\n",i+1); return false; }
    if(cf.pool.size()>MAXPOOL){fprintf(stderr,"POOL too big\n"); return false;}
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

static void show_hit(const Cfg&cf,uint64_t gi,const std::string&pass){
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
    printf("passphrase : %s\n",pass.empty()?"(none)":pass.c_str());
    printf("path       : m/44'/0'/0'/0/0\n");
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
    CK(cudaMalloc(&d_hit,8)); CK(cudaMalloc(&d_gis,8));
    for(int t=0;t<2;++t){
        Cfg cf; cf.words=ts[t].w; cf.target=ts[t].addr;
        cf.slots.assign(cf.words,Slot{M_LIT,-1,{}});
        std::string s(ts[t].mn); size_t p=0; int i=0;
        while(p<s.size()&&i<cf.words){ size_t e=s.find(' ',p); if(e==std::string::npos) e=s.size();
            cf.slots[i].lit=widx(s.substr(p,e-p)); cf.slots[i].mode=M_LIT; p=e+1; ++i; }
        upload_cfg(cf); upload_paths(cf); upload_salt("",cf.electrum);
        CK(cudaMemset(d_hit,0xFF,8)); CK(cudaMemset(d_gis,0,8));
        k_derive<<<1,1>>>(d_gis,1,d_hit);
        CK(cudaGetLastError()); CK(cudaDeviceSynchronize());
        uint64_t h; CK(cudaMemcpy(&h,d_hit,8,cudaMemcpyDeviceToHost));
        printf("  %2d-word canonical -> %s   %s\n",ts[t].w,ts[t].addr,h==0?"PASS":"*** FAIL ***");
        if(h!=0) fail=1;
    }
    printf("\n%s\n",fail?"*** SELFTEST FAILED — do not run a sweep. ***"
                        :"SELFTEST PASS — 12- and 24-word paths both verified.");
    return fail;
}

int main(int argc,char**argv){
    const char*cfg=nullptr,*pwf=nullptr,*wlf="bip39_en.txt"; uint64_t resume=0; bool st=false;
    for(int i=1;i<argc;++i){
        if(!strcmp(argv[i],"--config")&&i+1<argc) cfg=argv[++i];
        else if(!strcmp(argv[i],"--passphrases")&&i+1<argc) pwf=argv[++i];
        else if(!strcmp(argv[i],"--wordlist")&&i+1<argc) wlf=argv[++i];
        else if(!strcmp(argv[i],"--resume")&&i+1<argc) resume=strtoull(argv[++i],nullptr,10);
        else if(!strcmp(argv[i],"--selftest")) st=true;
        else { fprintf(stderr,"unknown arg %s\n",argv[i]); return 1; }
    }
    if(!load_wl(wlf)){ fprintf(stderr,"need 2048-word list in '%s'\n",wlf); return 1; }
    upload_wl();
    if(st) return selftest();
    if(!cfg){ fprintf(stderr,"usage: %s --config F [--passphrases F] [--resume N] | --selftest\n",argv[0]); return 1; }

    Cfg cf; if(!parse_cfg(cfg,cf)) return 1;
    upload_cfg(cf); upload_paths(cf);
    cf.total=1;
    for(int i=0;i<cf.words;++i){
        uint32_t n = cf.slots[i].mode==M_LIT?1u
                   : cf.slots[i].mode==M_LIST?(uint32_t)cf.slots[i].list.size()
                   : cf.slots[i].mode==M_POOL?(uint32_t)cf.pool.size():2048u;
        cf.total*=n;
    }
    int gaps=0; for(int i=0;i<cf.words;++i) if(cf.slots[i].mode!=M_LIT) ++gaps;
    if(cf.electrum)
        printf("scheme=ELECTRUM v2  words=%d  gaps=%d  pool=%zu  filter=HMAC prefix 01/100\n",
               cf.words,gaps,cf.pool.size());
    else
        printf("scheme=BIP39  words=%d  gaps=%d  pool=%zu  checksum=1/%d\n",
               cf.words,gaps,cf.pool.size(),1<<(cf.words/3));
    printf("space=%llu  expected derivations=%llu\n",(unsigned long long)cf.total,
           (unsigned long long)(cf.electrum? cf.total/171 : (cf.total>>(cf.words/3))));

    std::vector<std::string> passes;
    if(pwf){ FILE*f=fopen(pwf,"r"); if(!f){fprintf(stderr,"cannot open %s\n",pwf); return 1;}
        char b[256]; while(fgets(b,sizeof b,f)){ std::string s(b);
            while(!s.empty()&&(s.back()=='\n'||s.back()=='\r')) s.pop_back(); passes.push_back(s);} fclose(f); }
    else passes.push_back("");
    printf("passphrases=%zu\n\n",passes.size());

    const uint32_t CAP=1u<<25;
    uint64_t CHUNK = cf.electrum ? (((uint64_t)CAP<<7)/8)*7          // ~1/171 accept
                                 : (((uint64_t)CAP<<(cf.words/3))/8)*7;   // 12.5% headroom: survivor
                                                          // count is binomial, not exact
    uint64_t *d_out,*d_hit; uint32_t *d_n;
    CK(cudaMalloc(&d_out,(size_t)CAP*8)); CK(cudaMalloc(&d_n,4)); CK(cudaMalloc(&d_hit,8));

    for(size_t p=0;p<passes.size();++p){
        upload_salt(passes[p],cf.electrum); CK(cudaMemset(d_hit,0xFF,8));
        printf("[%zu/%zu] %s\n",p+1,passes.size(),passes[p].empty()?"(none)":passes[p].c_str());
        uint64_t done=(p==0)?resume:0;
        double t0=(double)clock()/CLOCKS_PER_SEC;
        while(done<cf.total){
            uint64_t n=(cf.total-done<CHUNK)?(cf.total-done):CHUNK;
            CK(cudaMemset(d_n,0,4));
            k_filter<<<(unsigned)((n+255)/256),256>>>(done,n,d_out,d_n,CAP);
            CK(cudaGetLastError());
            uint32_t c=0; CK(cudaMemcpy(&c,d_n,4,cudaMemcpyDeviceToHost));
            if(c>CAP){ fprintf(stderr,"\nsurvivor overflow %u>%u\n",c,CAP); return 1; }
            if(c){ k_derive<<<(unsigned)((c+127)/128),128>>>(d_out,c,d_hit);
                CK(cudaGetLastError()); CK(cudaDeviceSynchronize());
                uint64_t h; CK(cudaMemcpy(&h,d_hit,8,cudaMemcpyDeviceToHost));
                if(h!=0xFFFFFFFFFFFFFFFFULL){ show_hit(cf,h,passes[p]); return 0; } }
            done+=n;
            double el=(double)clock()/CLOCKS_PER_SEC-t0;
            printf("  %6.2f%%  %llu/%llu  survivors %u  %.0f/s\r",100.0*done/cf.total,
                   (unsigned long long)done,(unsigned long long)cf.total,c,done/(el>0?el:1));
            fflush(stdout);
            FILE*ck=fopen("progress2.txt","w");
            if(ck){ fprintf(ck,"%zu %llu\n",p,(unsigned long long)done); fclose(ck); }
        }
        printf("\n  exhausted, no match\n");
    }
    printf("\nall passphrases exhausted, no match.\n");
    return 2;
}
