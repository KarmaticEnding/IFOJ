{{ self.title() }}

{{ s('description') }}

给出一个长度为 $n$ 的序列 $a_1, a_2, \dots, a_n$ 和 $m$ 次操作。操作有以下两种：

- `1 l r x`：对于所有 $i \in [l, r]$，令 $a_i \leftarrow a_i + x$。
- `2 l r`：查询区间 $[l, r]$ 内所有非空连续子区间的元素和之和，即计算

  $$
  \sum_{i = l}^{r} \sum_{j = i}^{r} \sum_{k = i}^{j} a_k
  $$

  输出其对 ${{ args['mod'].hn() }}$ 取模的结果。

{{ s('input format') }}

{{ self.input_file() }}

第一行包含两个正整数 $n, m$。

第二行包含 $n$ 个正整数 $a_1, a_2, \dots, a_n$。

接下来 $m$ 行，每行表示一个操作，格式为 `1 l r x` 或 `2 l r`，含义如题目描述所示。

{{ s('output format') }}

{{ self.output_file() }}

对于每个 `2` 操作输出一行一个非负整数，表示该次查询的答案对 ${{ args['mod'].hn() }}$ 取模的结果。

{{ s('sample', 1) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

第一次查询时，六个非空连续子区间的元素和分别为 $1, 2, 3, 3, 5, 6$，其和为 $20$。

第一次修改后，序列变为 $[3, 4, 3]$，第二次查询的答案为 $3 + 4 + 3 + 7 + 7 + 10 = 34$，第三次查询的答案为 $4 + 3 + 7 = 14$。

第二次修改后，序列变为 $[3, 5, 4]$，最后一次查询的答案为 $3 + 5 + 8 = 16$。

{{ s('sample', 2) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

第一次修改后，唯一的元素为 ${{ args['mod'].hn() }}$，因此第二次查询的输出为 $0$。这说明输出可能为 $0$。

{{ s('sample', 3) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

该样例中的所有修改均满足 $l = r$；查询区间仍可以包含多个元素。

{{ s('sample', 4) }}

{{ self.sample_file() }}

该样例满足测试点 $1$ 的限制。

{{ s('sample', 5) }}

{{ self.sample_file() }}

该样例满足测试点 $2$ 的限制。

{{ s('sample', 6) }}

{{ self.sample_file() }}

该样例满足测试点 $3$ 的限制。

{{ s('sample', 7) }}

{{ self.sample_file() }}

该样例满足测试点 $4 \sim 5$ 的限制。

{{ s('sample', 8) }}

{{ self.sample_file() }}

该样例满足测试点 $6 \sim 9$ 的限制。

{{ s('sample', 9) }}

{{ self.sample_file() }}

该样例满足测试点 $10 \sim 13$ 的限制。

{{ s('sample', 10) }}

{{ self.sample_file() }}

该样例满足测试点 $14 \sim 16$ 的限制。

{{ s('sample', 11) }}

{{ self.sample_file() }}

该样例满足测试点 $17 \sim 20$ 的限制。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('subtasks') }}

对于所有测试数据，满足 $1 \le n, m \le {{ args['n'].hn() }}$，每次操作均满足 $1 \le l \le r \le n$，初始元素和修改操作中的参数满足 $1 \le a_i, x < {{ args['mod'].hn() }}$。

{{ tbl('data', merge=False) }}

特殊性质 A：对于每次 `1` 操作，均有 $l = r$。
