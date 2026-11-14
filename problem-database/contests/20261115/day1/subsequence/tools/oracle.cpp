// Independent oracle: scan right-to-left, minimizing edits for each pair count.
#include <bits/stdc++.h>
using namespace std;

int oracle(const string& s, const string& t, int budget) {
    const int n = s.size(), INF = n + 1;
    if (t[0] == t[1]) {
        vector<int> dp(n + 1, INF), next(n + 1, INF);
        dp[0] = 0;
        for (int i = 0; i < n; ++i) {
            fill(next.begin(), next.end(), INF);
            for (int c = 0; c <= i; ++c) {
                next[c] = min(next[c], dp[c] + (s[i] == t[0]));
                next[c + 1] = min(next[c + 1], dp[c] + (s[i] != t[0]));
            }
            dp.swap(next);
        }
        int result = 0;
        for (int c = 0; c <= n; ++c)
            if (dp[c] <= budget) result = max(result, c * (c - 1) / 2);
        return result;
    }

    const int width = n * n / 4 + 1;
    vector<short> dp((n + 1) * width, INF), next(dp.size(), INF);
    dp[0] = 0;
    for (int done = 0; done < n; ++done) {
        fill(next.begin(), next.end(), INF);
        char original = s[n - 1 - done];
        for (int right_b = 0; right_b <= done; ++right_b) {
            int row = right_b * width;
            for (int pairs = 0; pairs <= right_b * (done - right_b); ++pairs) {
                int cost = dp[row + pairs];
                if (cost > budget) continue;
                auto update = [&](int b, int v, int extra) {
                    int z = cost + extra;
                    if (z <= budget) {
                        short& dst = next[b * width + v];
                        dst = min<int>(dst, z);
                    }
                };
                update(right_b, pairs, original == t[0] || original == t[1]);
                update(right_b, pairs + right_b, original != t[0]);
                update(right_b + 1, pairs, original != t[1]);
            }
        }
        dp.swap(next);
    }
    for (int pairs = width - 1; pairs >= 0; --pairs)
        for (int b = 0; b <= n; ++b)
            if (dp[b * width + pairs] <= budget) return pairs;
    return 0;
}

#ifndef ORACLE_NO_MAIN
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, k; string s, t;
    cin >> n >> k >> s >> t;
    cout << oracle(s, t, k) << '\n';
}
#endif
