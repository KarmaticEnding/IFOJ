# 向量（vector）

20261107 模拟赛 T1，采用 CF1179B 的任务定义，中文题面重新编写。来源：https://codeforces.com/problemset/problem/1179/B

- GPT/vector.cpp：标准程序，O(nm) 时间、O(1) 额外空间，正常编译使用 vector.in/vector.out，__TUACK__ 或 LOCAL 宏下使用标准输入输出。
- 时限 1 秒，内存 256 MiB，nm≤1000000。
- data/1–20：正式输入与合法参考构造，20 个独立等分测试点，每点 5 分。分档为 1–2（nm≤9，10 分）、3–6（一维，20 分）、7–12（乘积偶数，30 分）、13–20（无额外限制，40 分）。
- down/1–3：题面小样例。down/4–7：依次对应四档的大样例，每份均有合法参考输出；题面注明对应测试点。
- 所有非小规模正式数据和大样例均有 nm≥990000；无特殊性质档混合奇偶组合和不同长宽比，没有额外固定操作模式。
- statement/zh-cn.md、tables/data.json、solution/zh-cn.md：完整 tuack 题面、部分分表和题解。

## 两个不同的 SPJ

正式版：data/chk/chk.cpp，使用稠密标记数组。既支持普通 testlib 三文件接口，也支持 Linux 下 tuack/Lemon 的七参数评分接口。

下发版：down/checker.cpp，使用哈希集合和不同的键编码，提供详细错误提示；附 Linux x86-64 可执行文件 down/checker。两者分别实现判定，不是同一份源码复制改名。

二者均引用 Mike Mirzayanov 官方仓库的 testlib.h，文件原样保留。tools/testlib-source.json 和 down/TESTLIB-SOURCE.json 记录精确提交、下载链接和 SHA-256。两个 checker 都忽略参考答案内容，接受任意合法路线。

## 离线可视化

down/visualizer.html 用浏览器直接打开，包含 n、m 和操作序列三个输入框。每行一个 x y；可以载入序列验证和播放，也可依次点击网格生成坐标序列。支持撤回、复制、缩放、滚动、定位和逐步播放。网格按可见区域绘制，支持百万格合法输入，不依赖网络资源。

## 验证与复现

先运行 python3 tools/verify.py，再在空数据副本运行 python3 gen.py。后者检查前者的记录和源码哈希，不覆盖已存在的 .in/.ans。每份参考输出另经过独立 Python 判定和两个 SPJ。

```bash
python3 -m tuack.test -s
python3 -m tuack.ren noi -s
```

测试日志和数据清单位于 tools/。构造题必须通过正式 SPJ 验证，不能以文本相等替代判定。
