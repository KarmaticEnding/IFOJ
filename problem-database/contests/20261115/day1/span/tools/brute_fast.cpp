#include <bits/stdc++.h>
using namespace std;
// Stronger quadratic baseline: global answer cap, branch-free min updates,
// and one dummy slot for irrelevant large labels.
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,m;cin>>n>>m;vector<int>a(n+1),ct(n+2);for(int i=1;i<=n;i++){cin>>a[i];ct[a[i]]++;}int K=1;while(ct[K]>=2)K++;for(int&i:a)i=min(i,K+1);vector<int>f(K+2),g(K+2);while(m--){int l,r,x;cin>>l>>r>>x;fill(f.begin(),f.end(),n+1);fill(g.begin(),g.end(),0);for(int p=l;p<=r;p++){int k=a[p];f[k]=min(f[k],p);g[k]=p;}int k=1;while(g[k]&&g[k]-f[k]+1>x)k++;cout<<k<<'\n';}}
