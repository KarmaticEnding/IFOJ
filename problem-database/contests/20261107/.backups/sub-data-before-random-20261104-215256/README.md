# 子区间（sub）

本题为 20261107 CSP-S 模拟赛 T2。模数保持原题面配置 993244853。

- 标准程序：GPT/sub.cpp，O(n+m log n)，线段树。
- 时限 8 秒，内存 512 MiB；本机最大随机点约 4.5 秒、94 MiB，详见 tools/data-manifest.json。
- 正常编译读取 sub.in、写入 sub.out；定义 __TUACK__ 或 LOCAL 时使用标准输入输出。
- data/1.in 至 data/20.in 为正式输入，答案为同名 .ans，每点 5 分，按 tuack 等分测试点规则独立计分，总分 100；data 不设置 score 字段。
- down/1–3 为题面小样例，down/4–11 依次对应八档限制的大样例，每份均附 .ans；题面通过 tuack 宏引用。
- pre/ 保持为空；未另设预测试。
- tables/data.json 为 tuack 部分分表；solution/zh-cn.md 为题解。

## 验证顺序

先运行 python3 tools/verify.py，再运行 python3 gen.py。造数脚本检查标准程序与独立参考程序的 SHA-256 和验证记录，未验证或验证后变更代码将拒绝造数。

verify.py 使用显式枚举所有子区间的暴力解，完成 1062 组穷举与随机对拍；其中 142 组启用未定义行为与数组边界检查，另检查 sub.in/sub.out 模式。

gen.py 使用固定种子，为每份输入验证范围、操作数量和特殊性质；由标准程序生成答案，再与 tools/reference.cpp 的四棵树状数组解法比较。完整记录见 tools/verification.json、tools/data-manifest.json 和 tools/generation.log。

为避免覆盖，gen.py 要求输出文件尚不存在。复现数据请在新的空构建副本中复制源码、验证脚本和配置后运行，不要直接删除或覆盖正在使用的数据。

在本题目录执行正式检查：

```bash
python3 -m tuack.ls
python3 -m tuack.test -s
python3 -m tuack.ren noi -s
```

正常源码编译、模数减法、64 位乘法、首尾区间、单点查询、单点修改、整段修改、嵌套区间、跨中点区间和模意义下变为零均已纳入验证。标准程序的源码哈希包含在验证与造数记录中。
