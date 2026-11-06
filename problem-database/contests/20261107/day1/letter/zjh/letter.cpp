#include <queue>
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
		bool isneg = false;
		for (; c < '0' || c > '9'; c = gc())
			isneg |= c == '-';
		for (; c >= '0' && c <= '9'; c = gc())
			x = (x << 3) + (x << 1) + (c & 15);
		isneg && (x = -x);
	}
	inline void readstr(char *s, int &n)
	{
		char c = gc(); n = 0;
		while ((c < 'a' || c > 'z') && c != '?')
			c = gc();
		for (; (c >= 'a' && c <= 'z') || c == '?'; c = gc())
			s[++n] = c;
	}
	#undef gc
}
using FastIn::read;
using FastIn::readstr;
const long long inf = 1e18;
int n, m, c, p[17], ed[1007];
long long ans = -1e18, f[(1 << 14) | 7][1007];
char sstr[1007], *psstr = sstr, *s[1007], S[400007];
namespace AC
{
	struct ACNode { int ch[14], fail; } tr[1007];
	struct Edge { int v, nxt; } e[1007];
	int tot = 1, idx = 1, tim, h[1007], nxt[15][1007];
	long long w[1007], wnxt[15][1007];
	inline void add(const int &u, const int &v) { e[++idx] = {v, h[u]}, h[u] = idx; }
	inline void insert(char *s, const int &len, const int &id, const int &val)
	{
		int u = 1;
		for (int i = 1; i <= len; ++i)
			!tr[u].ch[s[i] - 'a'] && (tr[u].ch[s[i] - 'a'] = ++tot), u = tr[u].ch[s[i] - 'a'];
		w[ed[id] = u] += val;
	}
	inline void getfail()
	{
		std::queue<int> q;
		for (int i = 0; i < 14; ++i)
			if (tr[1].ch[i])
				tr[tr[1].ch[i]].fail = 1, q.push(tr[1].ch[i]);
			else
				tr[1].ch[i] = 1;
		while (q.size())
		{
			int u = q.front(); q.pop();
			for (int i = 0; i < 14; ++i)
				if (tr[u].ch[i])
					tr[tr[u].ch[i]].fail = tr[tr[u].fail].ch[i], q.push(tr[u].ch[i]);
				else
					tr[u].ch[i] = tr[tr[u].fail].ch[i];
		}
	}
	void DFS0(const int &u)
	{
		for (int i = h[u], v = e[i].v; i; v = e[i = e[i].nxt].v)
			w[v] += w[u], DFS0(v);
	}
	inline void build()
	{
		getfail();
		for (int i = 2; i <= tot; ++i)
			add(tr[i].fail, i);
		DFS0(1);
	}
	inline int getnxt(const int &pi, const int &su)
	{
		if (nxt[pi][su])
			return nxt[pi][su];
		int u = su;
		for (int i = p[pi] + 1; i < p[pi + 1]; ++i)
			u = tr[u].ch[S[i] - 'a'], wnxt[pi][su] += w[u];
		return nxt[pi][su] = u;
	}
}
int main()
{
	read(n);
	for (int i = 1, len, w; i <= n; ++i)
		readstr(s[i] = psstr, len), read(w), psstr += len, AC::insert(s[i], len, i, w);
	s[n + 1] = psstr, AC::build(), readstr(S, m);
	for (int i = 1; i <= m; ++i)
		S[i] == '?' && (p[++c] = i);
	p[c + 1] = m + 1;
	for (int st = 0; st < 16384; ++st)
		for (int u = 1; u <= AC::tot; ++u)
			f[st][u] = -inf;
	f[0][1] = 0;
	for (int st = 0; st < 16384; ++st)
		if (__builtin_popcount(st) < c)
			for (int u = 1, v; u <= AC::tot; ++u)
				if (f[st][u] > -inf)
				{
					v = AC::getnxt(__builtin_popcount(st), u);
					long long w = AC::wnxt[__builtin_popcount(st)][u];
					for (int sch = (16384 - 1) ^ st, ch, vv; sch; sch &= (sch - 1))
						ch = __builtin_ctz(sch), vv = AC::tr[v].ch[ch],
						f[st | (1 << ch)][vv] = std::max(f[st | (1 << ch)][vv], f[st][u] + w + AC::w[vv]);
				}
	for (int st = 0; st < 16384; ++st)
		if (__builtin_popcount(st) == c)
			for (int u = 1; u <= AC::tot; ++u)
				if (f[st][u] > -inf)
					AC::getnxt(c, u), ans = std::max(ans, f[st][u] + AC::wnxt[c][u]);
	printf("%lld\n", ans);
	return 0;
}