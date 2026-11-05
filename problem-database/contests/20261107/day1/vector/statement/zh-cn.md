{{ self.title() }}

{{ s('description') }}

有一个 $n \times m$ 的网格，由 $n$ 行 $m$ 列组成，其中点的坐标 $(x, y)$ 表示它位于第 $x$ 行第 $y$ 列（行列编号均从 $1$ 开始，$1 \leq x \leq n, 1 \leq y \leq m$）。

你最初站在单元格 $(1, 1)$。每一步，你可以从当前所在的单元格 $(x, y)$ 跳到 $(x+dx, y+dy)$，其中 $(dx, dy)$ 是任意非零向量。你不能跳出网格，且每个向量只能使用一次，不能重复。

请问是否可以恰好访问网格中的每一个单元格一次。如果可以，输出任意一组可行解。

{{ s('input format') }}

{{ self.input_file() }}

输入仅一行，包含两个正整数 $n,m$。

{{ s('output format') }}

{{ self.output_file() }}

若不存在满足要求的方案，输出一行一个整数 $-1$。

否则输出 $n \cdot m$ 行，第 $i$ 行两个整数 $x_i, y_i$，表示第 $i$ 个访问的单元格坐标。

{{ s('sample', 1) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

网格只有一个格子，不需要进行任何跳跃。

{{ s('sample', 2) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

五次跳跃的位移向量依次为 $(1,2)$、$(-1,-1)$、$(1,0)$、$(-1,1)$、$(1,-2)$，互不相同。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 3) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

样例输出仅为一种合法方案，无需与之相同。

{{ s('sample', 4) }}

{{ self.sample_file() }}

该样例满足测试点 $1\sim2$ 的限制。

{{ s('sample', 5) }}

{{ self.sample_file() }}

该样例满足测试点 $3\sim6$ 的限制。

{{ s('sample', 6) }}

{{ self.sample_file() }}

该样例满足测试点 $7\sim12$ 的限制。

{{ s('sample', 7) }}

{{ self.sample_file() }}

该样例满足测试点 $13\sim20$ 的限制。

{{ s('subtasks') }}

对于所有测试数据，满足 $n,m\ge1$，$1\le nm\le {{ args['max_cells'].hn() }}$。

{{ tbl('data', merge=False) }}

{{ s('hint') }}

选手目录另提供本地检查程序 *checker.cpp*、其依赖的原版 *testlib.h* 及使用说明 *CHECKER-README.txt*。本地检查程序与正式评测程序分别实现，均按路线是否合法判定，不要求输出与样例答案相同。

另提供离线工具 *visualizer.html*：可以输入 $n,m$ 和坐标序列播放路线，也可以依次点击网格生成坐标序列。使用时直接用浏览器打开，具体格式见工具页面。
