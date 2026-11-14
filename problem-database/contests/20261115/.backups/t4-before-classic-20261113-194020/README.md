# 20261114 CSP-S 模拟赛

使用本机 tuack 官方生成器初始化，配置格式为 version 2。

当前题目依次为 `day1/product`, `day1/t2`, `day1/span`, `day1/t4`。
T1 product, T3 span; T2 and T4 are placeholders.
product and span are complete; t2 and t4 remain placeholders.

比赛时间暂沿用四小时安排：2026-11-14 08:30—12:30（北京时间），尚待确认。
product: 1.0 second, 256 MiB; span: 1.0 seconds, 512 MiB. T2/T4 retain placeholder limits.
使用文件输入输出，文件名与题目目录名一致；C++ 默认使用 C++14、-O2。

造题约定保存在本目录 AGENTS.md，后续所有题目沿用。
标准程序放在各题 `GPT/<题目名>.cpp`；公开样例放在 `down/`；正式数据放在 `data/`。

在比赛根目录检查工程：`python3 -m tuack.ls`。
完成题目后依次进行程序验证、数据生成和独立答案核对、tuack 评测、题面渲染检查。
tuack 评测与题面渲染应串行执行，避免临时目录冲突。


## span completed

GPT/span.cpp implements rollback Mo with monotone span buckets. Twenty independent 5-point cases; tiers 5/10/10/10/15/10/20/20. Three inline samples plus eight large file samples.
The original description is preserved. All answers are independently checked; tuack score 100.
Long intervals, large answers, actual endpoint movement and negative benchmarks are recorded in day1/span/tools/hardening-audit.json.
The stronger quadratic baseline exceeds six seconds on all four 40000 cases. Direct span-array candidate enumeration and span-prefix scans also fail the final full-size cases.
Original span backup: .backups/span-before-completion-20261113-175054


## T1 product completed

n<=1000000, b_i<=10^18, modulus=100000007. GPT/product.cpp; five tiers 10/20/20/20/30, twenty independent five-point cases.
All .ans files contain only the count; sample .out files contain the full two-line example outputs. Impossible contestant output must be two lines of -1; zero modular count still requires a valid construction.
Independent official/download checkers use unmodified official testlib.h, with provenance and SHA256 recorded. tuack score 100.
Order: product, t2, span, t4. Backup: .backups/t1-before-product-20261113-182931
