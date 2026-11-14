// Public SPJ: edge hash table and signed carry cancellation, independent of the official SPJ.
#include "testlib.h"
#include <vector>
#include <unordered_map>
#include <cstdint>
const int P=1000000007;
static uint64_t key(int u,int v){if(u>v)std::swap(u,v);return(uint64_t(uint32_t(u))<<32)|uint32_t(v);}
int main(int argc,char**argv){
 registerTestlibCmd(argc,argv);int n=inf.readInt(1,100000,"n"),m=inf.readInt(0,200000,"m"),X=0;
 std::unordered_map<uint64_t,int>edges;edges.reserve(2*m+1);std::vector<std::vector<int>>neighbors(n);
 for(int i=0;i<m;i++){int u=inf.readInt(1,n,"u")-1,v=inf.readInt(1,n,"v")-1,x=inf.readInt(0,100000,"x");edges[key(u,v)]=x;neighbors[u].push_back(v);neighbors[v].push_back(u);X=std::max(X,x);}
 int s=inf.readInt(1,n,"s")-1,t=inf.readInt(1,n,"t")-1;std::vector<int>delta(X+23),power(X+1,1);for(int i=1;i<=X;i++)power[i]=2LL*power[i-1]%P;
 int reference=ans.readInt(-1,P-1,"distance"),reported=ouf.readInt(-1,P-1,"distance");
 if(reference<0){
  std::vector<int>todo(1,s);std::vector<bool>vis(n);vis[s]=true;for(size_t j=0;j<todo.size();j++)for(int v:neighbors[todo[j]])if(!vis[v]){vis[v]=true;todo.push_back(v);}
  if(vis[t]||!ans.seekEof())quitf(_fail,"reference incorrectly claims no route");if(reported!=-1||!ouf.seekEof())quitf(_wa,"disconnected instances require only -1");quitf(_ok,"no route exists");
 }
 if(reference!=reported)quitf(_wa,"distance residue must be %d",reference);
 auto consume=[&](InStream&stream,int sign,int claimed,bool referenceFile){
  TResult error=referenceFile?_fail:_wa;int count=stream.readInt(1,n,"number of vertices"),prev=-1,residue=0;std::vector<bool>used(n);
  for(int j=0;j<count;j++){
   int now=stream.readInt(1,n,"path vertex")-1;
   if(used[now]||(j==0&&now!=s)||(j+1==count&&now!=t))quitf(error,"invalid path endpoints or repeated vertex");used[now]=true;
   if(prev>=0){auto it=edges.find(key(prev,now));if(it==edges.end())quitf(error,"consecutive vertices are not adjacent");delta[it->second]+=sign;residue=(residue+power[it->second])%P;}prev=now;
  }
  if(residue!=claimed||!stream.seekEof())quitf(error,"incorrect path residue or trailing data");
 };
 consume(ans,-1,reference,true);consume(ouf,1,reported,false);
 // Equality is tested as a signed polynomial at 2, not through a modular hash.
 for(size_t i=0;i+1<delta.size();i++){if(delta[i]%2)quitf(_wa,"the submitted path has a different exact length");delta[i+1]+=delta[i]/2;}
 if(delta.back())quitf(_wa,"different exact length");quitf(_ok,"path length equals the exact optimum");
}
