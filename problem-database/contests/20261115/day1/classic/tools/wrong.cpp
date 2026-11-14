#include <bits/stdc++.h>
using namespace std;
const int P=1000000007;
struct E{int v,x;};
int main(int argc,char**argv){
 ios::sync_with_stdio(false);cin.tie(nullptr);string mode=argc>1?argv[1]:"log";int n,m;cin>>n>>m;vector<vector<E>>g(n);int X=0;
 for(int i=0;i<m;i++){int u,v,x;cin>>u>>v>>x;--u;--v;g[u].push_back({v,x});g[v].push_back({u,x});X=max(X,x);}int s,t;cin>>s>>t;--s;--t;
 vector<int>p(n,-1),px(n),pow2(X+1,1);for(int i=1;i<=X;i++)pow2[i]=2LL*pow2[i-1]%P;
 vector<long double>d(n,numeric_limits<long double>::infinity());vector<char>done(n);priority_queue<pair<long double,int>,vector<pair<long double,int>>,greater<pair<long double,int>>>q;
 d[s]=mode=="log"?-1e30L:0;q.push({d[s],s});
 while(!q.empty()){
  auto cur=q.top();q.pop();int u=cur.second;if(done[u]||cur.first!=d[u])continue;done[u]=1;if(u==t)break;
  for(auto e:g[u])if(!done[e.v]){long double z;
   if(mode=="log"){long double hi=max(d[u],(long double)e.x),lo=min(d[u],(long double)e.x);z=hi+log2l(1+exp2l(lo-hi));}
   else z=d[u]+pow2[e.x];
   if(z<d[e.v]){d[e.v]=z;p[e.v]=u;px[e.v]=e.x;q.push({z,e.v});}
  }
 }
 if(!done[t]){cout<<-1<<'\n';return 0;}vector<int>a;int ans=0;for(int u=t;u!=-1;u=p[u]){a.push_back(u+1);if(p[u]>=0){ans+=pow2[px[u]];if(ans>=P)ans-=P;}}
 reverse(a.begin(),a.end());cout<<ans<<'\n'<<a.size()<<'\n';for(int u:a)cout<<u<<' ';cout<<'\n';
}
