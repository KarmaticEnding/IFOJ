#include <cstdio>
#include <vector>
using namespace std;
using int64 = long long;
constexpr int MOD = 993244853;

class FastIO {
    static constexpr int SIZE = 1 << 16;
    char input[SIZE], output[SIZE];
    int pos = 0, len = 0, used = 0;
public:
    ~FastIO() { flush(); }
    int get() {
        if (pos == len) {
            len = (int)fread(input, 1, SIZE, stdin); pos = 0;
            if (!len) return EOF;
        }
        return input[pos++];
    }
    int read() {
        int c, x = 0;
        do { c = get(); } while (c != EOF && c <= ' ');
        while (c >= '0' && c <= '9') { x = x * 10 + c - '0'; c = get(); }
        return x;
    }
    void flush() { if (used) fwrite(output, 1, used, stdout); used = 0; }
    void put(char c) { if (used == SIZE) flush(); output[used++] = c; }
    void write(int x) {
        char s[12]; int cnt = 0;
        do { s[cnt++] = char('0' + x % 10); x /= 10; } while (x);
        while (cnt) put(s[--cnt]);
        put('\n');
    }
};
int addmod(int a, int b) { int s = a + b; return s >= MOD ? s - MOD : s; }
struct Value {
    int s0 = 0, s1 = 0, s2 = 0;
    Value operator+(const Value &b) const {
        return {addmod(s0, b.s0), addmod(s1, b.s1), addmod(s2, b.s2)};
    }
};
struct Node {
    Value sum;
    int tag = 0, w1 = 0, w2 = 0;
};
class SegmentTree {
    vector<Node> tr;
    void pull(int p) { tr[p].sum = tr[p * 2].sum + tr[p * 2 + 1].sum; }
    void build(int p, int l, int r, FastIO &io) {
        if (l == r) {
            int a = io.read();
            tr[p].w1 = l; tr[p].w2 = int64(l) * l % MOD;
            tr[p].sum = {a, int(int64(a) * l % MOD), int(int64(a) * tr[p].w2 % MOD)};
            return;
        }
        int mid = (l + r) / 2;
        build(p * 2, l, mid, io); build(p * 2 + 1, mid + 1, r, io);
        tr[p].w1 = addmod(tr[p * 2].w1, tr[p * 2 + 1].w1);
        tr[p].w2 = addmod(tr[p * 2].w2, tr[p * 2 + 1].w2);
        pull(p);
    }
    void apply(int p, int len, int v) {
        Node &t = tr[p];
        t.sum.s0 = (t.sum.s0 + int64(v) * len) % MOD;
        t.sum.s1 = (t.sum.s1 + int64(v) * t.w1) % MOD;
        t.sum.s2 = (t.sum.s2 + int64(v) * t.w2) % MOD;
        t.tag = addmod(t.tag, v);
    }
    void push(int p, int l, int r) {
        if (!tr[p].tag) return;
        int mid = (l + r) / 2;
        apply(p * 2, mid - l + 1, tr[p].tag);
        apply(p * 2 + 1, r - mid, tr[p].tag);
        tr[p].tag = 0;
    }
    void change(int p, int l, int r, int ql, int qr, int v) {
        if (ql <= l && r <= qr) { apply(p, r - l + 1, v); return; }
        push(p, l, r);
        int mid = (l + r) / 2;
        if (ql <= mid) change(p * 2, l, mid, ql, qr, v);
        if (qr > mid) change(p * 2 + 1, mid + 1, r, ql, qr, v);
        pull(p);
    }
    Value query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tr[p].sum;
        push(p, l, r);
        int mid = (l + r) / 2;
        if (qr <= mid) return query(p * 2, l, mid, ql, qr);
        if (ql > mid) return query(p * 2 + 1, mid + 1, r, ql, qr);
        return query(p * 2, l, mid, ql, qr) + query(p * 2 + 1, mid + 1, r, ql, qr);
    }
    int n;
public:
    SegmentTree(int size, FastIO &io) : tr(4 * size + 4), n(size) { build(1, 1, n, io); }
    void change(int l, int r, int v) { change(1, 1, n, l, r, v); }
    int query(int l, int r) {
        Value v = query(1, 1, n, l, r);
        int64 c = int64(l - 1) * (r + 1) % MOD;
        int64 ans = (-v.s2 + int64(l + r) * v.s1 % MOD - c * v.s0 % MOD) % MOD;
        return int(ans < 0 ? ans + MOD : ans);
    }
};
int main() {
#if !defined(__TUACK__) && !defined(LOCAL)
    freopen("sub.in", "r", stdin);
    freopen("sub.out", "w", stdout);
#endif
    FastIO io;
    int n = io.read(), m = io.read();
    if (n < 1) return 0;
    SegmentTree tree(n, io);
    for (int i = 0; i < m; ++i) {
        int op = io.read(), l = io.read(), r = io.read();
        if (op == 1) tree.change(l, r, io.read());
        else io.write(tree.query(l, r));
    }
}
