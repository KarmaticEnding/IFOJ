from pathlib import Path
import subprocess,random,itertools,json,hashlib,tempfile
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def encode(a,queries):return f'{len(a)} {len(queries)}\n'+' '.join(map(str,a))+'\n'+''.join(f'{l} {r} {x}\n'for l,r,x in queries)
def run(exe,a,queries,*args):return list(map(int,subprocess.check_output([str(R/'tools'/exe),*args],input=encode(a,queries).encode(),timeout=40).split()))
def brute(a,qs):
 ans=[]
 for l,r,x in qs:
  first={};last={}
  for i in range(l-1,r):first.setdefault(a[i],i);last[a[i]]=i
  k=1
  while k in first and last[k]-first[k]+1>x:k+=1
  ans.append(k)
 return ans
if __name__=='__main__':
 for src,out,flags in [('GPT/span.cpp','std',['-O2','-DLOCAL']),('tools/oracle.cpp','oracle',['-O2']),('GPT/span.cpp','sanitized',['-O1','-g','-DLOCAL','-fsanitize=undefined,bounds','-D_GLIBCXX_ASSERTIONS'])]:subprocess.run(['g++','-std=c++14',*flags,str(R/src),'-o',str(R/'tools'/out)],check=True)
 tests=queries=0
 for n in range(1,6):
  qs=[(l,r,x)for l in range(1,n+1)for r in range(l,n+1)for x in range(1,n+2)]
  for a in itertools.product(range(1,4),repeat=n):
   expected=brute(a,qs);assert run('std',a,qs)==expected==run('oracle',a,qs)
   tests+=1;queries+=len(qs)
 rng=random.Random(20261115)
 for z in range(180):
  n=rng.randint(1,140);a=[rng.randint(1,n)for _ in range(n)]
  if z%3==0:
   a=[1+i%max(1,n//5)for i in range(n)];rng.shuffle(a)
  qs=[]
  for _ in range(rng.randint(1,220)):
   l=rng.randint(1,n);r=rng.randint(l,n);qs.append((l,r,rng.randint(1,n)))
  rng.shuffle(qs);e=brute(a,qs)
  assert run('std',a,qs)==e==run('oracle',a,qs)==run('oracle',a,qs,'scan')
  if z<40:assert run('sanitized',a,qs)==e
  tests+=1;queries+=len(qs)
 # Endpoint rollbacks, disappearing values, span=0/1 and long answer prefixes.
 a=list(range(1,65))*4
 qs=[(l,r,x)for l,r in [(1,256),(33,224),(65,192),(127,130),(256,256),(1,1)]for x in [1,64,65,128,256]]
 assert run('std',a,qs)==brute(a,qs)==run('oracle',a,qs)
 subprocess.run(['g++','-O2','-std=c++14',str(R/'GPT/span.cpp'),'-o',str(R/'tools/file-io')],check=True)
 with tempfile.TemporaryDirectory()as tmp:
  p=Path(tmp);(p/'span.in').write_text('4 3\n1 2 1 2\n1 4 1\n2 3 1\n1 4 3\n');subprocess.run([str(R/'tools/file-io')],cwd=tmp,check=True);assert list(map(int,(p/'span.out').read_text().split()))==[3,1,1]
 report={'passed':True,'array_cases':tests+1,'query_cases':queries+len(qs),'sanitized_arrays':40,'file_io':True,'std_sha256':sha(R/'GPT/span.cpp'),'oracle_sha256':sha(R/'tools/oracle.cpp')}
 (R/'tools/verification.json').write_text(json.dumps(report,indent=2));print(report)
