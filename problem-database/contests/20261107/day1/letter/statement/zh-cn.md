{{ self.title() }}

{{ s('description') }}

给定字符串 $S$ 和 $k$ 个模式串 $t_1,t_2,\ldots,t_k$，其中 $S$ 由小写字母 `a` 至 `n` 和问号 `?` 组成，每个模式串只含小写字母 `a` 至 `n`。

每个模式串 $t_i$ 有一个整数权值 $c_i$。定义字符串 $T$ 的价值为

$$\sum_{i=1}^{k}F(T,t_i)c_i,$$

其中 $F(T,t_i)$ 是 $t_i$ 在 $T$ 中作为连续子串出现的次数，允许不同次出现互相重叠。例如，$F(\texttt{aaabaaa},\texttt{aa})=4$。模式串可能相同，相同模式串的每一项权值都要计入。

请将 $S$ 中的每个问号替换为 `a` 至 `n` 中的一个字母，使替换后的字符串价值最大，并输出这个最大价值。

**不同问号填入的字母必须互不相同，但可以与原串中已有的字母相同。** 保证问号个数不超过 $14$。所有问号均须替换，权值和答案都可能为负数。

{{ s('input format') }}

{{ self.input_file() }}

第一行一个正整数 $k$。

接下来 $k$ 行，第 $i$ 行包含一个字符串 $t_i$ 和一个整数 $c_i$。

最后一行一个字符串 $S$。

{{ s('output format') }}

{{ self.output_file() }}

输出一行一个整数，表示替换后字符串的最大价值。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 1) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

可以将 $S$ 替换为 `cba`，价值为 $3+1+1=5$。替换为 `abc` 时还会出现权值为 $-10$ 的模式串，因此价值反而更小。

{{ s('sample', 2) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

两个相同模式串的权值均要计算。将问号替换为 `a`，价值为 $1+1=2$。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 3) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

共有 $14$ 个问号，必须恰好用完 `a` 至 `n` 这 $14$ 个字母，其中 `a` 恰好出现一次。因此最大价值为 $-1$，不能通过不填某个问号来避免负贡献。

{{ s('sample', 4) }}

{{ self.sample_file() }}

该样例满足测试点 $1\sim2$ 的限制。

{{ s('sample', 5) }}

{{ self.sample_file() }}

该样例满足测试点 $3\sim4$ 的限制。

{{ s('sample', 6) }}

{{ self.sample_file() }}

该样例满足测试点 $5\sim7$ 的限制。

{{ s('sample', 7) }}

{{ self.sample_file() }}

该样例满足测试点 $8\sim10$ 的限制。

{{ s('sample', 8) }}

{{ self.sample_file() }}

该样例满足测试点 $11\sim12$ 的限制。

{{ s('sample', 9) }}

{{ self.sample_file() }}

该样例满足测试点 $13\sim16$ 的限制。

{{ s('sample', 10) }}

{{ self.sample_file() }}

该样例满足测试点 $17\sim20$ 的限制。

{{ s('subtasks') }}

记 $n=|S|$，$L=\sum_{i=1}^k|t_i|$，$q$ 为 $S$ 中问号的个数。

对于所有测试数据，满足 $1\le k\le{{ tools.hn(1000) }}$，$1\le n\le{{ tools.hn(400000) }}$，$1\le|t_i|\le{{ tools.hn(1000) }}$，$1\le L\le{{ tools.hn(1000) }}$，$0\le q\le14$，$-{{ tools.hn(1000000) }}\le c_i\le{{ tools.hn(1000000) }}$。

本题共 $20$ 个测试点，每个测试点 $5$ 分，独立计分。各测试点限制如下表所示。

{{ tbl('data') }}

特殊性质 A：对于 $S$ 中任意两个问号，其下标 $p,r$ 均满足 $|p-r| \ge \max_i|t_i|$。

特殊性质 B：所有模式串长度均不超过 $2$。
