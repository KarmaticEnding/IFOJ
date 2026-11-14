#include <bits/stdc++.h>
#include <boost/multiprecision/cpp_int.hpp>
using namespace std;using boost::multiprecision::cpp_int;using ull=unsigned long long;
const int MOD=1000000007;
struct E{int u,v,x;};
struct DSU{vector<int>p,sz;DSU(int n):p(n),sz(n,1){iota(p.begin(),p.end(),0);}int find(int x){return p[x]==x?x:p[x]=find(p[x]);}bool join(int a,int b){a=find(a);b=find(b);if(a==b)return false;if(sz[a]<sz[b])swap(a,b);p[b]=a;sz[a]+=sz[b];return true;}};
template<class Distance>class Heap{
 vector<int>h,where;vector<Distance>&d;
 bool less(int a,int b){return d[a]<d[b]||(d[a]==d[b]&&a<b);}
 void exchange(int i,int j){swap(h[i],h[j]);where[h[i]]=i;where[h[j]]=j;}
public:
 Heap(int n,vector<Distance>&D):where(n,-1),d(D){}
 bool empty()const{return h.empty();}
 void update(int v){int i=where[v];if(i<0){i=h.size();h.push_back(v);where[v]=i;}while(i&&less(h[i],h[(i-1)/2])){exchange(i,(i-1)/2);i=(i-1)/2;}}
 int pop(){int v=h[0];exchange(0,h.size()-1);h.pop_back();where[v]=-1;int i=0;while(2*i+1<int(h.size())){int j=2*i+1;if(j+1<int(h.size())&&less(h[j+1],h[j]))j++;if(!less(h[j],h[i]))break;exchange(i,j);i=j;}return v;}
};
int main(int argc,char**argv){
 ios::sync_with_stdio(false);cin.tie(nullptr);int n,m;if(!(cin>>n>>m))return 0;vector<E>edges(m);vector<vector<pair<int,int>>>g(n);int low=100001,high=0;set<int>exponents;
 for(int i=0;i<m;i++){auto&e=edges[i];cin>>e.u>>e.v>>e.x;--e.u;--e.v;g[e.u].push_back({e.v,i});g[e.v].push_back({e.u,i});low=min(low,e.x);high=max(high,e.x);exponents.insert(e.x);}
 int s,t;cin>>s>>t;--s;--t;string mode=argc>1?argv[1]:"auto";vector<int>par(n,-1),pe(n,-1),path;bool reachable=false;
 auto route=[&](const vector<vector<pair<int,int>>>&tree,int a,int b){vector<int>p(n,-1),queue(1,a);p[a]=a;for(size_t z=0;z<queue.size()&&p[b]<0;z++)for(auto e:tree[queue[z]])if(p[e.first]<0){p[e.first]=queue[z];queue.push_back(e.first);}vector<int>ans;if(p[b]<0)return ans;for(int v=b;;v=p[v]){ans.push_back(v);if(v==a)break;}reverse(ans.begin(),ans.end());return ans;};
 if(mode=="tree"||mode=="distinct"||mode=="cycle"){
  vector<vector<pair<int,int>>>tree(n);DSU dsu(n);vector<int>order(m);iota(order.begin(),order.end(),0);if(mode=="distinct")sort(order.begin(),order.end(),[&](int a,int b){return edges[a].x<edges[b].x;});vector<int>extra;
  for(int i:order){auto e=edges[i];if(dsu.join(e.u,e.v)){tree[e.u].push_back({e.v,i});tree[e.v].push_back({e.u,i});}else extra.push_back(i);}
  path=route(tree,s,t);reachable=!path.empty();
  if(mode=="cycle"&&reachable){
   assert(extra.size()==1);auto edge=edges[extra[0]];vector<vector<int>>candidates(1,path);
   for(int orientation=0;orientation<2;orientation++){int u=orientation?edge.v:edge.u,v=orientation?edge.u:edge.v;auto a=route(tree,s,u),b=route(tree,v,t);a.insert(a.end(),b.begin(),b.end());set<int>seen(a.begin(),a.end());if(seen.size()==a.size())candidates.push_back(a);}
   vector<unordered_map<int,int>>lookup(n);for(auto e:edges){lookup[e.u][e.v]=e.x;lookup[e.v][e.u]=e.x;}
   cpp_int best;bool have=false;for(auto candidate:candidates){cpp_int value=0;for(size_t j=1;j<candidate.size();j++)value+=cpp_int(1)<<lookup[candidate[j-1]][candidate[j]];if(!have||value<best){have=true;best=value;path=move(candidate);}}
  }
 }else if((mode=="auto"&&(!m||high-low<=40))||mode=="two"){
  vector<ull>d(n);vector<unsigned char>have(n),done(n);Heap<ull>heap(n,d);have[s]=1;d[s]=0;heap.update(s);
  bool wide=mode=="two"&&high-low>=0&&(high-low>=18||(1ULL<<(high-low))>(ull)n);
  while(!heap.empty()){int u=heap.pop();done[u]=1;if(u==t)break;for(auto item:g[u]){int v=item.first,i=item.second;if(!done[v]){ull w=wide?(edges[i].x==high?(ull)n+1:1):(1ULL<<(edges[i].x-low));ull z=d[u]+w;if(!have[v]||z<d[v]){d[v]=z;have[v]=1;par[v]=u;pe[v]=i;heap.update(v);}}}}
  reachable=done[t];
 }else{
  vector<cpp_int>d(n);vector<unsigned char>have(n),done(n);Heap<cpp_int>heap(n,d);have[s]=1;d[s]=0;heap.update(s);
  while(!heap.empty()){int u=heap.pop();done[u]=1;if(u==t)break;for(auto item:g[u]){int v=item.first,i=item.second;if(!done[v]){cpp_int value=d[u]+(cpp_int(1)<<edges[i].x);if(!have[v]||value<d[v]){d[v]=move(value);have[v]=1;par[v]=u;pe[v]=i;heap.update(v);}}}}
  reachable=done[t];
 }
 if(!reachable){cout<<-1<<'\n';return 0;}
 if(path.empty()){for(int v=t;v!=-1;v=par[v])path.push_back(v);reverse(path.begin(),path.end());}
 vector<int>pow2(high+1,1);for(int i=1;i<=high;i++)pow2[i]=2LL*pow2[i-1]%MOD;int answer=0;
 vector<unordered_map<int,int>>lookup(n);for(auto e:edges){lookup[e.u][e.v]=e.x;lookup[e.v][e.u]=e.x;}
 for(size_t j=1;j<path.size();j++){answer+=pow2[lookup[path[j-1]][path[j]]];if(answer>=MOD)answer-=MOD;}
 cout<<answer<<'\n'<<path.size()<<'\n';for(size_t j=0;j<path.size();j++)cout<<path[j]+1<<(j+1==path.size()?'\n':' ');
}
