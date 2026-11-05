# 20261107 CSP-S 模拟赛

T1 vector, T2 sub and T4 mex are complete. T3 remains a placeholder; this contest is not ready for release.

## 工程结构

使用本机 tuack 0.1.5.4.7 官方生成器建立，conf.yaml 为 tuack version 2。
比赛根目录 → day1 比赛日 → vector、sub、t3、mex 四道传统题。

每题目录：
- statement/zh-cn.md：tuack Jinja2 中文题面
- solution/zh-cn.md：题解占位
- data/：正式数据，成对的 .in / .ans
- down/：公开样例及附件
- pre/：预测试数据
- tables/：题面表格
- resources/：题面资源
- std/：标准程序，尚未添加
- gen.py：待实现的数据生成接口；不会执行模板示例造数或重写 data 配置

## 待确认配置

- 比赛时间暂设 2026-11-07 08:30–12:30（北京时间 UTC+8），仅为四小时占位；请在 day1/conf.yaml 修改。
- T3、T4 的题名和配置仍为占位；T2 已重命名为 sub，标题为“子区间”。
- T3、T4 保留模板默认时限；T2 为 2.5 秒、512 MiB、C++14 -O2。
- file io: true，文件名随题目 name 为 t1.in / t1.out 等；这是 .out 提交文件名，标准答案数据仍用 .ans。
- partial score: false 为模板默认值；如需测试点部分分或子任务，请确定计分方式后修改。
- T3、T4 的数据和程序为空；T2 有 20 个等分测试点、11 份样例，标准程序为 day1/sub/GPT/sub.cpp。

## 常用命令

在比赛根目录运行：

```bash
python3 -m tuack.ls
```

补充 .in / .ans 数据与标准程序后，自动登记：

```bash
python3 -m tuack.gen auto
```

完成题面、样例、数据和程序配置后再进行：

```bash
python3 -m tuack.test -s
python3 -m tuack.ren noi -s
```

T2 已完成暴力对拍、双算法数据核验、tuack 正式评测与题面 PDF 检查；详细记录位于 day1/sub/tools/。其他题目尚未完成。

T2 原始文件与本次修改前的比赛配置已备份到 .backups/t2-before-sub-20261104-212209。

T2 已重造全部正式数据和八档大样例，均为所属档位满规模随机数据；原数据备份：.backups/sub-data-before-random-20261104-215256。


T1 向量（vector）已完成，位于 day1/vector。标准程序 GPT/vector.cpp，时限 1 秒、内存 256 MiB；20 个测试点每点 5 分，四档为 10/20/30/40 分。正式 SPJ 位于 data/chk/chk.cpp，下发的独立 SPJ 位于 down/checker.cpp，原版 testlib 来源与哈希已记录。down/visualizer.html 支持离线播放和点击生成路线。
T1 原始文件及修改前的比赛配置备份：.backups/t1-before-vector-20261105-162724。


## T4 mex completed

CF1608F; GPT/mex.cpp; 4.0 s, 256 MiB; 25 independent cases, 4 points each.
Subtask scores: 8/12/16/8/16/16/24. Three inline samples and seven downloadable large samples.
Validation, independent answer checks, tuack 100-point result and statement PDF are in day1/mex.
This entry supersedes older T4 placeholder descriptions above. Backup: .backups/t4-before-mex-20261105-222003
