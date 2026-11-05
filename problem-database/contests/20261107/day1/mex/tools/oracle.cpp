#include <bits/stdc++.h>
using namespace std;
const int P=998244353;
int pw(int a,int e){int r=1;for(;e;e>>=1,a=1LL*a*a%P)if(e&1)r=1LL*r*a%P;return r;}
void add(int& a,int b){a+=b;if(a>=P)a-=P;}
int main(int argc,char**argv){
 int n,k;cin>>n>>k;vector<int>b(n);for(int &x:b)cin>>x;
 if(argc>1&&string(argv[1])=="subset"){
  int lim=1<<(n+1);vector<int>f(lim),g(lim);f[0]=1;
  for(int i=0;i<n;i++){
   fill(g.begin(),g.end(),0);
   for(int s=0;s<lim;s++)if(f[s])for(int a=0;a<=n;a++){
    int t=s|(1<<a),x=0;while(t>>x&1)x++;
    if(abs(x-b[i])<=k)add(g[t],f[s]);
   }f.swap(g);
  }int r=0;for(int v:f)add(r,v);cout<<r<<'\n';return 0;
 }
 vector<int>fac(n+1),inv(n+1);fac[0]=1;for(int i=1;i<=n;i++)fac[i]=1LL*fac[i-1]*i%P;
 inv[n]=pw(fac[n],P-2);for(int i=n;i;i--)inv[i-1]=1LL*inv[i]*i%P;
 int lo=0,hi=0;vector<vector<int>>f(1,vector<int>(n+1));f[0][0]=1;
 for(int i=0;i<n;i++){
  int L=max(0,b[i]-k),R=min(i+1,b[i]+k);if(L>R){cout<<0<<'\n';return 0;}
  vector<vector<int>>g(R-L+1,vector<int>(n+1));
  // Independently maintain unweighted canonical counts (MEX, anonymous classes).
  for(int x=lo;x<=hi;x++)for(int j=0;j<=i-x;j++)if(f[x-lo][j]){
   int v=f[x-lo][j];
   if(x>=L&&x<=R){add(g[x-L][j],1LL*v*(x+j)%P);add(g[x-L][j+1],v);}
  }
  if(argc>1&&string(argv[1])=="slow"){
   for(int x=lo;x<=hi;x++)for(int j=0;j<=i-x;j++)if(f[x-lo][j])
    for(int y=max(L,x+1);y<=min(R,x+j+1);y++)
     add(g[y-L][j-y+x+1],1LL*f[x-lo][j]*fac[j]%P*inv[j-y+x+1]%P);
  }else{
   vector<int>diag(n+1);
   int at=lo;
   for(int y=L;y<=R;y++){
    while(at<=hi&&at<y){for(int j=0;j<=i-at;j++)add(diag[at+j],1LL*f[at-lo][j]*fac[j]%P);at++;}
    for(int h=max(0,1-y);h<=i+1-y;h++)add(g[y-L][h],1LL*diag[y+h-1]*inv[h]%P);
   }
  }f.swap(g);lo=L;hi=R;
 }
 int r=0;for(int x=lo;x<=hi;x++)for(int j=0;j<=n-x;j++)add(r,1LL*f[x-lo][j]*fac[n-x]%P*inv[n-x-j]%P);
 cout<<r<<'\n';
}
