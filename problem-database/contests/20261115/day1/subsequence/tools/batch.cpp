#define SUBSEQUENCE_NO_MAIN
#define ORACLE_NO_MAIN
#include "../GPT/subsequence.cpp"
#include "oracle.cpp"
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int cases; cin >> cases;
    while (cases--) {
        int k; string s, t; cin >> k >> s >> t;
        cout << solve(s, t, k) << ' ' << oracle(s, t, k) << '\n';
    }
}
