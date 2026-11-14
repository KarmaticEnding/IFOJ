# subsequence（T2：子序列）

来源：CF1409F Subsequences of Length Two。
https://codeforces.com/problemset/problem/1409/F

标准程序为 GPT/subsequence.cpp。n<=200，0<=k<=n。
文件输入输出：subsequence.in / subsequence.out。
时限 1.0s，内存 256 MiB。输出唯一整数，使用普通答案比较。

20 个独立测试点，每点 5 分；六档为 10/10/15/10/20/35。
down/1--3 为题面展示样例，down/4--9 为六档的单独文件样例。
题面表格不含分值列，数字由 tuack 的 hn/js_hn 格式化。

在本题目录验证、生成和评测：

```sh
python3 gen.py
python3 tools/harden.py
python3 -m tuack.test -s
```

gen.py 先做穷举与独立 DP 核对，再生成数据。生成器会校验已完成数据的哈希，保留已核对的数据。
tuack.test 返回值请结合 result.csv 检查；本机 tuack 会在分数 100 时仍因其他检查警告返回非零。

单题 PDF：

```sh
python3 tools/render_noi.py noi -s
```

在比赛根目录生成合并题面：

```sh
python3 day1/subsequence/tools/render_noi.py noi -s
```

此入口调用 tuack 官方渲染流程，仅在临时封面模板中让长文件名自动缩放至单元格宽度，解决 subsequence.in/out/cpp 在四题封面中的重叠。tuack 安装文件、题面内容、实际文件名和配置不变；渲染前后核对原模板 SHA256。

tools/verification.json：生成前正确性验证及源码哈希。
tools/data-audit.json：29 份输入/答案的规模、预算、独立核对、资源和哈希。
tools/hardening-audit.json：二元串简化、局部贪心、压掉字符个数状态等错误做法的结果。
tools/final-check.json：tuack 得分、样例、实测资源、其他题目配置保护结果。
tools/pdf-qa.json：单题和整场题面的页数、哈希与视觉检查记录。
tools/cover-render-audit.json：封面适配及官方模板未改动的记录。
