from pathlib import Path
import subprocess,random,json,hashlib,tempfile,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'));from model import encode,exact,value,P
H='743822d8120213a3482f4a6e8b9846219b84218350be548a42bdfdb056fba9e3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(exe,n,e,s,t,*args):return subprocess.check_output([str(R/'tools'/exe),*args],input=encode(n,e,s,t).encode(),timeout=30)
if __name__=='__main__':
 assert sha(R/'down/testlib.h')==sha(R/'data/chk/testlib.h')==H
 for src,out,flags in [('GPT/classic.cpp','std',['-O2','-DLOCAL']),('tools/oracle.cpp','oracle',['-O2']),('GPT/classic.cpp','sanitized',['-O1','-DLOCAL','-fsanitize=undefined,bounds','-D_GLIBCXX_ASSERTIONS']),('tools/binary_test.cpp','binary_test',['-O2']),('data/chk/chk.cpp','official',['-O2']),('down/checker.cpp','public',['-O2'])]:subprocess.run(['g++','-std=c++14',*flags,str(R/src),'-o',str(R/'tools'/out)],check=True)
 subprocess.run([str(R/'tools/binary_test')],check=True)
 rng=random.Random(46420261114);cases=[(1,[],1,1),(2,[],1,2),(2,[(1,2,100000)],1,2),(3,[(1,2,0),(2,3,0),(1,3,1)],1,3),(4,[(1,4,2),(1,2,0),(2,3,0),(3,4,0)],1,4),(4,[(1,2,4),(2,3,5),(3,4,6)],1,4),(4,[(1,2,0),(3,4,1)],1,4)]
 for z in range(240):
  n=rng.randint(2,18);pairs=[(u,v)for u in range(1,n+1)for v in range(u+1,n+1)];rng.shuffle(pairs);m=rng.randint(0,len(pairs));e=[(u,v,rng.randint(0,160)if z%4 else rng.randint(99980,100000))for u,v in pairs[:m]];cases.append((n,e,rng.randint(1,n),rng.randint(1,n)))
 for i,(n,e,s,t)in enumerate(cases):
  expected=exact(n,e,s,t);assert value(n,e,s,t,run('std',n,e,s,t))==expected
  assert value(n,e,s,t,run('oracle',n,e,s,t,'big'))==expected
  if i<40:assert value(n,e,s,t,run('sanitized',n,e,s,t))==expected
 modes=0
 for z in range(80):
  n=rng.randint(3,20);tree=[(rng.randint(1,v-1),v,rng.randint(0,100000))for v in range(2,n+1)];s,t=rng.sample(range(1,n+1),2)
  assert value(n,tree,s,t,run('oracle',n,tree,s,t,'tree'))==exact(n,tree,s,t);modes+=1
  occupied={tuple(sorted((u,v)))for u,v,x in tree};other=[(u,v)for u in range(1,n+1)for v in range(u+1,n+1)if(u,v)not in occupied];u,v=rng.choice(other);cycle=tree+[(u,v,rng.randint(0,100000))]
  assert value(n,cycle,s,t,run('oracle',n,cycle,s,t,'cycle'))==exact(n,cycle,s,t);modes+=1
  unique=[(u,v,x)for (u,v,_),x in zip(cycle,rng.sample(range(100001),len(cycle)))];assert value(n,unique,s,t,run('oracle',n,unique,s,t,'distinct'))==exact(n,unique,s,t);modes+=1
  a,b=rng.sample(range(100001),2);two=[(u,v,rng.choice([a,b]))for u,v,x in cycle];assert value(n,two,s,t,run('oracle',n,two,s,t,'two'))==exact(n,two,s,t);modes+=1
 # Checker tests include different optimum paths with carries and a non-optimal
 # path whose distance is congruent to the optimum modulo P.
 spj=0
 with tempfile.TemporaryDirectory()as tmp:
  q=Path(tmp);inp=q/'input';ans=q/'answer';out=q/'output'
  n=3;e=[(1,2,0),(2,3,0),(1,3,1)];inp.write_text(encode(n,e,1,3));ans.write_text('2\n2\n1 3\n')
  tests=[(b'2\n3\n1 2 3\n',True),(b'2\n2\n1 3\n',True),(b'-1\n',False),(b'2\n4\n1 2 1 3\n',False),(b'2\n2\n1 2\n',False),(b'2\n2\n0 3\n',False),(b'2\n2\n1 3\n4\n',False),(b'',False)]
  for text,ok in tests:
   out.write_bytes(text)
   for exe in ['official','public']:r=subprocess.run([str(R/'tools'/exe),str(inp),str(out),str(ans)],capture_output=True);assert(r.returncode==0)==ok,(exe,text,r.stderr);spj+=1
  bits=[i for i in range(31)if(P+1)>>i&1];n=len(bits)+1;e=[(i+1,i+2,x)for i,x in enumerate(bits)]+[(1,n,0)];inp.write_text(encode(n,e,1,n));ans.write_text(f'1\n2\n1 {n}\n');out.write_text(f'1\n{n}\n'+' '.join(map(str,range(1,n+1)))+'\n')
  for exe in ['official','public']:assert subprocess.run([str(R/'tools'/exe),str(inp),str(out),str(ans)],capture_output=True).returncode!=0;spj+=1
  for n,e,s,t in [(1,[],1,1),(4,[(1,2,0),(3,4,1)],1,4)]:
   inp.write_text(encode(n,e,s,t));good=run('std',n,e,s,t);ans.write_bytes(good);out.write_bytes(good)
   for exe in ['official','public']:assert subprocess.run([str(R/'tools'/exe),str(inp),str(out),str(ans)],capture_output=True).returncode==0;spj+=1
  full=q/'full';score=q/'score';info=q/'info';full.write_text('4\n');subprocess.run([str(R/'tools/official'),str(inp),str(out),str(ans),str(full),str(score),str(info)],check=True);assert float(score.read_text())==4
  out.write_text('-1\n9\n');subprocess.run([str(R/'tools/official'),str(inp),str(out),str(ans),str(full),str(score),str(info)],check=True);assert float(score.read_text())==0
 subprocess.run(['g++','-O2','-std=c++14',str(R/'GPT/classic.cpp'),'-o',str(R/'tools/file-io')],check=True)
 with tempfile.TemporaryDirectory()as tmp:
  p=Path(tmp);p.joinpath('classic.in').write_text('3 3\n1 2 0\n2 3 0\n1 3 1\n1 3\n');subprocess.run([str(R/'tools/file-io')],cwd=tmp,check=True);assert value(3,[(1,2,0),(2,3,0),(1,3,1)],1,3,p.joinpath('classic.out').read_bytes())==2
 report={'passed':True,'graph_cases':len(cases),'special_oracle_cases':modes,'binary_random_versions':5000,'binary_comparisons':15000,'forked_long_carry_checks':2000,'sanitized_graphs':40,'spj_cases':spj,'tuack_adapter':True,'file_io':True,'std_sha256':sha(R/'GPT/classic.cpp'),'oracle_sha256':sha(R/'tools/oracle.cpp'),'official_sha256':sha(R/'data/chk/chk.cpp'),'public_sha256':sha(R/'down/checker.cpp'),'testlib_sha256':H}
 (R/'tools/verification.json').write_text(json.dumps(report,indent=2));print(report)
