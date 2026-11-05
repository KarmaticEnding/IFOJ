#include <bits/stdc++.h>
using namespace std;
const int P=998244353;
inline void add(int &x,int y){x+=y;if(x>=P)x-=P;}
int main(){
#if !defined(LOCAL) && !defined(__TUACK__)
    freopen("mex.in","r",stdin);freopen("mex.out","w",stdout);
#endif
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n,k;if(!(cin>>n>>k))return 0;
    vector<int>b(n);for(int &x:b)cin>>x;
    int W=n+1,lo=0,hi=0;vector<int> f(W);f[0]=1;
    // f[x-lo][d]: canonical partitions, weighted by (d-x)!.
    // x is the current MEX; d is the number of distinct values seen.
    for(int i=0;i<n;i++){
        int L=max(0,b[i]-k),R=min(i+1,b[i]+k);
        if(L>R){cout<<0<<'\n';return 0;}
        vector<int>g((R-L+1)*W);
        for(int x=max(lo,L);x<=min(hi,R);x++){
            int *src=&f[(x-lo)*W],*dst=&g[(x-L)*W];
            for(int d=x;d<=i;d++)if(src[d]){
                add(dst[d],int(1LL*src[d]*d%P));
                add(dst[d+1],int(1LL*src[d]*(d+1-x)%P));
            }
        }
        // Appending the missing x may advance MEX to any y in [x+1,d+1].
        // Weighted coefficients are 1, so sum over old x using a prefix sum.
        for(int d=0;d<=i;d++){
            int sum=0;
            for(int x=lo;x<=min({hi,L-2,d});x++)add(sum,f[(x-lo)*W+d]);
            for(int y=L;y<=min(R,d+1);y++){
                int x=y-1;
                if(x>=lo&&x<=hi&&x<=d)add(sum,f[(x-lo)*W+d]);
                add(g[(y-L)*W+d+1],sum);
            }
        }
        f.swap(g);lo=L;hi=R;
    }
    vector<vector<int>> C(n+1);for(int i=0;i<=n;i++){
        C[i].resize(i+1);C[i][0]=C[i][i]=1;
        for(int j=1;j<i;j++){C[i][j]=C[i-1][j-1];add(C[i][j],C[i-1][j]);}
    }
    int ans=0;
    for(int x=lo;x<=hi;x++)for(int d=x;d<=n;d++)
        add(ans,int(1LL*f[(x-lo)*W+d]*C[n-x][d-x]%P));
    cout<<ans<<'\n';
}
