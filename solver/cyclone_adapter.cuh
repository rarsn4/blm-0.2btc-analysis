// cyclone_adapter.cuh — bridge CUDACyclone's EC code to the stage-3 interface.
//
// Cyclone already provides everything needed:
//   scalarMulBaseAffine(const uint64_t scalar_le[4], uint64_t outX[4], uint64_t outY[4])
//
// This adapter only handles representation conversion. It deliberately does NOT
// use Cyclone's getHash160_33_from_limbs, because that function's x_be_limbs
// parameter has ambiguous limb ordering and we already have an exact-verified
// hash160 in stage3.cu (3 vectors, including hash160(G) = 751e76e8...). One
// less thing to get wrong. Revisit later if Cyclone's is measurably faster.
//
// PERFORMANCE WARNING
// Cyclone's own comment at CUDAMath.h:1073 says "we don't need fast
// implementation of point mult". scalarMulBaseAffine is affine double-and-add,
// and pointDoubleAffine / pointAddAffine each call fieldInv — so roughly 384
// modular inversions per scalar multiplication, where a Jacobian windowed
// implementation needs exactly one. Expect this to be very slow. Use it to
// establish CORRECTNESS first; optimize afterwards against it as a reference.

#pragma once
#include <cstdint>
#include "CUDAMath.h"

// If the six vectors all fail with garbage — including k=1 — flip this to 1.
// Cyclone's constants are named SECP_GX_LE, so little-endian limb order
// (limb[0] least significant) is the documented assumption, and that is what
// LIMBS_ARE_BE=0 implements.
#ifndef LIMBS_ARE_BE
#define LIMBS_ARE_BE 0
#endif

// stage3.cu uses uint32_t priv[8], BIG-endian: priv[0] is the most significant
// word. Cyclone wants uint64_t scalar_le[4], little-endian: [0] least
// significant. So the mapping pairs and reverses simultaneously.
__device__ __forceinline__ void priv_be32_to_le64(const uint32_t priv[8],
                                                  uint64_t scalar_le[4]) {
    scalar_le[0] = ((uint64_t)priv[6] << 32) | priv[7];   // least significant
    scalar_le[1] = ((uint64_t)priv[4] << 32) | priv[5];
    scalar_le[2] = ((uint64_t)priv[2] << 32) | priv[3];
    scalar_le[3] = ((uint64_t)priv[0] << 32) | priv[1];   // most significant
}

// Serialize an affine point to a 33-byte compressed public key.
//   pub[0]    = 0x02 | (Y & 1)
//   pub[1..32] = X, 32 bytes big-endian
__device__ __forceinline__ void point_to_compressed(const uint64_t X[4],
                                                    const uint64_t Y[4],
                                                    uint8_t pub[33]) {
#if LIMBS_ARE_BE
    const uint64_t y_ls = Y[3];      // least significant limb
#else
    const uint64_t y_ls = Y[0];
#endif
    pub[0] = (uint8_t)(0x02u | (uint32_t)(y_ls & 1ULL));

#pragma unroll
    for (int i = 0; i < 4; ++i) {
#if LIMBS_ARE_BE
        uint64_t limb = X[i];                 // X[0] already most significant
#else
        uint64_t limb = X[3 - i];             // reverse: X[3] most significant
#endif
#pragma unroll
        for (int b = 0; b < 8; ++b)
            pub[1 + i * 8 + b] = (uint8_t)(limb >> (56 - 8 * b));
    }
}

// The stage-3 interface. Drop-in replacement for the stub in stage3.cu /
// scalarmult_test.cu — delete the stub there and #include this instead.
__device__ void secp256k1_pub_from_priv(const uint32_t priv[8], uint8_t pub[33]) {
    uint64_t k[4], X[4], Y[4];
    priv_be32_to_le64(priv, k);
    scalarMulBaseAffine(k, X, Y);
    point_to_compressed(X, Y, pub);
}

// ---------------------------------------------------------------- brainwallet
// Serialize an affine point to a 65-byte UNCOMPRESSED public key.
//   pub[0]     = 0x04
//   pub[1..32] = X big-endian
//   pub[33..64]= Y big-endian
// 2020-era brainwallet tools frequently defaulted to uncompressed keys, and a
// legacy 1-address is consistent with either form, so both must be tested.
__device__ __forceinline__ void point_to_uncompressed(const uint64_t X[4],
                                                      const uint64_t Y[4],
                                                      uint8_t pub[65]) {
    pub[0] = 0x04;
#pragma unroll
    for (int i = 0; i < 4; ++i) {
#if LIMBS_ARE_BE
        uint64_t xl = X[i],     yl = Y[i];
#else
        uint64_t xl = X[3 - i], yl = Y[3 - i];
#endif
#pragma unroll
        for (int b = 0; b < 8; ++b) {
            pub[1  + i * 8 + b] = (uint8_t)(xl >> (56 - 8 * b));
            pub[33 + i * 8 + b] = (uint8_t)(yl >> (56 - 8 * b));
        }
    }
}

// One scalar multiplication, both serializations. scalarMulBaseAffine is the
// expensive step (~384 field inversions); compressed and uncompressed differ
// only in how the SAME point is written out, so they must not cost two mults.
__device__ __forceinline__ void secp256k1_xy_from_priv(const uint32_t priv[8],
                                                       uint64_t X[4], uint64_t Y[4]) {
    uint64_t k[4];
    priv_be32_to_le64(priv, k);
    scalarMulBaseAffine(k, X, Y);
}
