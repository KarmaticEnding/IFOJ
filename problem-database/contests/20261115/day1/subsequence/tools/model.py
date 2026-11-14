from itertools import product

def encode(s,t,k):return f'{len(s)} {k}\n{s}\n{t}\n'

def pairs(s,t):
 count=answer=0
 for c in s:
  if c==t[1]:answer+=count
  if c==t[0]:count+=1
 return answer

def exhaustive(s,t):
 # A third representative permits edits away from both target characters too.
 alphabet=set(s)|set(t)|{'a','b','c'}
 if len(alphabet)>3:
  neutral=next(c for c in 'abcdefghijklmnopqrstuvwxyz' if c not in t)
  s=''.join(c if c in t else neutral for c in s)
  alphabet=set(t)|{neutral}
 best=[-1]*(len(s)+1)
 for z in product(sorted(alphabet),repeat=len(s)):
  cost=sum(a!=b for a,b in zip(s,z));best[cost]=max(best[cost],pairs(z,t))
 for k in range(1,len(best)):best[k]=max(best[k],best[k-1])
 return best

def binary_only(s,t,k):
 if t[0]==t[1]:return pairs(s,t)
 a,b=t;B=s.count(b);pre_a=pre_b=0;ga=[];gb=[]
 for c in s:
  if c==a:ga.append(pre_a-(B-pre_b));pre_a+=1
  if c==b:pre_b+=1;gb.append((B-pre_b)-pre_a)
 ga.reverse();pa=[0];pb=[0]
 for v in ga:pa.append(pa[-1]+v)
 for v in gb:pb.append(pb[-1]+v)
 base=pairs(s,t);ans=base
 for x in range(min(k,len(gb))+1):
  for y in range(min(k-x,len(ga))+1):
   ans=max(ans,base+pb[x]+pa[y]-x*(x-1)//2-y*(y-1)//2+x*y)
 return ans

def greedy(s,t,k,reverse=False):
 if t[0]==t[1]:return min(len(s),s.count(t[0])+k)*(min(len(s),s.count(t[0])+k)-1)//2
 s=list(s);a,b=t;changed=set();total=pairs(s,t)
 for z in range(k):
  before=0;after=s.count(b);candidates=[]
  for i,c in enumerate(s):
   if c==b:after-=1
   if i not in changed:
    for ch in t:
     if c!=ch:
      gain=((ch==a)-(c==a))*after+((ch==b)-(c==b))*before
      candidates.append((gain,(-i if reverse else i),ch,i))
   if c==a:before+=1
  if not candidates:break
  gain,_,ch,i=max(candidates)
  if gain<=0:break
  total+=gain;s[i]=ch;changed.add(i)
 return total
