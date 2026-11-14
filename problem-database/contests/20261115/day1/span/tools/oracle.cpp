#include <bits/stdc++.h>
using namespace std;
struct Q{int l,r,x,id;};
int main(int argc,char**argv){
 ios::sync_with_stdio(false);cin.tie(nullptr);int n,m;if(!(cin>>n>>m))return 0;
 int K=n/2+1;vector<int>a(n+1);for(int i=1;i<=n;i++)cin>>a[i];
 vector<Q>q(m);for(int i=0;i<m;i++){cin>>q[i].l>>q[i].r>>q[i].x;q[i].id=i;}
 string mode=argc>1?argv[1]:"tree";vector<int>ans(m),f(K+1),g(K+1);
 if(mode=="brute"){
  for(auto t:q){fill(f.begin(),f.end(),0);fill(g.begin(),g.end(),0);for(int i=t.l;i<=t.r;i++){int k=a[i];if(k<=K){if(!f[k])f[k]=i;g[k]=i;}}int k=1;while(f[k]&&g[k]-f[k]+1>t.x)++k;ans[t.id]=k;}
 }else{
  vector<vector<int>>pos(K+1);vector<int>rank(n+1);
  for(int i=1;i<=n;i++)if(a[i]<=K){rank[i]=pos[a[i]].size();pos[a[i]].push_back(i);}
  int S=1;while(S<K)S*=2;vector<int>tree(2*S,n+1);for(int k=1;k<=K;k++)tree[S+k-1]=0;for(int i=S-1;i;i--)tree[i]=min(tree[2*i],tree[2*i+1]);
  auto update=[&](int k){if(mode=="scan")return;int value=f[k]<g[k]?pos[k][g[k]-1]-pos[k][f[k]]+1:0;int z=S+k-1;tree[z]=value;while(z>1){z/=2;int t=min(tree[z*2],tree[z*2+1]);if(tree[z]==t)break;tree[z]=t;}};
  auto addLeft=[&](int i){int k=a[i];if(k<=K){f[k]=rank[i];update(k);}};
  auto addRight=[&](int i){int k=a[i];if(k<=K){g[k]=rank[i]+1;update(k);}};
  auto delLeft=[&](int i){int k=a[i];if(k<=K){f[k]=rank[i]+1;update(k);}};
  auto delRight=[&](int i){int k=a[i];if(k<=K){g[k]=rank[i];update(k);}};
  int B=max(1,int(n/sqrt(double(max(m,1)))));
  sort(q.begin(),q.end(),[&](const Q&a,const Q&b){int A=(a.l-1)/B,Bb=(b.l-1)/B;if(A!=Bb)return A<Bb;return A&1?a.r>b.r:a.r<b.r;});
  int l=1,r=0;
  for(auto t:q){
   while(l>t.l)addLeft(--l);while(r<t.r)addRight(++r);while(l<t.l)delLeft(l++);while(r>t.r)delRight(r--);
   if(mode=="scan"){
    int k=1;while(f[k]<g[k]&&pos[k][g[k]-1]-pos[k][f[k]]+1>t.x)++k;ans[t.id]=k;
   }else{
    int z=1;while(z<S){if(tree[z*2]<=t.x)z*=2;else z=z*2+1;}ans[t.id]=z-S+1;
   }
  }
 }
 for(int x:ans)cout<<x<<'\n';
}
