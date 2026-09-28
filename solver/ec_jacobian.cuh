// ec_jacobian.cuh — fixed-base scalar multiplication in Jacobian coordinates.
//
// WHY. Cyclone's scalarMulBaseAffine is affine double-and-add, and both
// pointDoubleAffine and pointAddAffine call _ModInv. That is ~384 modular
// inversions per scalar multiplication. Jacobian coordinates need exactly ONE,
// at the final conversion back to affine.
//
// Measured share: the elliptic-curve path is ~82% of BIP39 derivation runtime
// (isolated by timing 1-path vs 4-path configs: per-path cost 2.077 s against a
// 1.843 s shared PBKDF2 cost, and BIP32's HMACs are ~24 SHA-512 compressions
// against PBKDF2's 4096, i.e. negligible). So the Amdahl ceiling is 5.51x and a
// 30x multiply lands at 4.82x, 87% of it. A comb table would add ~2% more and is
// deliberately NOT implemented -- it is extra risk surface for nothing.
//
// CORRECTNESS. This file does not replace the affine implementation; it sits
// beside it. ec_jacobian_test.cu differential-tests the two on random scalars
// and requires bit-identical output. The slow, already-verified routine is the
// oracle. Nothing here is wired into the solver until that test passes.
//
// Formulas: a = 0 (secp256k1), so
//   doubling        dbl-2009-l
//   mixed addition  madd-2007-bl   (Q is always affine G)
#pragma once
#include "CUDAMath.h"

struct ECPointJ { uint64_t X[4], Y[4], Z[4]; };   // Z == 0 means the point at infinity

__device__ __forceinline__ bool jIsInf(const ECPointJ &P){ return fieldIsZero(P.Z); }
__device__ __forceinline__ void jSetInf(ECPointJ &P){
    for(int i=0;i<4;++i){ P.X[i]=0; P.Y[i]=0; P.Z[i]=0; }
    P.X[0]=1; P.Y[0]=1;                       // X=Y=1, Z=0 is the usual encoding
}
__device__ __forceinline__ void fieldDbl(const uint64_t a[4], uint64_t o[4]){ fieldAdd(a,a,o); }

// R = 2P   (7 sqr/mul, no inversion)
__device__ void jDouble(const ECPointJ &P, ECPointJ &R){
    if(jIsInf(P)){ jSetInf(R); return; }
    uint64_t A[4],B[4],C[4],D[4],E[4],F[4],t[4],u[4];
    fieldSqr(P.X,A);                       // A = X^2
    fieldSqr(P.Y,B);                       // B = Y^2
    fieldSqr(B,C);                         // C = B^2
    fieldAdd(P.X,B,t); fieldSqr(t,t);      // (X+B)^2
    fieldSub(t,A,t); fieldSub(t,C,t);      // (X+B)^2 - A - C
    fieldDbl(t,D);                         // D = 2*that
    fieldDbl(A,E); fieldAdd(E,A,E);        // E = 3A
    fieldSqr(E,F);                         // F = E^2
    fieldDbl(D,t); fieldSub(F,t,R.X);      // X3 = F - 2D
    fieldSub(D,R.X,t); fieldMul(E,t,t);    // E*(D - X3)
    fieldDbl(C,u); fieldDbl(u,u); fieldDbl(u,u);   // 8C
    fieldSub(t,u,R.Y);                     // Y3 = E*(D-X3) - 8C
    fieldMul(P.Y,P.Z,t); fieldDbl(t,R.Z);  // Z3 = 2*Y*Z
}

// R = P + Q, Q affine (qx,qy). madd-2007-bl. Handles P==inf, P==Q, P==-Q.
__device__ void jAddAffine(const ECPointJ &P, const uint64_t qx[4], const uint64_t qy[4], ECPointJ &R){
    if(jIsInf(P)){
        fieldCopy(qx,R.X); fieldCopy(qy,R.Y);
        R.Z[0]=1; R.Z[1]=R.Z[2]=R.Z[3]=0;
        return;
    }
    uint64_t Z1Z1[4],U2[4],S2[4],H[4],HH[4],I[4],J[4],r[4],V[4],t[4],u[4];
    fieldSqr(P.Z,Z1Z1);                    // Z1Z1 = Z1^2
    fieldMul(qx,Z1Z1,U2);                  // U2 = x2*Z1Z1
    fieldMul(P.Z,Z1Z1,t); fieldMul(qy,t,S2);   // S2 = y2*Z1*Z1Z1
    fieldSub(U2,P.X,H);                    // H = U2 - X1
    fieldSub(S2,P.Y,t);                    // S2 - Y1
    if(fieldIsZero(H)){
        if(fieldIsZero(t)){ jDouble(P,R); return; }   // P == Q
        jSetInf(R); return;                            // P == -Q
    }
    fieldDbl(t,r);                         // r = 2*(S2 - Y1)
    fieldSqr(H,HH);                        // HH = H^2
    fieldDbl(HH,I); fieldDbl(I,I);         // I = 4*HH
    fieldMul(H,I,J);                       // J = H*I
    fieldMul(P.X,I,V);                     // V = X1*I
    fieldSqr(r,t); fieldSub(t,J,t);
    fieldDbl(V,u); fieldSub(t,u,R.X);      // X3 = r^2 - J - 2V
    fieldSub(V,R.X,t); fieldMul(r,t,t);
    fieldMul(P.Y,J,u); fieldDbl(u,u);
    fieldSub(t,u,R.Y);                     // Y3 = r*(V-X3) - 2*Y1*J
    fieldMul(P.Z,H,t); fieldDbl(t,R.Z);    // Z3 = 2*Z1*H
}

// The single inversion for the whole multiplication.
__device__ void jToAffine(const ECPointJ &P, uint64_t outX[4], uint64_t outY[4]){
    if(jIsInf(P)){
        for(int i=0;i<4;++i){ outX[i]=0; outY[i]=0; }
        return;
    }
    // NOTE: _ModInv operates on NBBLOCK = 5 limbs and must NOT be handed a
    // uint64_t[4]. fieldInv is the 4-limb wrapper that zero-extends correctly.
    // Passing the 4-limb array directly compiles, runs, and returns garbage --
    // caught immediately by the differential test, silently fatal without it.
    uint64_t Zi[4],Z2[4],Z3[4];
    fieldInv(P.Z,Zi);
    fieldSqr(Zi,Z2); fieldMul(Z2,Zi,Z3);
    fieldMul(P.X,Z2,outX);
    fieldMul(P.Y,Z3,outY);
}

// Drop-in replacement for scalarMulBaseAffine. Same little-endian limb order,
// same affine output, same all-zero encoding for the infinity result.
__device__ void scalarMulBaseJacobian(const uint64_t scalar_le[4], uint64_t outX[4], uint64_t outY[4]){
    int msb=-1;
    for(int limb=3;limb>=0;--limb){
        uint64_t v=scalar_le[limb];
        if(v){ msb=limb*64+63-__clzll(v); break; }
    }
    if(msb<0){ for(int i=0;i<4;++i){ outX[i]=0; outY[i]=0; } return; }
    uint64_t gx[4],gy[4];
    for(int i=0;i<4;++i){ gx[i]=SECP_GX_LE[i]; gy[i]=SECP_GY_LE[i]; }
    ECPointJ R; jSetInf(R);
    for(int bi=msb;bi>=0;--bi){
        ECPointJ T; jDouble(R,T); R=T;
        if((scalar_le[bi>>6]>>(bi&63))&1ULL){ ECPointJ A; jAddAffine(R,gx,gy,A); R=A; }
    }
    jToAffine(R,outX,outY);
}
