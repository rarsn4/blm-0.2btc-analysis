#!/usr/bin/env python3
"""All three dispersion statistics from ONE correlated simulation.

The analytic versions sat on different footings: the variance p used a rescaled
chi-square, the max-|z| p assumed independence. Here the 41x41 correlation matrix
is built from box intersections (as in rho_bar.py), 10^5 correlated standard-
normal vectors are drawn from it, and all three statistics are read off the same
draws. Also reported: the familywise probability that AT LEAST ONE of the three is
as extreme as observed, which is the right way to handle having looked at three."""
import sys, os, math, itertools
import numpy as np
sys.argv=['tally2.py','configs']
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tally2.py')).read().split("if __name__")[0]
t={}; exec(compile(src,'tally2.py','exec'), t)
runs=[n for n in t['EVIDENCED'] if n!='t21_loo21']
B=t['load'](runs)
def var(box):
    s21=box[21]; k=[0]*16
    for i in s21:
        if i<2048: k[i//128]+=1
    return (t['vol'](box)/len(s21))*sum((x/128)*(1-x/128) for x in k)
def inter(a,b):
    r={}
    for s in range(1,22):
        x=a[s]&b[s]
        if not x: return None
        r[s]=x
    return r
n=len(runs); V=[var(B[r]) for r in runs]
R=np.eye(n)
for i,j in itertools.combinations(range(n),2):
    I=inter(B[runs[i]],B[runs[j]])
    R[i,j]=R[j,i]=(var(I)/math.sqrt(V[i]*V[j])) if I else 0.0
w=np.linalg.eigvalsh(R)
print(f"matrix {n}x{n}   min eigenvalue {w.min():.6f}  ({'positive definite' if w.min()>0 else 'NOT PD'})")
print(f"mean off-diagonal rho {R[np.triu_indices(n,1)].mean():.5f}  (rho_bar.py gave 0.02230)")
OBS_MAX, OBS_S2 = 1.802, 0.6948
rng=np.random.default_rng(20261013)
L=np.linalg.cholesky(R)
N=100_000
Z=rng.standard_normal((N,n))@L.T
mx=np.abs(Z).max(1); s2=Z.var(1,ddof=1); b2=(np.abs(Z)>=2).sum(1)
e1=mx<=OBS_MAX; e2=s2<=OBS_S2; e3=b2==0
se=lambda p: math.sqrt(p*(1-p)/N)
print(f"\n{N:,} correlated draws, seed 20261013:")
print(f"  P(all {n} inside {OBS_MAX})        {e1.mean():.4f}  +/- {se(e1.mean()):.4f}")
print(f"  P(sample Var <= {OBS_S2})         {e2.mean():.4f}  +/- {se(e2.mean()):.4f}")
print(f"  P(none of {n} beyond 2 sigma)     {e3.mean():.4f}  +/- {se(e3.mean()):.4f}")
fw=(e1|e2|e3).mean()
print(f"  P(at least one of the three)    {fw:.4f}  +/- {se(fw):.4f}   <- familywise")
print(f"\n  mean simulated sample Var {s2.mean():.4f}   (1 - rho_bar = {1-R[np.triu_indices(n,1)].mean():.4f})")
