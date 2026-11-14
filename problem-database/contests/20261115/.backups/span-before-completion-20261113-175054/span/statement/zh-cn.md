{{ self.title() }}

{{ s('description') }}

给一个长度为 $n$ 的序列 $a_1, a_2, \dots, a_n$。

定义

$$
\text{exist}_k(l, r) = \left[\{i \mid i \in [l, r] \wedge a_i = k\} \neq \varnothing\right]
$$

再定义

$$
\text{span}_k(l, r) =
\begin{cases}
\displaystyle \left(\max_{i \in [l, r] \wedge a_i = k} i\right) - \displaystyle \left(\min_{i \in [l, r] \wedge a_i = k} i\right) + 1 & \text{exist}_k(l, r) \\
0 & \text{otherwise}
\end{cases}
$$

给出 $m$ 次查询，每次查询给出三个正整数 $l, r, x$，你需要求出

$$
\min_{k\ge1,\ \text{span}_k(l, r) \le x} k
$$

{{ s('input format') }}

{{ self.input_file() }}

待编写。

{{ s('output format') }}

{{ self.output_file() }}

待编写。

{{ s('subtasks') }}

待确定数据范围、测试点和部分分。
