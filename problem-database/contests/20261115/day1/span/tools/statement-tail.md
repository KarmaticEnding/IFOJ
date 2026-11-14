{{ s('input format') }}

{{ self.input_file() }}

第一行包含两个正整数 $n,m$。

第二行包含 $n$ 个正整数 $a_1,a_2,\ldots,a_n$。

接下来 $m$ 行，每行包含三个正整数 $l,r,x$，表示一次查询。

{{ s('output format') }}

{{ self.output_file() }}

对于每次查询，输出一行一个正整数，表示满足 $\operatorname{span}_k(l,r)\le x$ 的最小正整数 $k$。

未出现的正整数的 span 为 $0$，因此答案一定存在；答案允许大于序列中的最大值。

{{ s('sample', 1) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

前两次查询中，$1$ 和 $2$ 的 span 都为 $3$，而 $3$ 没有出现，span 为 $0$，因此答案为 $3$。当 $x=3$ 时，$1$ 已满足条件。

对于区间 $[2,3]$，$1$ 和 $2$ 均只出现一次，span 均为 $1$，答案为 $1$。

{{ s('sample', 2) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

区间 $[1,2]$ 和 $[2,2]$ 中均没有出现 $1$，但它的 span 为 $0$，因此两次查询的答案均为 $1$。

{{ s('sample', 3) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

在区间 $[1,6]$ 中，$1,2,3$ 的 span 均为 $4$。因此当 $x=3$ 时，答案为未出现的 $4$；当 $x=4$ 时，答案为 $1$。

{{ s('sample', 4) }}

{{ self.sample_file() }}

该样例满足测试点 $1$ 的限制。

{{ s('sample', 5) }}

{{ self.sample_file() }}

该样例满足测试点 $2\sim3$ 的限制。

{{ s('sample', 6) }}

{{ self.sample_file() }}

该样例满足测试点 $4\sim5$ 的限制。

{{ s('sample', 7) }}

{{ self.sample_file() }}

该样例满足测试点 $6\sim7$ 的限制。

{{ s('sample', 8) }}

{{ self.sample_file() }}

该样例满足测试点 $8\sim10$ 的限制。

{{ s('sample', 9) }}

{{ self.sample_file() }}

该样例满足测试点 $11\sim12$ 的限制。

{{ s('sample', 10) }}

{{ self.sample_file() }}

该样例满足测试点 $13\sim16$ 的限制。

{{ s('sample', 11) }}

{{ self.sample_file() }}

该样例满足测试点 $17\sim20$ 的限制。

{{ s('subtasks') }}

对于所有测试数据，满足 $1\le n,m\le{{ args['n'].hn() }}$，$1\le a_i\le n$。每次查询均满足 $1\le l\le r\le n$，$1\le x\le n$。

本题共 $20$ 个测试点，每个测试点 $5$ 分，独立计分，各测试点限制如下表所示。

{{ tbl('data', merge=False) }}

特殊性质 A：同一个测试点内所有查询的 $x$ 均相同。

特殊性质 B：对于每个值，它在整个序列中出现的次数均不超过两次。
