from pathlib import Path
import random,json,subprocess,time,hashlib,math,argparse,bisect
R=Path(__file__).resolve().parent
GROUPS=[(1,1,1000,1000,'general'),(2,3,8000,8000,'general'),(4,5,200000,5,'general'),(6,7,200000,20,'general'),(8,10,200000,200000,'fixed'),(11,12,200000,200000,'twice'),(13,16,40000,40000,'general'),(17,20,200000,200000,'general')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def make(n,m,kind,seed):
 rng=random.Random(seed)
 dense=(kind=='general'and m>=40000)
 if kind=='twice'or dense:
  core=(2*n//5 if n==40000 else 7*n//20)if dense else n//8;a=[0]*n;order=list(range(1,core+1));rng.shuffle(order)
  left=n//20 if dense else n//4-core//2
  second_start=n-n//20-core if dense else 3*n//4-core//2;right=second_start+core;a[left:left+core]=order
  second=[];size=max(1,core//(2+seed%4))
  for i in range(0,core,size):piece=order[i:i+size];rng.shuffle(piece);second.extend(piece)
  a[second_start:right]=second
  if dense:rest=[rng.randint(1,core)if rng.random()<.7 else rng.randint(core+1,n)for _ in range(n-2*core)]
  else:rest=[k for k in range(core+1,n//2+1)for _ in range(2)]
  rng.shuffle(rest);it=iter(rest)
  for i in range(n):
   if not a[i]:a[i]=next(it)
  p=[-1]*(core+1);gap=n
  for i,k in enumerate(a):
   if k<=core:
    if p[k]<0:p[k]=i
    else:gap=min(gap,i-p[k]+1)
  guarantee=second_start-left-core+1 if dense else gap-1;minlong=n//2
 else:
  chunks=8+seed%4;size=(n+chunks-1)//chunks;core=n//(chunks+3);a=[]
  for j in range(chunks):
   length=min(size,n-len(a))
   if not length:break
   block=list(range(1,core+1))
   while len(block)<length:
    block.append(rng.randint(1,core)if rng.random()<.48 else rng.randint(core+1,min(n,3*core)))
   rng.shuffle(block);a.extend(block)
  assert len(a)==n
  minlong=min(n,max(4*size,3*n//4));guarantee=max(1,size-2)
 occ=[[]for _ in range(core+1)]
 for i,k in enumerate(a):
  if k<=core:occ[k].append(i)
 fixedx=rng.randint(max(1,n//5),max(1,n//4))if kind=='fixed'else rng.randint(max(1,guarantee//3),max(1,guarantee))
 if kind=='fixed':minlong=min(n,max(minlong,fixedx+4*size+4))
 qs=[]
 for i in range(m):
  hard=i<max(2,int(.78*m))
  if (kind=='twice'or dense)and hard:
   l=rng.randint(1,left+1);r=rng.randint(right,n)
  else:
   length=minlong if hard else max(2,n//3)
   l=rng.randint(1,n-length+1);r=rng.randint(l+length-1,n)
  if kind=='fixed':x=fixedx
  elif hard:
   if kind=='twice'or dense:bound=guarantee
   else:
    first_full=(l-1+size-1)//size;last_full=r//size-1
    if r==n:last_full=(n-1)//size
    bound=max(1,(last_full-first_full-1)*size+1)
   x=rng.randint(max(1,2*bound//3),max(1,bound))
  elif i%2:x=rng.randint(1,r-l+1)
  else:
   k=rng.randint(1,core);v=occ[k];lo=bisect.bisect_left(v,l-1);hi=bisect.bisect_left(v,r)
   span=0 if lo==hi else v[hi-1]-v[lo]+1;x=max(1,min(n,span+rng.choice([-1,0,1])))
  qs.append((l,r,x))
 # Explicit long, high-answer witnesses even in the five-query tier.
 for i in range(min(2,m)):
  qs[i]=(1+i,n-i,fixedx if kind=='fixed'else max(1,guarantee//2))
 if m<=20:
  for i in range(2,m):
   l=1+(i-1)*(2*n//3)//max(1,m-2);r=min(n,l+rng.randint(n//3,2*n//3))
   qs[i]=(l,r,rng.randint(1,max(1,(r-l+1)//3)))
 rng.shuffle(qs)
 return a,qs,core
def encode(a,qs):return f'{len(a)} {len(qs)}\n'+' '.join(map(str,a))+'\n'+''.join(f'{l} {r} {x}\n'for l,r,x in qs)
def movement(n,qs):
 B=max(1,int(n/math.sqrt(len(qs))))
 sortedq=sorted(qs,key=lambda t:((t[0]-1)//B,-t[1]));perm=temp=0;lastblock=-1;r=n
 for l,R,x in sortedq:
  block=(l-1)//B
  if block!=lastblock:lastblock=block;r=n
  perm+=r-R;r=R;temp+=2*(l-(block*B+1))
 l=r=0;ordinary=0
 for L,R,x in sorted(qs,key=lambda t:((t[0]-1)//B,t[1]if((t[0]-1)//B)%2==0 else-t[1])):
  ordinary+=abs(L-l)+abs(R-r);l=L;r=R
 return {'block_length':B,'rollback_right_moves':perm,'rollback_temporary_moves':temp,'rollback_total_moves':perm+temp,'ordinary_total_moves':ordinary,'rollback_normalized':(perm+temp)/(n*math.sqrt(len(qs)))}
def save(folder,index,a,qs,group,core):
 _,_,N,M,kind=GROUPS[group-1];n=len(a);m=len(qs)
 assert n<=N and m<=M and all(1<=k<=n for k in a)
 assert all(1<=l<=r<=n and 1<=x<=n for l,r,x in qs)
 if kind=='fixed':assert len({x for l,r,x in qs})==1
 if kind=='twice':
  from collections import Counter
  assert max(Counter(a).values())<=2
 raw=encode(a,qs).encode();answers=[];timings=[]
 for mode in ['std','oracle']:
  start=time.monotonic();answers.append(subprocess.check_output([str(R/'tools'/mode)],input=raw,timeout=120));timings.append(time.monotonic()-start)
 assert answers[0]==answers[1],(folder,index)
 if n<=8000 or m<=20:
  brute=subprocess.check_output([str(R/'tools/oracle'),'brute'],input=raw,timeout=120);assert brute==answers[0]
 values=list(map(int,answers[0].split()));assert len(values)==m
 threshold=max(2,n//30);longlarge=sum(r-l+1>=n//2 and v>=threshold for(l,r,x),v in zip(qs,values))
 assert longlarge>=min(2,m),(folder,index,longlarge,threshold)
 moves=movement(n,qs);assert moves['rollback_normalized']>=.3,(folder,index,moves)
 p=R/folder/f'{index}.in';ans=p.with_suffix('.ans');assert not p.exists()and not ans.exists();p.write_bytes(raw);ans.write_bytes(answers[0])
 row={'input':str(p.relative_to(R)),'group':group,'n':n,'m':m,'kind':kind,'core':core,'answer_min':min(values),'answer_max':max(values),'answer_sum':sum(values),'long_large_count':longlarge,'large_threshold':threshold,'scan_interval_work':sum(r-l+1 for l,r,x in qs),'average_length_fraction':sum(r-l+1 for l,r,x in qs)/(n*m),'std_seconds':timings[0],'oracle_seconds':timings[1],'input_sha256':sha(p),'answer_sha256':sha(ans),**moves}
 print(row,flush=True);return row
if __name__=='__main__':
 gate=json.loads((R/'tools/verification.json').read_text());assert gate['passed']and gate['std_sha256']==sha(R/'GPT/span.cpp')and gate['oracle_sha256']==sha(R/'tools/oracle.cpp')
 parser=argparse.ArgumentParser();parser.add_argument('--probe',action='store_true');args=parser.parse_args()
 for d in ['data','down','probe']:(R/d).mkdir(exist_ok=True)
 if args.probe:
  rows=[]
  for i,g in enumerate([7,8],1):
   _,_,n,m,kind=GROUPS[g-1];a,qs,core=make(n,m,kind,2026111400+13 if g==7 else 2026111400+17);rows.append(save('probe',i,a,qs,g,core))
  (R/'tools/probe-manifest.json').write_text(json.dumps(rows,indent=2))
 else:
  rows=[]
  examples=[([1,2,1,2],[(1,4,1),(1,4,2),(1,4,3),(2,3,1)],[3,3,1,1]),([2,2,3],[(1,2,1),(2,2,1)],[1,1]),([1,2,3,1,2,3],[(1,6,3),(1,6,4),(2,5,1)],[4,1,1])]
  for idx,(a,qs,expected)in enumerate(examples,1):
   raw=encode(a,qs).encode();out=subprocess.check_output([str(R/'tools/std')],input=raw)
   assert list(map(int,out.split()))==expected
   assert out==subprocess.check_output([str(R/'tools/oracle'),'brute'],input=raw)
   p=R/'down'/f'{idx}.in';ans=p.with_suffix('.ans');assert not p.exists()and not ans.exists();p.write_bytes(raw);ans.write_bytes(out)
   rows.append({'input':str(p.relative_to(R)),'inline_sample':True,'n':len(a),'m':len(qs),'input_sha256':sha(p),'answer_sha256':sha(ans)})
  for g,(left,right,n,m,kind)in enumerate(GROUPS,1):
   for i in range(left,right+1):a,qs,core=make(n,m,kind,2026111400+i);rows.append(save('data',i,a,qs,g,core))
   a,qs,core=make(n,m,kind,2026112400+g);rows.append(save('down',g+3,a,qs,g,core))
  (R/'tools/data-manifest.json').write_text(json.dumps(rows,indent=2))
