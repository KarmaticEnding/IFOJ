#include <bits/stdc++.h>
using namespace std;

int solve(const string& s, const string& t, int budget) {
    const int n = s.size();
    if (t[0] == t[1]) {
        int count = std::count(s.begin(), s.end(), t[0]);
        count = min(n, count + budget);
        return count * (count - 1) / 2;
    }

    const int width = n + 1;
    vector<int> dp((budget + 1) * width, -1), next(dp.size());
    dp[0] = 0;
    for (int i = 0; i < n; ++i) {
        fill(next.begin(), next.end(), -1);
        string choices(1, s[i]);
        if (s[i] != t[0]) choices += t[0];
        if (s[i] != t[1]) choices += t[1];
        for (int used = 0; used <= min(i, budget); ++used) {
            for (int count = 0; count <= i; ++count) {
                int value = dp[used * width + count];
                if (value < 0) continue;
                for (char c : choices) {
                    int cost = used + (c != s[i]);
                    if (cost > budget) continue;
                    int nc = count + (c == t[0]);
                    int nv = value + (c == t[1] ? count : 0);
                    int& dst = next[cost * width + nc];
                    dst = max(dst, nv);
                }
            }
        }
        dp.swap(next);
    }
    return *max_element(dp.begin(), dp.end());
}

#ifndef SUBSEQUENCE_NO_MAIN
int main() {
#if !defined(LOCAL) && !defined(__TUACK__)
    if (!freopen("subsequence.in", "r", stdin)) return 1;
    if (!freopen("subsequence.out", "w", stdout)) return 1;
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    string s, t;
    if (!(cin >> n >> k >> s >> t)) return 0;
    cout << solve(s, t, k) << '\n';
}
#endif
