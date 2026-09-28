// Differential test: scalarMulBaseJacobian vs the verified scalarMulBaseAffine.
// The slow routine is the oracle. Bit-identical or the new one does not ship.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <cuda_runtime.h>
#include "ec_jacobian.cuh"

#define CK(x) do{ cudaError_t e=(x); if(e!=cudaSuccess){ \
  fprintf(stderr,"CUDA %s @%d: %s\n",#x,__LINE__,cudaGetErrorString(e)); exit(1);} }while(0)

__global__ void kAff(const uint64_t*s,uint64_t*X,uint64_t*Y,int n){
    int i=blockIdx.x*blockDim.x+threadIdx.x; if(i>=n)return;
    scalarMulBaseAffine(s+i*4,X+i*4,Y+i*4);
}
__global__ void kJac(const uint64_t*s,uint64_t*X,uint64_t*Y,int n){
    int i=blockIdx.x*blockDim.x+threadIdx.x; if(i>=n)return;
    scalarMulBaseJacobian(s+i*4,X+i*4,Y+i*4);
}

int main(int argc,char**argv){
    int N = argc>1?atoi(argv[1]):4096;
    uint64_t *hs=(uint64_t*)malloc(N*32);
    srand(12345);
    // n-1, 1, 2, 3 and then random 256-bit scalars below n
    memset(hs,0,N*32);
    hs[0]=1;                                    // k=1 -> G
    hs[4]=2; hs[8]=3;
    hs[12]=0xBFD25E8CD0364140ULL; hs[13]=0xBAAEDCE6AF48A03BULL;
    hs[14]=0xFFFFFFFFFFFFFFFEULL; hs[15]=0xFFFFFFFFFFFFFFFFULL;   // n-1
    for(int i=4;i<N;++i){
        for(int j=0;j<4;++j)
            hs[i*4+j]=((uint64_t)rand()<<48)^((uint64_t)rand()<<32)^((uint64_t)rand()<<16)^rand();
        hs[i*4+3] &= 0x7FFFFFFFFFFFFFFFULL;     // keep below n
    }
    uint64_t *ds,*aX,*aY,*jX,*jY;
    CK(cudaMalloc(&ds,N*32)); CK(cudaMalloc(&aX,N*32)); CK(cudaMalloc(&aY,N*32));
    CK(cudaMalloc(&jX,N*32)); CK(cudaMalloc(&jY,N*32));
    CK(cudaMemcpy(ds,hs,N*32,cudaMemcpyHostToDevice));
    int TB=64, GB=(N+TB-1)/TB;

    cudaEvent_t e0,e1; cudaEventCreate(&e0); cudaEventCreate(&e1); float ta=0,tj=0;
    kAff<<<GB,TB>>>(ds,aX,aY,N); CK(cudaGetLastError()); CK(cudaDeviceSynchronize());
    cudaEventRecord(e0); kAff<<<GB,TB>>>(ds,aX,aY,N); cudaEventRecord(e1);
    CK(cudaDeviceSynchronize()); cudaEventElapsedTime(&ta,e0,e1);
    kJac<<<GB,TB>>>(ds,jX,jY,N); CK(cudaGetLastError()); CK(cudaDeviceSynchronize());
    cudaEventRecord(e0); kJac<<<GB,TB>>>(ds,jX,jY,N); cudaEventRecord(e1);
    CK(cudaDeviceSynchronize()); cudaEventElapsedTime(&tj,e0,e1);

    uint64_t *ax=(uint64_t*)malloc(N*32),*ay=(uint64_t*)malloc(N*32);
    uint64_t *jx=(uint64_t*)malloc(N*32),*jy=(uint64_t*)malloc(N*32);
    CK(cudaMemcpy(ax,aX,N*32,cudaMemcpyDeviceToHost));
    CK(cudaMemcpy(ay,aY,N*32,cudaMemcpyDeviceToHost));
    CK(cudaMemcpy(jx,jX,N*32,cudaMemcpyDeviceToHost));
    CK(cudaMemcpy(jy,jY,N*32,cudaMemcpyDeviceToHost));

    int bad=0;
    for(int i=0;i<N;++i)
        if(memcmp(ax+i*4,jx+i*4,32)||memcmp(ay+i*4,jy+i*4,32)){
            if(bad<3){
                printf("  MISMATCH at %d\n    scalar %016lx%016lx%016lx%016lx\n",i,
                       hs[i*4+3],hs[i*4+2],hs[i*4+1],hs[i*4+0]);
                printf("    affine X %016lx%016lx%016lx%016lx\n",ax[i*4+3],ax[i*4+2],ax[i*4+1],ax[i*4+0]);
                printf("    jacob  X %016lx%016lx%016lx%016lx\n",jx[i*4+3],jx[i*4+2],jx[i*4+1],jx[i*4+0]);
            }
            ++bad;
        }
    // k=1 must be G
    
    printf("\n  scalars tested        : %d  (incl. k=1, 2, 3, n-1)\n",N);
    printf("  mismatches            : %d\n",bad);
    printf("  affine kernel         : %8.2f ms   (%.0f mult/s)\n",ta,N/(ta/1000.0));
    printf("  jacobian kernel       : %8.2f ms   (%.0f mult/s)\n",tj,N/(tj/1000.0));
    printf("  SPEEDUP               : %8.2fx\n",ta/tj);
    printf("\n  %s\n", bad?"*** FAIL — do not ship ***":"PASS — bit-identical to the verified affine routine");
    return bad?1:0;
}
