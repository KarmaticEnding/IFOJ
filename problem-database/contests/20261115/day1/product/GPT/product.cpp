#include <bits/stdc++.h>
using namespace std;
using ll=long long;
const ll MOD=100000007;
int main(){
#if !defined(LOCAL) && !defined(__TUACK__)
    if(!freopen("product.in","r",stdin))return 1;
    if(!freopen("product.out","w",stdout))return 1;
#endif
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n;if(!(cin>>n))return 0;vector<ll>b(n),a(n);for(ll&x:b)cin>>x;
    ll left=1,right=1000000000,root=0;
    while(left<=right){ll mid=(left+right)/2;if(mid*mid<=b[0])root=mid,left=mid+1;else right=mid-1;}
    bool ok=root*root==b[0];ll low=root,high=root,ways=1;a[0]=root;
    for(int i=1;i<n&&ok;i++){
        if(b[i]==b[i-1]){a[i]=low;ways=ways*((high-low+1)%MOD)%MOD;}
        else if(b[i]>b[i-1]){if(b[i]%low)ok=false;else high=b[i]/low,a[i]=high;}
        else{if(b[i]%high)ok=false;else low=b[i]/high,a[i]=low;}
    }
    if(!ok){cout<<"-1\n-1\n";return 0;}
    cout<<ways<<'\n';for(int i=0;i<n;i++)cout<<a[i]<<(i+1==n?'\n':' ');
}
