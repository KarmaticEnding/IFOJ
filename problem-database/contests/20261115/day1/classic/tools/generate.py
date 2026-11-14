"""Deterministic data generation, gated by the completed independent verification."""
from pathlib import Path
import random, subprocess, json, hashlib, resource, time, shutil, sys
R=Path(__file__).resolve().parents[1]
SEED=20261114464

class Graph:
 def __init__(self,n,seed):self.n=n;self.r=random.Random(seed);self.e={};self.s=1;self.t=n
 def add(self,u,v,x):
  assert 1<=u<=self.n and 1<=v<=self.n and 0<=x<=100000
  if u==v:return False
  k=(min(u,v),max(u,v))
  if k in self.e:return False
  self.e[k]=x;return True
 def fill(self,m,weight,lo=1,hi=None):
  if hi is None:hi=self.n
  while len(self.e)<m:self.add(self.r.randint(lo,hi),self.r.randint(lo,hi),weight())
 def write(self,path):
  edges=[(u,v,x)for(u,v),x in self.e.items()];self.r.shuffle(edges)
  with path.open('w')as f:
   f.write(f'{self.n} {len(edges)}\n')
   for u,v,x in edges:
    if self.r.randrange(2):u,v=v,u
    f.write(f'{u} {v} {x}\n')
   f.write(f'{self.s} {self.t}\n')

def ordinary(n,m,seed,low,high,disconnected=False):
 g=Graph(n,seed);r=g.r
 # A substantial chain plus random-parent branches; no bounded-degree promise.
 end=n//2 if disconnected else n
 for v in range(2,n+1):
  if v==end+1:continue
  start=1 if v<=end else end+1
  u=v-1 if v%3 else r.randint(start,v-1)
  g.add(u,v,r.randint(low,high))
 while len(g.e)<m:
  left,right=(1,end)if not disconnected or r.randrange(2)else(end+1,n)
  g.add(r.randint(left,right),r.randint(left,right),r.randint(low,high))
 # Explicit endpoints of the promised exponent range.
 keys=list(g.e);g.e[keys[0]]=low;g.e[keys[1]]=high
 return g

def tree(n,seed):
 g=Graph(n,seed)
 for v in range(2,n+1):g.add(v-1 if v<n//2 else g.r.randint(1,v-1),v,g.r.randint(0,100000))
 g.e[(1,2)]=100000;return g

def cycle(n,seed):
 g=Graph(n,seed);c=2*n//3
 for v in range(2,c+1):g.add(v-1,v,g.r.randint(0,100000))
 g.add(1,c,99999)
 for v in range(c+1,n+1):g.add(g.r.randint(1,v-1),v,g.r.randint(0,100000))
 g.s=n-1;g.t=n;g.e[(1,2)]=100000;return g

def two(n,m,seed,a,b):
 g=ordinary(n,m,seed,0,1)
 for k in g.e:g.e[k]=a if g.r.randrange(2)else b
 keys=list(g.e);g.e[keys[0]]=a;g.e[keys[1]]=b;return g

def unique(n,seed,disconnected=False):
 g=ordinary(n,100001,seed,0,100000,disconnected);xs=list(range(100001));g.r.shuffle(xs)
 for k,x in zip(g.e,xs):g.e[k]=x
 return g

def common(n,m,seed):
 g=Graph(n,seed);g.add(1,2,100000);p=n-3
 for v in range(3,p+1):g.add(v-1 if v%3 else g.r.randint(2,v-1),v,g.r.randint(0,60000))
 k=g.r.randint(1000,1500)
 # Mandatory terminal gadget: MST takes three unit edges, optimum takes two.
 g.add(p,n,k+1);g.add(p,n-2,k);g.add(n-2,n-1,k);g.add(n-1,n,k)
 g.fill(m,lambda:g.r.randint(0,60000),2,p);return g

def ripple(n,m,seed):
 g=Graph(n,seed);p=n//2
 for v in range(2,p+1):g.add(v-1,v,v-1)
 for v in range(p+1,n-2):g.add(p,v,1)
 g.add(n-3,n,1);g.add(n-3,n-2,0);g.add(n-2,n-1,0);g.add(n-1,n,0)
 # These edges cannot improve any shortest distance through the small edges.
 g.fill(m,lambda:g.r.randint(99980,100000),2,n-3)
 g.e[(2,n-3)]=100000
 # Keep exact requested m, even if the forced maximum was an absent edge.
 if len(g.e)>m:
  for k in reversed(list(g.e)):
   if k!=(2,n-3)and g.e[k]>=99980:del g.e[k];break
 return g

def gadgets(n,m,seed):
 g=Graph(n,seed);g.add(1,2,100000);u=2;kind=0
 while u+3<=n:
  k=g.r.randint(0,2000)
  if kind%3==0:
   a,b,v=u+1,u+2,u+3
   g.add(u,v,k+1);g.add(u,a,k);g.add(a,b,k);g.add(b,v,k)
  else:
   a,v=u+1,u+2
   g.add(u,v,k+(2 if kind%3==1 else 1));g.add(u,a,k);g.add(a,v,k)
  u=v;kind+=1
 while u<n:g.add(u,u+1,g.r.randint(0,2000));u+=1
 g.fill(m,lambda:g.r.randint(99980,99999),2);return g

def build(group,index,sample=False):
 seed=SEED+index*1009+(1000003 if sample else 0)
 if group==1:return ordinary(100000,200000,seed,0,40,index==2 and not sample)
 if group==2:return ordinary(100000,200000,seed,99960,100000)
 if group==3:return tree(100000,seed)
 if group==4:return cycle(100000,seed)
 if group==5:
  a,b=[(99984,100000),(0,100000),(99994,100000),(0,17)][index%4]
  return two(100000,200000,seed,a,b)
 if group==6:return unique(100000,seed,index==14 and not sample)
 if group==7:
  maker=[lambda:ordinary(5000,10000,seed,0,100000),lambda:common(5000,10000,seed),lambda:ripple(5000,10000,seed),lambda:gadgets(5000,10000,seed),lambda:ordinary(5000,10000,seed,0,100000),lambda:gadgets(5000,10000,seed)]
  return maker[(index-17)%6]()
 return [common,ripple,gadgets][(index-23)%3](100000,200000,seed)

def properties(g,group):
 n=g.n;m=len(g.e);xs=list(g.e.values());x=max(xs);y=min(xs)
 assert n==(5000 if group==7 else 100000)
 assert m==(99999 if group==3 else 100000 if group==4 else 100001 if group==6 else 10000 if group==7 else 200000)
 assert max(xs)<=100000 and min(xs)>=0
 if group==1:assert x<=40
 if group==2:assert x-y<=40
 if group==5:assert len(set(xs))<=2
 if group==6:assert len(set(xs))==m
 p=list(range(n+1));sizes=[1]*(n+1);components=n
 def find(u):
  while p[u]!=u:p[u]=p[p[u]];u=p[u]
  return u
 for u,v in g.e:
  a,b=find(u),find(v)
  if a!=b:
   if sizes[a]<sizes[b]:a,b=b,a
   p[b]=a;sizes[a]+=sizes[b];components-=1
 if group in(3,4):assert components==1
 return dict(n=n,m=m,X=x,Y=y,distinct_exponents=len(set(xs)),components=components)

def bounded():
 resource.setrlimit(resource.RLIMIT_AS,(2300*1024**2,2300*1024**2))
 resource.setrlimit(resource.RLIMIT_CPU,(180,180))

def run_case(inp,ans,mode):
 stats=R/'tools/.timing'
 with inp.open('rb')as fi,ans.open('wb')as fo:
  subprocess.run(['/usr/bin/time','-f','%e %M','-o',str(stats),str(R/'tools/std')],stdin=fi,stdout=fo,check=True,timeout=60)
 seconds,kib=stats.read_text().split();result={'std_seconds':float(seconds),'std_kib':int(kib)}
 oracle=R/'tools/.oracle.out'
 with inp.open('rb')as fi,oracle.open('wb')as fo:
  start=time.monotonic();subprocess.run([str(R/'tools/oracle'),mode],stdin=fi,stdout=fo,check=True,timeout=200,preexec_fn=bounded)
  result['oracle_seconds']=round(time.monotonic()-start,3)
 for exe in ['official','public']:
  c=subprocess.run([str(R/'tools'/exe),str(inp),str(oracle),str(ans)],capture_output=True,timeout=30)
  assert c.returncode==0,(inp,exe,c.stderr.decode())
  c=subprocess.run([str(R/'tools'/exe),str(inp),str(ans),str(ans)],capture_output=True,timeout=30)
  assert c.returncode==0,(inp,exe,c.stderr.decode())
 result['oracle_mode']=mode
 result['sha256_in']=hashlib.sha256(inp.read_bytes()).hexdigest();result['sha256_ans']=hashlib.sha256(ans.read_bytes()).hexdigest()
 return result

if __name__=='__main__':
 verify=json.loads((R/'tools/verification.json').read_text());assert verify['passed']
 for key,path in [('std','GPT/classic.cpp'),('oracle','tools/oracle.cpp'),('official','data/chk/chk.cpp'),('public','down/checker.cpp')]:assert hashlib.sha256((R/path).read_bytes()).hexdigest()==verify[key+'_sha256']
 (R/'data').mkdir(exist_ok=True);(R/'down').mkdir(exist_ok=True)
 audit_path=R/'tools/data-audit.json';audit=json.loads(audit_path.read_text())if audit_path.exists()else{}
 # Inline samples have ordinary complete three-line answers.
 inline=[(4,[(1,4,2),(1,2,0),(2,3,0),(3,4,0)],1,4),(3,[(1,2,0),(2,3,0),(1,3,1)],1,3),(4,[(1,2,0),(3,4,1)],1,4)]
 sys.path.insert(0,str(R/'tools'));from model import encode,exact,value
 for i,(n,e,s,t)in enumerate(inline,1):
  inp=R/f'down/{i}.in';ans=R/f'down/{i}.ans';inp.write_text(encode(n,e,s,t));audit[f'down/{i}']=run_case(inp,ans,'big');assert value(n,e,s,t,ans.read_bytes())==exact(n,e,s,t)
 groups=[1]*3+[2]*2+[3]+[4]*2+[5]*4+[6]*4+[7]*6+[8]*3
 jobs=[(f'data/{i}',group,i,False)for i,group in enumerate(groups,1)]
 jobs +=[(f'down/{group+3}',group,[1,4,6,7,10,13,20,25][group-1],True)for group in range(1,9)]
 modes={1:'auto',2:'auto',3:'tree',4:'cycle',5:'two',6:'distinct',7:'big',8:'big'}
 for label,group,index,sample in jobs:
  if label in audit:print('Previously checked',label,flush=True);continue
  g=build(group,index,sample);info=properties(g,group);inp=R/(label+'.in');ans=R/(label+'.ans');g.write(inp)
  del g
  info.update(run_case(inp,ans,modes[group]));info['group']=group;audit[label]=info
  audit_path.write_text(json.dumps(audit,indent=2));print(label,info,flush=True)
 assert len(audit)==36
 print('All 25 formal cases and 11 samples checked by both independent SPJs.',flush=True)
