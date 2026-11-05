from pathlib import Path
import subprocess,json,random,itertools,hashlib,tempfile
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def encode(p,s):return str(len(p))+'\n'+''.join(f'{t} {w}\n'for t,w in p)+s+'\n'
def run(exe,p,s,*args):return int(subprocess.check_output([str(R/'tools'/exe),*args],input=encode(p,s).encode(),timeout=60))
def brute(p,s):
 q=s.count('?');best=-10**30
 for a in itertools.permutations('abcdefghijklmn',q):
  it=iter(a);z=''.join(next(it)if c=='?'else c for c in s)
  v=sum(w*sum(z[i:i+len(t)]==t for i in range(len(z)-len(t)+1))for t,w in p);best=max(best,v)
 return best
if __name__=='__main__':
 for src,out,flags in [('GPT/letter.cpp','std',['-O2','-DLOCAL']),('tools/oracle.cpp','oracle',['-O2']),('GPT/letter.cpp','sanitized',['-O1','-DLOCAL','-fsanitize=undefined,bounds','-D_GLIBCXX_ASSERTIONS'])]:
  subprocess.run(['g++','-std=c++14',*flags,str(R/src),'-o',str(R/'tools'/out)],check=True)
 rng=random.Random(13271107);count=0
 fixed=[([('abc',-10),('a',1),('b',1),('c',3)],'?b?',5),([('a',1),('a',1)],'?',2),([('a',1),('b',3),('ab',4)],'ab',8),([('a',-1)],'?'*13,0),([('a',-1)],'?'*14,-1),([('a',1000000)]*1000,'a'*400000,400000000000000),([('a',-1000000)]*1000,'a'*400000,-400000000000000)]
 for p,s,e in fixed:assert run('std',p,s)==e==run('oracle',p,s);count+=1
 for z in range(140):
  n=rng.randint(1,12);q=rng.randint(0,min(3,n));s=list(''.join(rng.choice('abcdefghijklmn')for _ in range(n)))
  for i in rng.sample(range(n),q):s[i]='?'
  s=''.join(s);p=[(''.join(rng.choice('abcde')for _ in range(rng.randint(1,5))),rng.randint(-20,20))for _ in range(rng.randint(1,8))]
  # Include patterns copied from a genuine distinct-letter completion.
  it=iter(rng.sample('abcdefghijklmn',q));w=''.join(next(it)if c=='?'else c for c in s)
  i=rng.randrange(n);p.append((w[i:min(n,i+rng.randint(1,5))],rng.randint(-20,20)))
  expected=brute(p,s);assert run('std',p,s)==expected==run('oracle',p,s,'direct'),(p,s,expected)
  if z<30:assert run('sanitized',p,s)==expected
  count+=1
 for z in range(30):
  n=rng.randint(10,40);q=rng.randint(4,7);s=list(''.join(rng.choice('abcd')for _ in range(n)))
  for i in rng.sample(range(n),q):s[i]='?'
  s=''.join(s);p=[(''.join(rng.choice('abcd')for _ in range(rng.randint(1,8))),rng.randint(-100,100))for _ in range(12)]
  assert run('std',p,s)==run('oracle',p,s,'direct');count+=1
 subprocess.run(['g++','-O2','-std=c++14',str(R/'GPT/letter.cpp'),'-o',str(R/'tools/file-io')],check=True)
 with tempfile.TemporaryDirectory()as tmp:
  p=Path(tmp);(p/'letter.in').write_text('2\na 1\na 1\n?\n');subprocess.run([str(R/'tools/file-io')],cwd=tmp,check=True);assert(p/'letter.out').read_text().strip()=='2'
 result={'passed':True,'cases':count,'brute_cases':140,'direct_character_dp':170,'sanitized':30,'file_io':True,'std_sha256':sha(R/'GPT/letter.cpp'),'oracle_sha256':sha(R/'tools/oracle.cpp')}
 (R/'tools/verification.json').write_text(json.dumps(result,indent=2));print(result)
