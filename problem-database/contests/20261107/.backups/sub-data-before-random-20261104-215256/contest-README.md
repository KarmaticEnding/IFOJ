# 20261107 CSP-S 模拟赛

T2 子区间（sub）已完成；T1、T3、T4 仍为骨架，整场比赛尚不能直接发布。

## 工程结构

使用本机 tuack 0.1.5.4.7 官方生成器建立，conf.yaml 为 tuack version 2。
比赛根目录 → day1 比赛日 → t1、sub、t3、t4 四道传统题。

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
- T1、T3、T4 的题名和配置仍为占位；T2 已重命名为 sub，标题为“子区间”。
- T1、T3、T4 保留模板默认时限；T2 为 8 秒、512 MiB、C++14 -O2。
- file io: true，文件名随题目 name 为 t1.in / t1.out 等；这是 .out 提交文件名，标准答案数据仍用 .ans。
- partial score: false 为模板默认值；如需测试点部分分或子任务，请确定计分方式后修改。
- T1、T3、T4 的数据和程序为空；T2 有 20 个等分测试点、11 份样例，标准程序为 day1/sub/GPT/sub.cpp。

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
