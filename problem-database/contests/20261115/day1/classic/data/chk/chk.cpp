// Official SPJ: sorted adjacency, two normalized exact binary sums.
#include "testlib.h"
#include <vector>
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#if !defined(_WIN32)
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#endif
const int MOD=1000000007;
static int check(int argc,char**argv){
 registerTestlibCmd(argc,argv);int n=inf.readInt(1,100000,"n"),m=inf.readInt(0,200000,"m"),X=0;
 std::vector<std::vector<std::pair<int,int>>>g(n);
 for(int i=0;i<m;i++){int u=inf.readInt(1,n,"u")-1,v=inf.readInt(1,n,"v")-1,x=inf.readInt(0,100000,"x");g[u].push_back({v,x});g[v].push_back({u,x});X=std::max(X,x);}
 int s=inf.readInt(1,n,"s")-1,t=inf.readInt(1,n,"t")-1;for(auto &v:g)std::sort(v.begin(),v.end());
 std::vector<int>pow2(X+1,1);for(int i=1;i<=X;i++)pow2[i]=2LL*pow2[i-1]%MOD;
 auto read=[&](InStream&f,bool jury,int reported){
  TResult error=jury?_fail:_wa;int k=f.readInt(1,n,"path length");std::vector<unsigned char>seen(n);std::vector<int>bits(X+22);int previous=-1,sum=0;
  for(int i=0;i<k;i++){
   int u=f.readInt(1,n,"vertex")-1;if(seen[u])quitf(error,"path repeats a vertex");seen[u]=1;
   if(i==0&&u!=s)quitf(error,"wrong starting vertex");if(i+1==k&&u!=t)quitf(error,"wrong ending vertex");
   if(previous>=0){auto it=std::lower_bound(g[previous].begin(),g[previous].end(),std::make_pair(u,-1));if(it==g[previous].end()||it->first!=u)quitf(error,"path uses a nonexistent edge");bits[it->second]++;sum+=pow2[it->second];if(sum>=MOD)sum-=MOD;}
   previous=u;
  }
  if(sum!=reported)quitf(error,"reported residue differs from path length modulo %d",MOD);
  if(!f.seekEof())quitf(error,"extra output");
  for(size_t i=0;i+1<bits.size();i++){bits[i+1]+=bits[i]/2;bits[i]%=2;}return bits;
 };
 int expected=ans.readInt(-1,MOD-1,"distance");
 if(expected==-1){
  std::vector<int>q(1,s);std::vector<unsigned char>seen(n);seen[s]=1;for(size_t i=0;i<q.size();i++)for(auto e:g[q[i]])if(!seen[e.first]){seen[e.first]=1;q.push_back(e.first);}
  if(seen[t]||!ans.seekEof())quitf(_fail,"invalid unreachable jury answer");
  if(ouf.readInt(-1,MOD-1,"distance")!=-1||!ouf.seekEof())quitf(_wa,"expected a single -1");quitf(_ok,"unreachability verified");
 }
 auto exact=read(ans,true,expected);int reported=ouf.readInt(-1,MOD-1,"distance");if(reported!=expected)quitf(_wa,"wrong distance residue");
 auto actual=read(ouf,false,reported);if(actual!=exact)quitf(_wa,"path is not shortest: equal residues do not imply equal lengths");quitf(_ok,"exact shortest path verified");
}
int main(int argc,char**argv){
 if(argc!=7)return check(argc,argv);
#if !defined(_WIN32)
 disableFinalizeGuard();FILE*score=fopen(argv[5],"w");if(!score)return 3;double full=100;if(FILE*f=fopen(argv[4],"r")){if(fscanf(f,"%lf",&full)!=1)full=100;fclose(f);}else full=strtod(argv[4],nullptr);
 pid_t pid=fork();if(pid==0){int fd=open(argv[6],O_WRONLY|O_CREAT|O_TRUNC,0644);if(fd<0)_exit(3);dup2(fd,STDERR_FILENO);close(fd);char*args[]={argv[0],argv[1],argv[2],argv[3],nullptr};check(4,args);_exit(3);}
 int status=0;bool ok=pid>0&&waitpid(pid,&status,0)==pid&&WIFEXITED(status)&&WEXITSTATUS(status)==0;fprintf(score,"%.6f\n",ok?full:0.0);fclose(score);return 0;
#else
 return 3;
#endif
}
