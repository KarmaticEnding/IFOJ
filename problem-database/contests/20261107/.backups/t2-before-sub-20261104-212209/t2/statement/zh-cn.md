{{ self.title() }}

{{ s('description') }}

给出一个长度为 $n$ 的序列 $a_1, a_2, \dots, a_n$ 和 $m$ 次操作，操作有以下两种：

-	`1 l r x`，对于所有 $i \in [l, r]$，令 $a_i \leftarrow a_i + x$。
-	`2 l r`，查询以下式子对 ${{ args['mod'].hn() }}$的值：

	$$ \sum_{i = l}^r \sum_{j = i}^r \sum_{k = i}^j a_k $$

{{ s('input format') }}

{{ self.input_file() }}

第一行输入两个正整数 $n, m$。

接下来一行输入 $n$ 个正整数表示 $a_1, a_2, \dots, a_n$。

接下来 $m$ 行每行表示一个操作。

{{ s('output format') }}

{{ self.output_file() }}

对于每个查询操作，输出一行一个正整数表示该次查询的答案对 ${{ args['mod'].hn() }}$ 取模的值。

{{ s('subtasks') }}

对于所有的数据，满足 $1 \le n, m \le {{ args['n'].hn() }}, 1 \le l \le r \le n, 1 \le a_i, x < {{ args['mod'].hn() }}$。