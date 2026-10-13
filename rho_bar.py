#!/usr/bin/env python3
"""Mean pairwise correlation of the per-run z-scores, from box intersections.

Survivor counts over boxes A and B co-vary only through their shared sub-box, so
Cov(N_A, N_B) = Var(N_{A∩B}) and rho_AB = Var(N_{A∩B}) / (sigma_A sigma_B).
Every variance uses the per-prefix stratified formula on THAT box's slot-21 set:
Var(N_X) = (vol(X) / |S21_X|) * sum_j k_j/128 (1 - k_j/128).

For n standardised scores with mean pairwise correlation rho, E[s^2] = 1 - rho, so
positive correlation pushes the sample variance DOWN. This measures how much.

Approximation, stated: t21_loo6 was scored on its counted segment (86% of its box);
here its full box is used for both numerator and denominator. t21_loo21 has no z
(exact identity) and is excluded, leaving 41 runs and 820 pairs."""
import sys, os, math, itertools
sys.argv=['tally2.py','configs']
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tally2.py')).read().split("if __name__")[0]
t={}; exec(compile(src,'tally2.py','exec'), t)
runs=[n for n in t['EVIDENCED'] if n!='t21_loo21']
B=t['load'](runs)
def var(box):
    s21=box[21]; k=[0]*16
    for i in s21:
        if i<2048: k[i//128]+=1
    pv=sum((x/128)*(1-x/128) for x in k)
    return (t['vol'](box)/len(s21))*pv
def inter(a,b):
    r={}
    for s in range(1,22):
        x=a[s]&b[s]
        if not x: return None
        r[s]=x
    return r
V={n:var(B[n]) for n in runs}
rhos=[]; nz=0; top=[]
for a,b in itertools.combinations(runs,2):
    I=inter(B[a],B[b])
    r=(var(I)/math.sqrt(V[a]*V[b])) if I else 0.0
    rhos.append(r)
    if r>0: nz+=1; top.append((r,a,b))
rb=sum(rhos)/len(rhos)
print(f"runs {len(runs)}   pairs {len(rhos)}   pairs with any overlap {nz}")
print(f"mean pairwise rho          {rb:.5f}")
print(f"E[s^2] = 1 - rho_bar        {1-rb:.4f}")
top.sort(reverse=True)
print("largest pairwise rho:")
for r,a,b in top[:8]: print(f"  {r:.4f}  {a} x {b}")
