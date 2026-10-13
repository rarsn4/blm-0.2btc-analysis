#!/usr/bin/env python3
"""Per-run z table for every EVIDENCED run, computed from configs and logs.

sigma model, one formula for all three cases: for a fixed 20-word prefix exactly
one word per 128-block of the 2048 list carries a valid 7-bit checksum, so the
count over slot 21's word set is a sum of 16 independent Bernoullis k_j/128,
k_j = how many of slot 21's words fall in block j. Per-prefix variance is
sum k_j/128 (1 - k_j/128). @FULL gives k_j=128 everywhere: variance 0, an exact
identity. A pinned slot reduces to the binomial. A pool gives the stratified
value, computed from THAT run's pool -- not the 54-pool constant.

Survivor lines are matched to runs by name AND by the 'of <space>' figure, which
must equal the box volume. Resumed runs are scored on their counted segment."""
import sys, os, re, glob, math
sys.argv=['tally2.py','configs']
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tally2.py')).read().split("if __name__")[0]
t={}; exec(compile(src,'tally2.py','exec'), t)
EV=t['EVIDENCED']; CH=3_758_096_384
LOGD=os.path.expanduser('~/Downloads/Brainwallet/files(6)')
WL=[w.strip() for w in open(os.path.join(LOGD,'bip39_en.txt'))]

# every (name, survivors, space, resume) in every log
recs=[]
for f in sorted(glob.glob(LOGD+'/*.log')):
    # single-run logs carry no banner; the filename names the run
    fn=os.path.basename(f)[:-4]
    cur=fn if fn.startswith('t21_') and not fn.endswith('_jac') else None
    resume=0; jac_resumed=False
    for line in open(f, errors='replace'):
        m=re.search(r'\bt21_[a-z0-9_]+', line)
        if m and ('=====' in line or 'START' in line or 'resumed' in line):
            cur=m.group(0); rm=re.search(r'resume from (\d+)', line); resume=int(rm.group(1)) if rm else 0
            # a cross-binary resume records no index; flag it so it is never
            # scored as if the counter covered the whole box
            jac_resumed = 'resumed on Jacobian' in line
        s=re.search(r'survivors (\d+) of (\d+)\)', line)
        if s and cur: recs.append((cur,int(s.group(1)),int(s.group(2)),resume,os.path.basename(f),jac_resumed)); cur=None
def find(name, vol):
    base=name.replace('_p1','')
    c=[r for r in recs if r[0] in (name,base) and r[2]==vol]
    return c[-1] if c else None

rows=[]
for n in EV:
    b=t['load']([n])[n]; vol=t['vol'](b)
    s21=b[21]; n21=len(s21)
    k=[0]*16
    for i in s21: 
        if i<2048: k[i//128]+=1
    pv=sum((x/128)*(1-x/128) for x in k)            # per-prefix variance
    model='identity' if pv==0 else ('binomial' if n21==1 else 'stratified')
    r=find(n, vol)
    if not r: rows.append((n,model,vol,None,None,None,None,None,'NO LOG LINE')); continue
    _,sv,sp,res,lf,jr=r
    infer=False
    if jr and res==0:
        # Index not recorded. Infer it from the identity -- which makes the
        # residual zero BY CONSTRUCTION, so it is not evidence. The independent
        # check is whether the inferred index lands on a chunk boundary.
        res=vol-sv*128; infer=True
    seg=vol-res
    exp=seg//128 if seg%128==0 else seg/128
    var=(seg/n21)*pv
    note=(f"resume {res/CH:.3f} chk" + (" INFERRED: residual 0 by construction, chunk-alignment is the test" if infer else "")) if res else ""
    if model=='identity':
        z=None; d=sv-seg//128; note+=f" residual {d}"
    else:
        sd=math.sqrt(var); z=(sv-seg/128)/sd
    rows.append((n,model,vol,seg,sv,seg/128,(math.sqrt(var) if var else 0),z,note.strip()))

print(f"{'run':20} {'model':10} {'counted cand':>18} {'survivors':>15} {'expected':>17} {'band +/-':>9} {'z':>8}  note")
for n,m,vol,seg,sv,e,sd,z,note in rows:
    if sv is None: print(f"{n:20} {m:10} {'':>18} {'':>15} {'':>17} {'':>9} {'':>8}  {note}"); continue
    zs=f"{z:+.3f}" if z is not None else "  exact"
    print(f"{n:20} {m:10} {seg:>18,} {sv:>15,} {e:>17,.1f} {sd:>9,.0f} {zs:>8}  {note}")
zz=[r[7] for r in rows if r[7] is not None]
print(f"\nscored with a z: {len(zz)}   exact identity: {sum(1 for r in rows if r[1]=='identity')}   "
      f"no log line: {sum(1 for r in rows if r[4] is None)}")
if zz:
    print(f"max |z| {max(abs(x) for x in zz):.3f}   mean z {sum(zz)/len(zz):+.3f}")
