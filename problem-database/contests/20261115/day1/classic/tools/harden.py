from pathlib import Path
import subprocess,json,math
R=Path(__file__).resolve().parents[1]

def check(case,out):
 p=R/f'data/{case}'
 r=subprocess.run([str(R/'tools/official'),str(p)+'.in',str(out),str(p)+'.ans'],capture_output=True)
 return {'accepted':r.returncode==0,'message':r.stderr.decode().strip()}

if __name__=='__main__':
 subprocess.run(['g++','-O2','-std=c++14',str(R/'tools/wrong.cpp'),'-o',str(R/'tools/wrong')],check=True)
 audit={}
 for mode in ['log','mod','mst']:
  rows={}
  for case in [17,18,19,20,21,22,23,24,25]:
   out=R/f'tools/.wrong-{mode}.out'
   exe=[str(R/'tools/oracle'),'distinct']if mode=='mst'else[str(R/'tools/wrong'),mode]
   with (R/f'data/{case}.in').open('rb')as fi,out.open('wb')as fo:subprocess.run(exe,stdin=fi,stdout=fo,check=True,timeout=40)
   rows[str(case)]=check(case,out)
  if mode=='mst':assert all(not rows[str(k)]['accepted']for k in [23,24,25]),rows
  else:assert any(not v['accepted']for k,v in rows.items()if int(k)>=23),(mode,rows)
  audit[mode]=rows
 # Exact count for the designated repeated-carry construction (point 24).
 n=100000;p=n//2
 audit['per_bit_carry']=dict(case=24,reused_version_ones=p-1,independent_extensions=n-p-3,bit_flips_lower_bound=(p-1)*(n-p-3),description='Each extension adds 2 to the same distance 2^50000-2; deleting the final 49999 one-bits cannot be amortized over versions.')
 # Indexed arbitrary-precision heap, independent of the standard solution.
 out=R/'tools/.big-benchmark.out';timing=R/'tools/big-benchmark.txt'
 with (R/'data/25.in').open('rb')as fi,out.open('wb')as fo:
  subprocess.run(['/usr/bin/time','-f','%e %M','-o',str(timing),str(R/'tools/oracle'),'big'],stdin=fi,stdout=fo,check=True,timeout=200)
 seconds,kib=timing.read_text().split();audit['cpp_int']=dict(case=25,seconds=float(seconds),peak_kib=int(kib),**check(25,out))
 assert audit['cpp_int']['accepted']
 audit['formal']=dict(points=25,points_each=4,tiers=[12,8,4,8,16,16,24,12],large_samples=8,inline_samples=3)
 (R/'tools/hardening-audit.json').write_text(json.dumps(audit,indent=2))
 print(json.dumps(audit,indent=2),flush=True)
