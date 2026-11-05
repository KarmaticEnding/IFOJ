#include <bits/stdc++.h>
using namespace std;using ll=long long;
const ll NEG=-(1LL<<60);
struct Node{array<int,14>go{};int fail=0;ll val=0;};
int main(){
#if !defined(LOCAL) && !defined(__TUACK__)
    if(!freopen("letter.in","r",stdin))return 1;
    if(!freopen("letter.out","w",stdout))return 1;
#endif
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int k;if(!(cin>>k))return 0;vector<Node>a(1);
    while(k--){string t;ll w;cin>>t>>w;int v=0;for(char c:t){int z=c-'a';if(!a[v].go[z]){a[v].go[z]=a.size();a.emplace_back();}v=a[v].go[z];}a[v].val+=w;}
    queue<int>que;for(int c=0;c<14;c++)if(a[0].go[c])que.push(a[0].go[c]);
    while(!que.empty()){int v=que.front();que.pop();a[v].val+=a[a[v].fail].val;for(int c=0;c<14;c++){int u=a[v].go[c];if(u){a[u].fail=a[a[v].fail].go[c];que.push(u);}else a[v].go[c]=a[a[v].fail].go[c];}}
    string s;cin>>s;vector<string>blocks(1);for(char c:s)if(c=='?')blocks.emplace_back();else blocks.back()+=c;
    int q=blocks.size()-1,V=a.size(),v=0;ll base=0;
    for(char c:blocks[0]){v=a[v].go[c-'a'];base+=a[v].val;}
    if(!q){cout<<base<<'\n';return 0;}
    vector<vector<array<int,14>>>to(q,vector<array<int,14>>(V));
    vector<vector<array<ll,14>>>gain(q,vector<array<ll,14>>(V));
    for(int j=0;j<q;j++){
        vector<int>end(V);vector<ll>cost(V);
        for(int u=0;u<V;u++){int z=u;ll w=0;for(char c:blocks[j+1]){z=a[z].go[c-'a'];w+=a[z].val;}end[u]=z;cost[u]=w;}
        for(int u=0;u<V;u++)for(int c=0;c<14;c++){int z=a[u].go[c];to[j][u][c]=end[z];gain[j][u][c]=a[z].val+cost[z];}
    }
    vector<ll>dp(size_t(1<<14)*V,NEG);dp[v]=base;ll ans=NEG;
    for(int mask=0;mask<(1<<14);mask++){
        int j=__builtin_popcount((unsigned)mask);if(j>q)continue;
        ll *src=dp.data()+size_t(mask)*V;
        if(j==q){for(int u=0;u<V;u++)ans=max(ans,src[u]);continue;}
        for(int u=0;u<V;u++)if(src[u]!=NEG){
            unsigned left=((1<<14)-1)^mask;
            while(left){int c=__builtin_ctz(left);left&=left-1;ll &dst=dp[size_t(mask|(1<<c))*V+to[j][u][c]];dst=max(dst,src[u]+gain[j][u][c]);}
        }
    }cout<<ans<<'\n';
}
