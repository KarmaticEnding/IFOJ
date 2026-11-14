import heapq
P=1000000007
def encode(n,edges,s,t):return f'{n} {len(edges)}\n'+''.join(f'{u} {v} {x}\n'for u,v,x in edges)+f'{s} {t}\n'
def exact(n,edges,s,t):
 g=[[]for _ in range(n+1)]
 for u,v,x in edges:g[u].append((v,1<<x));g[v].append((u,1<<x))
 d=[None]*(n+1);d[s]=0;heap=[(0,s)]
 while heap:
  value,u=heapq.heappop(heap)
  if d[u]!=value:continue
  if u==t:return value
  for v,w in g[u]:
   z=value+w
   if d[v]is None or z<d[v]:d[v]=z;heapq.heappush(heap,(z,v))
 return None
def value(n,edges,s,t,out):
 words=list(map(int,out.split()))
 if words==[-1]:return None
 assert len(words)>=3;reported,k=words[:2];path=words[2:];assert 1<=k<=n and len(path)==k and path[0]==s and path[-1]==t and len(set(path))==k
 lookup={tuple(sorted((u,v))):x for u,v,x in edges};counts={};residue=0
 for u,v in zip(path,path[1:]):
  x=lookup[tuple(sorted((u,v)))];counts[x]=counts.get(x,0)+1;residue=(residue+pow(2,x,P))%P
 assert residue==reported
 # Building one result integer is cheap even for a long path.
 total=0;carry=0
 for x in range(max(counts,default=0)+22):
  carry+=counts.get(x,0)
  if carry&1:total|=1<<x
  carry//=2
 assert not carry
 return total
