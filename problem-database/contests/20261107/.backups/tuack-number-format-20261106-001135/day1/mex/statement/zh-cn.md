{{ self.title() }}

{{ s('description') }}

对于一个由非负整数组成的序列 $c$，定义 $\operatorname{MEX}(c)$ 为没有在 $c$ 中出现的最小非负整数。例如，$\operatorname{MEX}([0,1,3])=2$，$\operatorname{MEX}([2,2])=0$。

给定整数 $n,k$ 和序列 $b_1,b_2,\ldots,b_n$。请统计有多少个长度为 $n$ 的整数序列 $a$ 同时满足：

- 对于每个 $1\le i\le n$，都有 $0\le a_i\le n$；
- 对于每个 $1\le i\le n$，都有

  $$\left|\operatorname{MEX}([a_1,a_2,\ldots,a_i])-b_i\right|\le k.$$

答案可能很大，请输出答案对 $998244353$ 取模的结果。两个序列不同，当且仅当它们在至少一个位置上的元素不同。

{{ s('input format') }}

{{ self.input_file() }}

第一行两个整数 $n,k$。第二行 $n$ 个整数 $b_1,b_2,\ldots,b_n$。

{{ s('output format') }}

{{ self.output_file() }}

输出一行一个非负整数，表示满足条件的序列个数对 $998244353$ 取模的结果。

{{ s('sample', 1) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

每个前缀的 MEX 都必须为 $0$，因此序列中不能出现 $0$。每个位置可以独立选择 $1,2,3,4$，答案为 $4^4=256$。

{{ s('sample', 2) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

前两个前缀的 MEX 只能为 $0$ 或 $1$；后两个前缀的 MEX 可以为 $0,1,2$。注意这里限制的是每个前缀，而不仅是整个序列。

{{ s('sample', 3) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

$b_i$ 可以为负数。第一个前缀的 MEX 必须为 $0$，最后一个前缀的 MEX 必须至少为 $2$。满足条件的序列共有 $11$ 个。

{{ s('sample', 4) }}

{{ self.sample_file() }}

该样例满足测试点 $1\sim2$ 的限制。

{{ s('sample', 5) }}

{{ self.sample_file() }}

该样例满足测试点 $3\sim5$ 的限制。

{{ s('sample', 6) }}

{{ self.sample_file() }}

该样例满足测试点 $6\sim9$ 的限制。

{{ s('sample', 7) }}

{{ self.sample_file() }}

该样例满足测试点 $10\sim11$ 的限制。

{{ s('sample', 8) }}

{{ self.sample_file() }}

该样例满足测试点 $12\sim15$ 的限制。

{{ s('sample', 9) }}

{{ self.sample_file() }}

该样例满足测试点 $16\sim19$ 的限制。

{{ s('sample', 10) }}

{{ self.sample_file() }}

该样例满足测试点 $20\sim25$ 的限制。

{{ s('subtasks') }}

对于所有测试数据，满足 $1\le n\le2000$，$0\le k\le50$，$-k\le b_i\le n+k$。

{{ tbl('data', merge=False) }}
