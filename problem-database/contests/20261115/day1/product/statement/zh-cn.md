{{ self.title() }}

{{ s('description') }}

给定一个长度为 $n$ 的正整数序列 $b_1,b_2,\ldots,b_n$。

请计算有多少个长度为 $n$ 的正整数序列 $a_1,a_2,\ldots,a_n$，使得对于每个 $1\le i\le n$，均有

$$b_i=\left(\max_{1\le j\le i}a_j\right)\left(\min_{1\le j\le i}a_j\right).$$

两个序列不同，当且仅当至少一个位置的元素不同。你还需要构造任意一个满足条件的序列 $a$。

{{ s('input format') }}

{{ self.input_file() }}

第一行一个正整数 $n$。

第二行包含 $n$ 个正整数 $b_1,b_2,\ldots,b_n$。

{{ s('output format') }}

{{ self.output_file() }}

如果存在满足条件的序列，输出两行：第一行输出方案数对 ${{ args['mod'].hn() }}$ 取模的值；第二行输出 $n$ 个正整数，表示你构造的序列 $a$。

如果不存在满足条件的序列，第一行和第二行均输出一个整数 $-1$。

**方案数取模后为 $0$ 不代表无解。此时仍须在第二行输出合法序列，不能输出 $-1$。**

合法构造的元素一定不超过 ${{ args['max_b'].hn() }}$。若存在多种构造，输出任意一种即可。

{% macro construction_sample() -%}
{{ self.sample_input_text() }}

## {{ _('Sample Output %s') % vars['sample_id'] }}

```plain
{{ down_file(vars['sample_id'].__str__()+'.out') }}
```
{%- endmacro %}

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 1) }}

{{ construction_sample() }}

{{ self.title_sample_description() }}

满足条件的序列恰为 $[2,3,2]$ 和 $[2,3,3]$，因此方案数为 $2$。样例输出只展示其中一种。

{{ s('sample', 2) }}

{{ construction_sample() }}

{{ self.title_sample_description() }}

由 $b_1=4$ 可知 $a_1=2$，但无法填入一个正整数，使第二个前缀的最大值与最小值乘积为 $7$。因此必须输出两行 $-1$。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 3) }}

{{ construction_sample() }}

{{ self.title_sample_description() }}

$a_1$ 必须为 $1$，$a_2$ 必须为 ${{ args['mod'].hn() }}$，而 $a_3$ 可以是 $1$ 至 ${{ args['mod'].hn() }}$ 中的任意一个正整数。恰有 ${{ args['mod'].hn() }}$ 个方案，取模后为 $0$，但仍然有解。

{{ s('sample', 4) }}

{{ self.sample_file() }}

该样例满足测试点 $1\sim2$ 的限制。

{{ s('sample', 5) }}

{{ self.sample_file() }}

该样例满足测试点 $3\sim6$ 的限制。

{{ s('sample', 6) }}

{{ self.sample_file() }}

该样例满足测试点 $7\sim10$ 的限制。

{{ s('sample', 7) }}

{{ self.sample_file() }}

该样例满足测试点 $11\sim14$ 的限制。

{{ s('sample', 8) }}

{{ self.sample_file() }}

该样例满足测试点 $15\sim20$ 的限制。

{{ s('subtasks') }}

对于所有测试数据，满足 $1\le n\le{{ args['n'].hn() }}$，$1\le b_i\le{{ args['max_b'].hn() }}$。

本题共 $20$ 个测试点，每个测试点 $5$ 分，独立计分。各测试点限制如下表所示。

{{ tbl('data', merge=False) }}

特殊性质 A：$b$ 单调不降，即对于所有 $1\le i<n$，都有 $b_i\le b_{i+1}$。

特殊性质 B：$b$ 单调不增，即对于所有 $1\le i<n$，都有 $b_i\ge b_{i+1}$。

{{ s('hint') }}

下发的所有 *.ans* 文件都只包含方案数（无解时为 $-1$），不包含构造。题面展示样例的完整输出另存为 *.out* 文件。

选手目录提供本地检查程序 *checker.cpp*、官方原版 *testlib.h* 及说明 *CHECKER-README.txt*，用于检查方案数与构造。该程序与正式评测 SPJ 分别实现。
