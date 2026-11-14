from pathlib import Path
import random,json,hashlib,subprocess,time,tempfile,sys
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'tools'));from model import solve,validate,small_dp,P
MAXB=10**18
GROUPS=[(1,2,6,9,'general'),(3,6,2000,20,'general'),(7,10,1000000,MAXB,'up'),(11,14,1000000,MAXB,'down'),(15,20,1000000,MAXB,'general')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def make(n,kind,seed,flavor='valid'):
 rng=random.Random(seed)
 if n==6:
  if seed>=2026112400:return [9,6,6,8,8,8]
  return [4,6,3,3,9,9]if seed%2 else [1,2,2,7,7,9]
 if n==2000:
  plan=[16,20,15,18,12,14,16,18,20,10,20];events=sorted(rng.sample(range(1,n-2),9))+[n-2];b=[plan[0]]*n;at=0
  for i in range(n):
   if at<len(events)and i==events[at]:at+=1
   b[i]=plan[at]
  if flavor=='invalid':b[-1]=19
  return b
 zero='zero'in flavor
 if kind=='up':
  root=2 if zero else rng.randint(100000,3000000)if flavor=='wide'else rng.randint(30000000,400000000)
  hi=root+P-1 if zero else root;limit=MAXB//root;b=[root*root,root*hi,root*hi]if zero else [root*root]
  start=hi
  for i in range(len(b),n):
   if rng.random()<.65 or i==n-1:hi=start+(limit-start)*i//(n-1)
   b.append(root*hi)
 elif kind=='down':
  root=10**9 if flavor=='boundary'else rng.randint(700000000,999999999)
  lo=root-P+1 if zero else root;b=[root*root,root*lo,root*lo]if zero else[root*root];start=lo
  for i in range(len(b),n):
   if rng.random()<.65 or i==n-1:lo=max(1,start-(start-1)*i//(n-1))
   b.append(root*lo)
  if 'invalid'in flavor:b[-1]=b[-2]-1
 else:
  root=100000000 if zero else 10**9 if flavor=='boundary'else rng.randint(100000000,800000000)
  lo=root;hi=root+P-1 if zero else root;b=[root*root,lo*hi,lo*hi]if zero else[root*root]
  for i in range(len(b),n-3):
   v=rng.random();remaining=max(1,(n-i)//3)
   if v<.33 and lo>1:lo=max(1,lo-rng.randint(1,max(1,(lo-1)//remaining)))
   elif v<.68 and MAXB//lo>hi:hi=min(MAXB//lo,hi+rng.randint(1,max(1,(MAXB//lo-hi)//remaining)))
   b.append(lo*hi)
  b.extend([hi,MAXB,MAXB])
  if 'invalid'in flavor:b[-1]=MAXB-1
  if flavor=='nonsquare':b[0]=MAXB-1
 return b
def save(folder,index,b,group,flavor):
 _,_,N,V,kind=GROUPS[group-1];assert len(b)==N and all(1<=v<=V for v in b)
 if kind=='up':assert all(x<=y for x,y in zip(b,b[1:]))
 if kind=='down':assert all(x>=y for x,y in zip(b,b[1:]))
 expected,alternate=solve(b)
 if V<=20:assert expected==small_dp(b)
 if 'invalid'in flavor or flavor=='nonsquare':assert expected==-1,(index,flavor)
 if 'zero'in flavor and 'invalid'not in flavor:assert expected==0
 path=R/folder/f'{index}.in';ans=path.with_suffix('.ans');assert not path.exists()and not ans.exists()
 path.write_text(str(len(b))+'\n'+' '.join(map(str,b))+'\n');ans.write_text(str(expected)+'\n')
 start=time.monotonic()
 with tempfile.TemporaryDirectory()as tmp:
  out=Path(tmp)/'output'
  with path.open('rb')as inp,out.open('wb')as dest:subprocess.run([str(R/'tools/std')],stdin=inp,stdout=dest,check=True,timeout=20)
  elapsed=time.monotonic()-start;validate(b,out.read_bytes(),expected)
  for checker in ['official','public']:
   result=subprocess.run([str(R/'tools'/checker),str(path),str(out),str(ans)],capture_output=True,timeout=30);assert result.returncode==0,(index,checker,result.stderr)
  # Exercise non-unique full-size output and >10 MB lines once, too.
  if folder=='down'and group==5:
   out.write_text(str(expected)+'\n'+(' '.join(map(str,alternate))if alternate else '-1')+'\n')
   for checker in ['official','public']:assert subprocess.run([str(R/'tools'/checker),str(path),str(out),str(ans)],capture_output=True,timeout=30).returncode==0
 row={'input':str(path.relative_to(R)),'group':group,'n':len(b),'maximum_b':max(b),'kind':kind,'flavor':flavor,'count':expected,'std_seconds':elapsed,'input_sha256':sha(path),'answer_sha256':sha(ans)};print(row,flush=True);return row
if __name__=='__main__':
 gate=json.loads((R/'tools/verification.json').read_text());assert gate['passed']
 for p,key in [('GPT/product.cpp','std_sha256'),('data/chk/chk.cpp','official_sha256'),('down/checker.cpp','public_sha256')]:assert sha(R/p)==gate[key]
 for d in ['data','down']:(R/d).mkdir(exist_ok=True)
 rows=[]
 examples=[([4,6,6],b'2\n2 3 3\n'),([4,7],b'-1\n-1\n'),([1,P,P],f'0\n1 {P} {P}\n'.encode())]
 for i,(b,out)in enumerate(examples,1):
  p=R/'down'/f'{i}.in';ans=p.with_suffix('.ans');assert not p.exists()and not ans.exists();count,_=solve(b);validate(b,out,count)
  p.write_text(str(len(b))+'\n'+' '.join(map(str,b))+'\n');ans.write_text(str(count)+'\n');p.with_suffix('.out').write_bytes(out)
  for checker in ['official','public']:assert subprocess.run([str(R/'tools'/checker),str(p),str(p.with_suffix('.out')),str(ans)],capture_output=True).returncode==0
  rows.append({'input':str(p.relative_to(R)),'inline_sample':True,'count':count,'input_sha256':sha(p),'answer_sha256':sha(ans)})
 flavors={5:'invalid',7:'zero',9:'wide',11:'zero',13:'zero_invalid',14:'boundary',16:'zero',17:'zero_invalid',19:'boundary',20:'nonsquare'}
 for g,(left,right,n,V,kind)in enumerate(GROUPS,1):
  for i in range(left,right+1):flavor=flavors.get(i,'valid');rows.append(save('data',i,make(n,kind,2026111400+i,flavor),g,flavor))
  flavor='zero'if g in(3,4)else'valid';rows.append(save('down',g+3,make(n,kind,2026112400+g,flavor),g,flavor))
 (R/'tools/data-manifest.json').write_text(json.dumps(rows,indent=2))
