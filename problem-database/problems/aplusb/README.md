# A + B Problem

原版 tuack version 2 独立题目工程，使用标准输入输出。

- `conf.yaml`：题目元数据、数据编号与标准程序的预期得分。
- `statement/zh-cn.md`：原生 tuack Jinja 题面模板。
- `down/`：3 组样例输入与答案。
- `data/`：20 组正式数据，各 5 分，总分 100 分。
- `pre/`：2 组预测试数据，不计入正式测试点。
- `std/std.cpp`：标准程序，预期得分 100。
- `solution/zh-cn.md`：题解。
- `gen.py`：确定性数据生成器，同时提供 tuack.dmk 的 gen、vali、std 钩子。
- `tables/`、`resources/`：预留的表格及资源目录。

在本工程目录执行 `python3 gen.py` 可原样重建全部输入和答案，无需额外依赖。

在已配置 tuack 的环境中，可使用 `python3 -m tuack.ren loj` 渲染题面、`python3 -m tuack.test` 测试配置中的标准程序；这些命令可能生成 tuack 的缓存、日志和结果文件。
