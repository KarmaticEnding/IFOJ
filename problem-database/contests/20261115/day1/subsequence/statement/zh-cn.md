{{ self.title() }}

{{ s('description') }}

给定一个长度为 $n$ 的字符串 $s$ 和一个长度为 $2$ 的字符串 $t$，两个字符串均只包含小写英文字母。

你可以进行至多 $k$ 次修改。每次修改选择 $s$ 中的一个位置，将该位置的字符替换为任意一个小写英文字母。

请使修改后的字符串中，等于 $t$ 的长度为 $2$ 的子序列数量尽可能多，并输出这个最大数量。

具体地，所求数量为满足 $1\le i<j\le n$、$s_i=t_1$ 且 $s_j=t_2$ 的下标对 $(i,j)$ 的数量。这里的 $s$ 指修改后的字符串，选取的两个位置不要求相邻。两个下标对只要有一个下标不同，就视为不同的子序列。

{{ s('input format') }}

{{ self.input_file() }}

第一行包含两个整数 $n,k$，分别表示字符串 $s$ 的长度和最多允许进行的修改次数。

第二行包含一个长度为 $n$ 的字符串 $s$。

第三行包含一个长度为 $2$ 的字符串 $t$。

{{ s('output format') }}

{{ self.output_file() }}

输出一行一个整数，表示至多进行 $k$ 次修改后，等于 $t$ 的长度为 $2$ 的子序列数量的最大值。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 1) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

可以将 $s$ 的第 $1$ 个字符改为 `a`、第 $4$ 个字符改为 `b`，得到 `abab`。对应的下标对为 $(1,2)$、$(1,4)$ 和 $(3,4)$，共 $3$ 个。

{{ s('sample', 2) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

可以将字符串改为 `ssddsdd`，恰好修改 $3$ 个位置。第 $1$、$2$、$5$ 个位置的 `s` 分别贡献 $4$、$4$、$2$ 个 `sd` 子序列，总数为 $10$。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 3) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

可以将字符串改为 `aaacaaa`，恰好修改 $2$ 个位置。此时有 $6$ 个 `a`，任选两个不同位置并按下标递增排列，即得到一个 `aa` 子序列，共 $\binom62=15$ 个。

{{ s('sample', 4) }}

{{ self.sample_file().replace(' 与 ', '  \n与 ') }}

该样例满足测试点 $1\sim2$ 的限制。

{{ s('sample', 5) }}

{{ self.sample_file().replace(' 与 ', '  \n与 ') }}

该样例满足测试点 $3\sim4$ 的限制。

{{ s('sample', 6) }}

{{ self.sample_file().replace(' 与 ', '  \n与 ') }}

该样例满足测试点 $5\sim7$ 的限制。

{{ s('sample', 7) }}

{{ self.sample_file().replace(' 与 ', '  \n与 ') }}

该样例满足测试点 $8\sim9$ 的限制。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 8) }}

{{ self.sample_file().replace(' 与 ', '  \n与 ') }}

该样例满足测试点 $10\sim13$ 的限制。

{{ s('sample', 9) }}

{{ self.sample_file().replace(' 与 ', '  \n与 ') }}

该样例满足测试点 $14\sim20$ 的限制。

{{ s('subtasks') }}

对于所有测试数据，满足 $2\le n\le{{ args['n'].hn() }}$，$0\le k\le n$，$s$ 的长度为 $n$，$t$ 的长度为 $2$，且 $s,t$ 均只包含小写英文字母。

本题共 $20$ 个测试点，每个测试点 $5$ 分，独立计分。各测试点限制如下表所示。

{{ tbl('data', merge=False) }}

特殊性质 A：$t_1=t_2$。

特殊性质 B：$t_1\ne t_2$，且对于所有 $1\le i\le n$，均有 $s_i\in\{t_1,t_2\}$。
