from pathlib import Path
import random,json,hashlib,subprocess,time,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from model import encode,pairs,binary_only,greedy
SEED=202611141409
GROUPS=[1]*2+[2]*2+[3]*3+[4]*2+[5]*4+[6]*7
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(exe,s,t,k):return int(subprocess.check_output([str(R/'tools'/exe)],input=encode(s,t,k).encode(),timeout=20))
def saturation(s,t):
 if t[0]==t[1]:return len(s)-s.count(t[0])
 n=len(s);return min(sum(c!=(t[0]if i<p else t[1])for i,c in enumerate(s))for p in {n//2,(n+1)//2})
def raw(group,index,r,attempt):
 if group==1:return ''.join(r.choices('abc',k=12)),'ab',4 if index%2 else 6
 if group in(2,3):
  s=''.join(r.choices('abcde',weights=[3,3,1,1,1],k=200))
  return s,'ab',group-1
 if group==4:
  count=50 if index%2==0 else 120
  s=list('a'*count+''.join(r.choices('bcdef',k=200-count)));r.shuffle(s)
  return ''.join(s),'aa',70 if count==50 else 35
 if group==5:
  q=(index-10)%4
  if q==0:s='b'*100+'a'*100;k=60
  elif q==1:s=''.join(r.choices('ab',k=200));k=35
  elif q==2:s='ab'*100;k=50
  else:
   s=''
   while len(s)<200:s+=r.choice('ab')*r.randint(1,14)
   s=s[:200];k=75
  return s,'ab',min(k,saturation(s,'ab')-1)
 q=(index-14)%7
 if q==0:s='b'*70+'c'*60+'a'*70;k=110
 elif q==1:s=''.join(r.choices('abc',k=200));k=110
 elif q==2:s='bcaa'*50;k=90
 elif q==3:s='a'*30+'c'*80+'b'*60+'a'*30;k=40
 elif q==4:s='c'*10+''.join(r.choices('ab',k=180))+'c'*10;k=9
 elif q==5:s=''.join(r.choices('abcde',weights=[3,3,1,1,1],k=200));k=70
 else:s=''.join(r.choices('abcd',k=200));k=saturation(s,'ab')-1
 if attempt and q in(0,1,2):
  s=''.join(r.choices('abc',k=200));k=r.randint(90,120)
 return s,'ab',k
def build(group,index,sample=False):
 r=random.Random(SEED+index*1009+(1000003 if sample else 0))
 for attempt in range(400):
  s,t,k=raw(group,index,r,attempt)
  if not(0<=k<=len(s)):continue
  if group!=4 and (len(set(s))<(2 if group==5 else 3)or not all(c in s for c in t)):continue
  if group==6 and not(2<k<saturation(s,t)):continue
  ans=run('std',s,t,k)
  if group==6:
   if ans<=binary_only(s,t,k):continue
   if (index-14)%7 in(0,1,2,6)and ans<=max(greedy(s,t,k),greedy(s,t,k,True)):continue
  # Randomly rename every letter; none of the algorithms may assume t='ab'.
  letters=list('abcdefghijklmnopqrstuvwxyz');r.shuffle(letters);mapping=dict(zip('abcdef',letters))
  return ''.join(mapping[c]for c in s),''.join(mapping[c]for c in t),k,attempt+1
 raise AssertionError(('No suitable counterexample',group,index,sample))
def validate(s,t,k,group):
 assert 2<=len(s)<=200 and len(t)==2 and all('a'<=c<='z'for c in s+t)
 assert 0<=k<=len(s)
 assert len(s)==(12 if group==1 else 200)
 if group==2:assert k==1
 if group==3:assert k==2
 if group==4:assert t[0]==t[1]
 if group==5:assert t[0]!=t[1]and set(s)==set(t)
 if group==6:assert t[0]!=t[1]and len(set(s))>=3 and 2<k<saturation(s,t)

def output_case(label,s,t,k,group=None,attempts=1):
 if group:validate(s,t,k,group)
 inp=R/(label+'.in');ans=R/(label+'.ans');inp.write_text(encode(s,t,k))
 timing=R/'tools/.timing'
 with inp.open('rb')as fi,ans.open('wb')as fo:
  subprocess.run(['/usr/bin/time','-f','%e %M','-o',str(timing),str(R/'tools/std')],stdin=fi,stdout=fo,check=True,timeout=20)
 answer=int(ans.read_text());start=time.monotonic();independent=run('oracle',s,t,k);assert answer==independent,(label,answer,independent)
 seconds,kib=timing.read_text().split()
 extra={}
 if len(s)<=12:assert answer==run('brute',s,t,k);extra['brute']=True
 if k<=2:assert answer==run('small_k',s,t,k);extra['small_k_enumeration']=True
 if t[0]!=t[1]and set(s)<=set(t):assert answer==binary_only(s,t,k);extra['binary_formula']=True
 row={'group':group,'n':len(s),'k':k,'t':t,'alphabet_size':len(set(s)),'target_counts':[s.count(c)for c in t],'edits_for_theoretical_maximum':saturation(s,t),'original_pairs':pairs(s,t),'answer':answer,'std_seconds':float(seconds),'std_kib':int(kib),'oracle_seconds':round(time.monotonic()-start,4),'selection_attempts':attempts,'independent_checks':extra,'sha256_in':sha(inp),'sha256_ans':sha(ans)}
 if t[0]!=t[1]:row.update(binary_only_answer=binary_only(s,t,k),greedy_right_tie=greedy(s,t,k),greedy_left_tie=greedy(s,t,k,True))
 return row

if __name__=='__main__':
 verification=json.loads((R/'tools/verification.json').read_text());assert verification['passed']
 for key,path in [('std','GPT/subsequence.cpp'),('oracle','tools/oracle.cpp'),('brute','tools/brute.cpp')]:assert sha(R/path)==verification[key+'_sha256']
 subprocess.run(['g++','-O2','-std=c++14',str(R/'tools/small_k.cpp'),'-o',str(R/'tools/small_k')],check=True)
 (R/'data').mkdir(exist_ok=True);(R/'down').mkdir(exist_ok=True)
 p=R/'tools/data-audit.json';audit=json.loads(p.read_text())if p.exists()else{}
 inline=[('bbaa','ab',2),('asddsaf','sd',3),('abacaba','aa',2)]
 for i,(s,t,k)in enumerate(inline,1):audit[f'down/{i}']=output_case(f'down/{i}',s,t,k)
 jobs=[(f'data/{i}',g,i,False)for i,g in enumerate(GROUPS,1)]+[(f'down/{g+3}',g,[1,3,5,8,11,15][g-1],True)for g in range(1,7)]
 for label,group,index,sample in jobs:
  if label in audit:
   assert sha(R/(label+'.in'))==audit[label]['sha256_in']and sha(R/(label+'.ans'))==audit[label]['sha256_ans'];continue
  s,t,k,attempts=build(group,index,sample);audit[label]=output_case(label,s,t,k,group,attempts)
  p.write_text(json.dumps(audit,indent=2));print(label,audit[label],flush=True)
 assert len(audit)==29
 full=[audit[f'data/{i}']for i in range(14,21)]
 assert all(v['answer']>v['binary_only_answer']for v in full)
 assert sum(v['answer']>max(v['greedy_right_tie'],v['greedy_left_tie'])for v in full)>=4
 print('20 formal cases and 9 public samples independently checked.',flush=True)
