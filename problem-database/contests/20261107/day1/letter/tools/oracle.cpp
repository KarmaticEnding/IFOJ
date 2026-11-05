#include <bits/stdc++.h>
using namespace std;using ll=long long;const ll BAD=-(1LL<<60);
int main(int argc,char**argv){
 int k;cin>>k;vector<string>pat(k);vector<ll>w(k);set<string>words={""};
 for(int i=0;i<k;i++){cin>>pat[i]>>w[i];for(int j=1;j<=int(pat[i].size());j++)words.insert(pat[i].substr(0,j));}
 string s;cin>>s;vector<string>str(words.begin(),words.end());int V=str.size();unordered_map<string,int>id;for(int i=0;i<V;i++)id[str[i]]=i;
 vector<array<int,14>>go(V);vector<ll>val(V);
 for(int u=0;u<V;u++){
  for(int i=0;i<k;i++)if(str[u].size()>=pat[i].size()&&str[u].compare(str[u].size()-pat[i].size(),pat[i].size(),pat[i])==0)val[u]+=w[i];
  for(int c=0;c<14;c++){string z=str[u]+char('a'+c);while(!id.count(z))z.erase(z.begin());go[u][c]=id[z];}
 }
 int q=count(s.begin(),s.end(),'?');
 if(argc>1&&string(argv[1])=="direct"){
  unordered_map<int,ll>f,g;f[0]=0;
  for(char ch:s){g.clear();for(auto it:f){int mask=it.first/V,u=it.first%V;int begin=ch=='?'?0:ch-'a',end=ch=='?'?14:begin+1;for(int c=begin;c<end;c++)if(ch!='?'||!(mask>>c&1)){int m=ch=='?'?mask|(1<<c):mask;int z=go[u][c],key=m*V+z;ll v=it.second+val[z];auto p=g.find(key);if(p==g.end())g[key]=v;else p->second=max(p->second,v);}}f.swap(g);}
  ll ans=BAD;for(auto it:f)ans=max(ans,it.second);cout<<ans<<'\n';return 0;
 }
 vector<string>b(1);for(char c:s)if(c=='?')b.emplace_back();else b.back()+=c;
 int start=0;ll base=0;for(char c:b[0]){start=go[start][c-'a'];base+=val[start];}
 vector<vector<int>>dest(q,vector<int>(V));vector<vector<ll>>cost(q,vector<ll>(V));
 for(int j=0;j<q;j++){
  iota(dest[j].begin(),dest[j].end(),0);
  // Compose a fixed block character by character for every starting state.
  for(char c:b[j+1])for(int u=0;u<V;u++){int z=go[dest[j][u]][c-'a'];dest[j][u]=z;cost[j][u]+=val[z];}
 }
 vector<ll>d(size_t(1<<14)*V,BAD);
 for(int mask=(1<<14)-1;mask>=0;mask--){int j=__builtin_popcount((unsigned)mask);if(j>q)continue;
  for(int u=0;u<V;u++){
   ll &x=d[size_t(mask)*V+u];if(j==q){x=0;continue;}
   for(int c=0;c<14;c++)if(!(mask>>c&1)){int z=go[u][c];ll tail=d[size_t(mask|(1<<c))*V+dest[j][z]];if(tail!=BAD)x=max(x,val[z]+cost[j][z]+tail);}
  }
 }cout<<base+d[start]<<'\n';
}
