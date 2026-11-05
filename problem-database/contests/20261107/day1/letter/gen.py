from pathlib import Path
import random,json,subprocess,time,hashlib
R=Path(__file__).resolve().parent
GROUPS=[(1,2,100,100,3,'none'),(3,4,400000,1000,0,'none'),(5,7,400000,1000,14,'separated'),(8,10,100,100,14,'none'),(11,12,400000,1000,14,'short'),(13,16,400000,1000,6,'none'),(17,20,400000,1000,14,'none')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def make(n,L,q,prop,seed):
 rng=random.Random(seed);letters='abcdefghijklmn';s=list(rng.choices(letters,k=n))
 # General cases vary dense and separated clusters; no separation promise is used.
 if prop=='separated':pos=sorted(rng.sample(range(1000,n-1000,1100),q))
 elif q:
  mode=seed%3;center=rng.randrange(max(1,n-3*q))
  if prop=='short' and mode==1:mode=2
  if mode==0:pos=list(range(center,center+q))
  elif mode==1:pos=[center+2*i for i in range(q)]
  else:
   a=q//2;b=q-a;center=min(center,n-q-10)
   pos=list(range(center,center+a))+list(range(n-b-1,n-1))
   if len(set(pos))<q:pos=list(range(q))
 else:pos=[]
 for i in pos:s[i]='?'
 it=iter(rng.sample(letters,q));w=''.join(next(it)if c=='?'else c for c in s)
 patterns=[];left=L
 # Mix alphabet coverage, suffix relationships, duplicate strings and mixed signs.
 for c in rng.sample(list(letters),min(14,L//4)):
  patterns.append((c,rng.randint(-1000000,1000000)));left-=1
 while left:
  if prop=='short':length=rng.randint(1,min(2,left))
  elif left>200 and seed%4==0 and len(patterns)<16:length=min(left,350)
  else:length=rng.randint(1,min(left,14 if n>100 else 8))
  if pos and rng.random()<.8:
   target=rng.choice(pos);start=max(0,min(n-length,target-rng.randrange(length)))
  else:start=rng.randrange(n-length+1)
  t=w[start:start+length]
  if patterns and rng.random()<.1 and len(patterns[-1][0])<=left and (prop!='short' or len(patterns[-1][0])<=2):t=patterns[-1][0]
  patterns.append((t,rng.randint(-1000000,1000000)));left-=len(t)
 assert sum(map(lambda x:len(x[0]),patterns))==L
 return patterns,''.join(s)
def encode(p,s):return str(len(p))+'\n'+''.join(f'{t} {w}\n'for t,w in p)+s+'\n'
def save(folder,index,p,s,group):
 left,right,n,L,q,prop=GROUPS[group-1]
 assert 1<=len(s)<=n and sum(len(t)for t,w in p)<=L and s.count('?')<=q
 assert set(s)<=set('abcdefghijklmn?') and 1<=len(p)<=1000
 assert all(1<=len(t)<=1000 and set(t)<=set('abcdefghijklmn') and -1000000<=w<=1000000 for t,w in p)
 positions=[i for i,c in enumerate(s)if c=='?'];M=max(len(t)for t,w in p)
 if prop=='separated':assert all(b-a>=M for a,b in zip(positions,positions[1:]))
 if prop=='short':assert M<=2
 raw=encode(p,s).encode();outs=[];times=[]
 for exe in ['std','oracle']:
  begin=time.monotonic();outs.append(subprocess.check_output([str(R/'tools'/exe)],input=raw,timeout=90));times.append(time.monotonic()-begin)
 assert outs[0]==outs[1],(folder,index)
 path=R/folder/f'{index}.in';ans=path.with_suffix('.ans');assert not path.exists()and not ans.exists();path.write_bytes(raw);ans.write_bytes(outs[0])
 row={'input':str(path.relative_to(R)),'group':group,'n':len(s),'L':sum(len(t)for t,w in p),'q':len(positions),'max_length':M,'answer':int(outs[0]),'std_seconds':times[0],'oracle_seconds':times[1],'input_sha256':sha(path),'answer_sha256':sha(ans)}
 print(row,flush=True);return row
if __name__=='__main__':
 gate=json.loads((R/'tools/verification.json').read_text());assert gate['passed']and gate['std_sha256']==sha(R/'GPT/letter.cpp')and gate['oracle_sha256']==sha(R/'tools/oracle.cpp')
 for d in ['data','down']:(R/d).mkdir(exist_ok=True)
 small=[([('abc',-10),('a',1),('b',1),('c',3)],'?b?'),([('a',1),('a',1)],'?'),([('a',-1)],'?'*14)]
 rows=[]
 for i,(p,s)in enumerate(small,1):rows.append(save('down',i,p,s,1 if i<3 else 4))
 for g,(a,b,n,L,q,prop)in enumerate(GROUPS,1):
  for i in range(a,b+1):p,s=make(n,L,q,prop,2026110700+i);rows.append(save('data',i,p,s,g))
  p,s=make(n,L,q,prop,2026111700+g);rows.append(save('down',g+3,p,s,g))
 (R/'tools/data-manifest.json').write_text(json.dumps(rows,indent=2))
