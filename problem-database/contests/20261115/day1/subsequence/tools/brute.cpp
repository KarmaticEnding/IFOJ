#include <bits/stdc++.h>
using namespace std;
int brute(const string& s, const string& t, int k) {
    int best = 0;
    function<void(int,int,int,int)> dfs = [&](int i, int edits, int count, int value) {
        if (edits > k) return;
        if (i == (int)s.size()) { best = max(best, value); return; }
        string options(1, s[i]);
        if (s[i] != t[0]) options += t[0];
        if (s[i] != t[1] && t[0] != t[1]) options += t[1];
        for (char c : options)
            dfs(i + 1, edits + (c != s[i]), count + (c == t[0]), value + (c == t[1] ? count : 0));
    };
    dfs(0, 0, 0, 0); return best;
}
int main() { int n,k; string s,t; cin>>n>>k>>s>>t; cout<<brute(s,t,k)<<'\n'; }
