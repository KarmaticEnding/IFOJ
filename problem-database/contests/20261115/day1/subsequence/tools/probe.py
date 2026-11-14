from pathlib import Path
import sys,random,subprocess
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from model import encode,greedy,binary_only
r=random.Random(1409);fail=0
for z in range(100):
 s=''.join(r.choices('abc',k=200));k=r.randint(5,120)
 ans=int(subprocess.check_output([str(R/'tools/std')],input=encode(s,'ab',k).encode()))
 a,b=greedy(s,'ab',k),greedy(s,'ab',k,True)
 if max(a,b)<ans:
  fail+=1
  if fail<=5:print('counterexample',z,k,ans,a,b,flush=True)
print('Both greedy tie orders failed on',fail,'of 100 random full-size probes.',flush=True)
