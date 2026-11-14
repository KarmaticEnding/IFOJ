{{ self.title() }}

{{ s('description') }}

给定一张有 $n$ 个顶点、$m$ 条边的无向图，顶点编号为 $1,2,\ldots,n$。图中没有自环和重边，但不保证连通。

第 $i$ 条边连接顶点 $u_i$ 和 $v_i$，边权为 $2^{x_i}$，其中 $x_i$ 是一个非负整数。

给定起点 $s$ 和终点 $t$，请找出一条从 $s$ 到 $t$ 的最短路径。路径的长度为经过的所有边的边权之和。

若存在这样的路径，你需要输出最短路径长度对 ${{ args['mod'].hn() }}$ 取模的值，以及任意一条最短路径。注意，取模仅用于输出，判断路径长短时应比较实际长度。

{{ s('input format') }}

{{ self.input_file() }}

第一行包含两个整数 $n,m$。

接下来 $m$ 行，每行包含三个整数 $u_i,v_i,x_i$，表示一条连接 $u_i,v_i$、边权为 $2^{x_i}$ 的无向边。

最后一行包含两个整数 $s,t$，表示起点和终点。允许 $s=t$。

{{ s('output format') }}

{{ self.output_file() }}

如果从 $s$ 无法到达 $t$，只输出一行一个整数 $-1$。

否则输出三行：

- 第一行输出最短路径长度对 ${{ args['mod'].hn() }}$ 取模的值。
- 第二行输出一个正整数 $k$，表示路径经过的顶点数，满足 $1\le k\le n$。
- 第三行输出 $k$ 个整数 $p_1,p_2,\ldots,p_k$，依次表示路径上的顶点。要求 $p_1=s$、$p_k=t$，相邻顶点间有边，且所有顶点互不相同。

若有多条最短路径，输出任意一条即可。特别地，当 $s=t$ 时，最短路径长度为 $0$，路径只包含顶点 $s$。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 1) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

路径 $1\to2\to3\to4$ 的长度为 $1+1+1=3$，小于直接经过边 $(1,4)$ 的长度 $4$。

{{ s('sample', 2) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

路径 $1\to3$ 和 $1\to2\to3$ 的长度均为 $2$，输出其中任意一条都可以。

{{ s('sample', 3) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

顶点 $1$ 和顶点 $4$ 不连通，因此输出 $-1$。

{{ s('sample', 4) }}

{{ self.sample_file() }}
该样例满足测试点 $1\sim3$ 的限制。

{{ s('sample', 5) }}

{{ self.sample_file() }}
该样例满足测试点 $4\sim5$ 的限制。

{{ s('sample', 6) }}

{{ self.sample_file() }}
该样例满足测试点 $6$ 的限制。

{{ s('sample', 7) }}

{{ self.sample_file() }}
该样例满足测试点 $7\sim8$ 的限制。

{{ s('sample', 8) }}

{{ self.sample_file() }}
该样例满足测试点 $9\sim12$ 的限制。

{{ render(json.dumps('\\clearpage'), 'noi') }}

{{ s('sample', 9) }}

{{ self.sample_file() }}
该样例满足测试点 $13\sim16$ 的限制。

{{ s('sample', 10) }}

{{ self.sample_file() }}
该样例满足测试点 $17\sim22$ 的限制。

{{ s('sample', 11) }}

{{ self.sample_file() }}
该样例满足测试点 $23\sim25$ 的限制。

{{ s('subtasks') }}

对于所有测试数据，满足 $1\le n\le{{ args['n'].hn() }}$，$0\le m\le{{ args['m'].hn() }}$，$1\le u_i,v_i,s,t\le n$，$u_i\ne v_i$，$0\le x_i\le{{ args['X'].hn() }}$，且图中没有重边。

当 $m>0$ 时，定义 $X=\max_{1\le i\le m}x_i$、$Y=\min_{1\le i\le m}x_i$；当 $m=0$ 时，约定 $X=Y=0$。

本题共 $25$ 个测试点，每个测试点 $4$ 分，独立计分。各测试点限制如下表所示。

{{ tbl('data', merge=False) }}

“最多两种指数”指集合 $\{x_i\mid1\le i\le m\}$ 的大小不超过 $2$。

