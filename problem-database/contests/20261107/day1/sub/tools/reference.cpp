// Independent oracle: four Fenwick trees over polynomially weighted differences.
// This program always uses standard input/output and is not a contestant solution.
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll P = 993244853;
ll norm(ll x) { x %= P; return x < 0 ? x + P : x; }
ll h(int k, ll x) {
    if (k == 0) return x % P;
    if (k == 1) return (x * (x + 1) / 2) % P;
    return (x * (x + 1) * (2 * x + 1) / 6) % P;
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m; if (!(cin >> n >> m)) return 0;
    vector<array<ll, 4>> bit(n + 1);
    ll previous = 0;
    auto weights = [&](int j, ll d) {
        return array<ll,4>{d, d * h(0,j-1) % P, d * h(1,j-1) % P, d * h(2,j-1) % P};
    };
    for (int i = 1; i <= n; ++i) {
        ll a; cin >> a;
        auto w = weights(i, norm(a - previous)); previous = a;
        for (int k=0;k<4;++k) bit[i][k] = (bit[i][k] + w[k]) % P;
        int p = i + (i & -i);
        if (p <= n) for (int k=0;k<4;++k) bit[p][k] = (bit[p][k]+bit[i][k])%P;
    }
    auto change = [&](int i, ll d) {
        if (i>n) return;
        auto w = weights(i, norm(d));
        for (; i<=n; i+=i&-i) for (int k=0;k<4;++k) bit[i][k]=(bit[i][k]+w[k])%P;
    };
    auto prefix = [&](int x) {
        array<ll,4> t{};
        for (int i=x;i;i-=i&-i) for(int k=0;k<4;++k) t[k]=(t[k]+bit[i][k])%P;
        array<ll,3> a{};
        for(int k=0;k<3;++k) a[k]=norm(h(k,x)*t[0]%P-t[k+1]);
        return a;
    };
    while (m--) {
        int op,l,r; cin>>op>>l>>r;
        if(op==1) { ll v; cin>>v; change(l,v); change(r+1,-v); }
        else {
            auto a=prefix(r),b=prefix(l-1);
            ll s0=norm(a[0]-b[0]),s1=norm(a[1]-b[1]),s2=norm(a[2]-b[2]);
            cout<<norm(-s2+(l+r)*s1%P-(ll(l-1)*(r+1)%P)*s0%P)<<'\n';
        }
    }
}
