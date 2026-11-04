# 20261107 CSP-S 模拟赛

这是比赛工程骨架，尚未命题，不能直接用于正式比赛。

## 工程结构

使用本机 tuack 0.1.5.4.7 官方生成器建立，conf.yaml 为 tuack version 2。
比赛根目录 → day1 比赛日 → t1、t2、t3、t4 四道传统题。

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
- 题目名称 t1–t4、标题均为占位；重命名时同步修改目录、name 与 day1 的 subdir。
- 每题时间 1 秒、内存 512 MiB、C++14 -O2 为 tuack 模板默认值，须按题目调整。
- file io: true，文件名随题目 name 为 t1.in / t1.out 等；这是 .out 提交文件名，标准答案数据仍用 .ans。
- partial score: false 为模板默认值；如需测试点部分分或子任务，请确定计分方式后修改。
- data、samples、pre 与 users 均为空，不含示例题数据、标准程序或虚构测试点。

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
python3 -m tuack.test
python3 -m tuack.ren noi -s
```

当前阶段仅验证工程解析、层级与目录完整性；尚不能完成评测和正式题面发布。
