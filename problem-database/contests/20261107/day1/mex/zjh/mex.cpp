#include <cstdio>
template <typename _T> inline _T max(const _T &x, const _T &y) { return x > y ? x : y; }
template <typename _T> inline _T min(const _T &x, const _T &y) { return x < y ? x : y; }
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
	#undef gc
}
using FastIn::read;
const int mod = 998244353;
inline int M(const int &x) { return x >= mod ? x - mod : x; }
int n, m, ans, a[2007], f[2][2007][2007], C[2007][2007];
int main()
{
	for (int i = 0; i < 2007; ++i)
	{
		C[i][0] = C[i][i] = 1;
		for (int j = 1; j < i; ++j)
			C[i][j] = M(C[i - 1][j - 1] + C[i - 1][j]);
	}
	read(n), read(m);
	for (int i = 1; i <= n; ++i)
		read(a[i]);
	f[0][0][0] = 1;
	int lstl = 0, lstr = 0;
	for (int i = 1, l, r; i <= n; ++i)
	{
		l = max(0, a[i] - m), r = min(n, a[i] + m);
		for (int j = l; j <= r; ++j)
			for (int k = 0, lim = min(n - j, i); k <= lim; ++k)
				if (lstl <= j && j <= lstr)
					f[i & 1][j][k] = ((long long)(j + k) * f[(i & 1) ^ 1][j][k] + (k ? (long long)(k) * f[(i & 1) ^ 1][j][k - 1] : 0)) % mod;
				else
					f[i & 1][j][k] = 0;
		for (int t = l, sum, x; t <= n; ++t)
		{
			sum = 0, x = lstl;
			for (int j = l; j <= r && j <= t; ++j)
			{
				for (; x <= lstr && x < j; ++x)
					t - x - 1 >= 0 && (sum = M(sum + f[(i & 1) ^ 1][x][t - x - 1]));
				f[i & 1][j][t - j] = M(f[i & 1][j][t - j] + sum);
			}
		}
		lstl = l, lstr = r;
	}
	for (int j = lstl; j <= lstr; ++j)
		for (int k = 0; k <= n - j; ++k)
			ans = (ans + (long long)(f[n & 1][j][k]) * C[n - j][k]) % mod;
	printf("%d\n", ans);
	return 0;
}