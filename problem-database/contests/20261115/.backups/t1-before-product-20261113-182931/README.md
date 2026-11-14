# 20261114 CSP-S 模拟赛

使用本机 tuack 官方生成器初始化，配置格式为 version 2。

当前题目依次为 `day1/span`、`day1/t2`、`day1/t3`、`day1/t4`。
span 暂列第一题，最终题序待确定；其他三个名称均为占位符。
span is complete; the other three problems remain placeholders.

比赛时间暂沿用四小时安排：2026-11-14 08:30—12:30（北京时间），尚待确认。
span: 2.5 seconds, 512 MiB. Other problems keep their placeholder resource limits.
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
