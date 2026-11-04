#include <cstdio>
namespace FastIn
{
	const int S = 4e6 + 7;
	char *p1, *p2, buf[S];
	#define gc() (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, S, stdin), p1 == p2) ? EOF : *p1++)
	inline void read(int &x)
	{
		x = 0;
		char c = gc();
		while (c < '0' || c > '9')
			c = gc();
		for (; c >= '0' && c <= '9'; c = gc())
			x = (x << 3) + (x << 1) + (c & 15);
	}
	#undef gc
}
using FastIn::read;
const int MAXN = 1e6 + 7, mod = 993244853;
inline int M(const int x) { return x >= mod ? x - mod : x; }
inline int S1(const int l, const int r) { return ((long long)(l + r) * (r - l + 1) >> 1) % mod; }
inline int S2(const int x) { return ((long long)(x) * (x + 1) * ((x << 1) | 1) / 6) % mod; }
inline int S2(const int l, const int r) { return M(S2(r) + mod - S2(l - 1)); }
int n, m, a[MAXN];
namespace SgT
{
	struct SgTNode
	{
		int s[3], tag;
		inline void apltag(const int l, const int r, const int tg)
		{
			tag = M(tag + tg),
			s[0] = (s[0] + (long long)(r - l + 1) * tg) % mod,
			s[1] = (s[1] + (long long)(S1(l, r)) * tg) % mod,
			s[2] = (s[2] + (long long)(S2(l, r)) * tg) % mod; 
		}
		inline SgTNode operator+(const SgTNode &rhs) const
		{
			SgTNode res; res.tag = 0;
			res.s[0] = M(s[0] + rhs.s[0]),
			res.s[1] = M(s[1] + rhs.s[1]),
			res.s[2] = M(s[2] + rhs.s[2]);
			return res;
		}
	} tr[MAXN << 2];
	#define ls rt << 1
	#define rs (rt << 1) | 1
	#define lson l, mid, rt << 1
	#define rson mid + 1, r, (rt << 1) | 1
	inline void pushdown(const int l, const int r, const int rt)
	{
		int mid = (l + r) >> 1;
		if (tr[rt].tag)
			tr[ls].apltag(l, mid, tr[rt].tag),
			tr[rs].apltag(mid + 1, r, tr[rt].tag),
			tr[rt].tag = 0;
	}
	void build(const int l, const int r, const int rt)
	{
		if (l == r)
		{
			tr[rt].s[0] = a[l],
			tr[rt].s[1] = (long long)(l) * a[l] % mod,
			tr[rt].s[2] = (long long)(l) * l % mod * a[l] % mod;
			return;
		}
		int mid = (l + r) >> 1;
		build(lson), build(rson), tr[rt] = tr[ls] + tr[rs];
	}
	void update(const int L, const int R, const int val, const int l, const int r, const int rt)
	{
		if (L <= l && r <= R)
			return tr[rt].apltag(l, r, val);
		int mid = (l + r) >> 1;
		pushdown(l, r, rt);
		if (L <= mid)
			update(L, R, val, lson);
		if (R > mid)
			update(L, R, val, rson);
		tr[rt] = tr[ls] + tr[rs];
	}
	SgTNode query(const int L, const int R, const int l, const int r, const int rt)
	{
		if (L <= l && r <= R)
			return tr[rt];
		int mid = (l + r) >> 1;
		pushdown(l, r, rt);
		if (R <= mid)
			return query(L, R, lson);
		else if (L > mid)
			return query(L, R, rson);
		else
			return query(L, R, lson) + query(L, R, rson);
	}
	inline int query(const int l, const int r) { SgTNode res = query(l, r, 1, n, 1); return ((-res.s[2] + (long long)(l + r) * res.s[1] - (long long)(l - 1) * (r + 1) % mod * res.s[0]) % mod + mod) % mod; }
	#undef ls
	#undef rs
	#undef lson
	#undef rson
}
int main()
{
	read(n), read(m);
	for (int i = 1; i <= n; ++i)
		read(a[i]);
	SgT::build(1, n, 1);
	for (int i = 1, op, l, r, x; i <= m; ++i)
		if (read(op), read(l), read(r), op == 1)
			read(x), SgT::update(l, r, x, 1, n, 1);
		else
			printf("%d\n", SgT::query(l, r));
	return 0;
}