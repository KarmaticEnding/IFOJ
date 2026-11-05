# T3 letter — 字母与问号

改编自 CF1327G：https://codeforces.com/problemset/problem/1327/G 。
标准程序 GPT/letter.cpp，文件输入输出 letter.in / letter.out。定义 LOCAL 或 __TUACK__ 时使用标准流。
20 个测试点每点 5 分，七档为 10/10/15/15/10/20/20。表格不展示分值列。
down/1..3 为题面展示样例，down/4..10 分别为七档满规模大样例。

先运行 python3 tools/verify.py，成功后运行 python3 gen.py。生成器校验标准程序及独立程序的源码 hash，拒绝覆盖已有数据。
所有正式数据和大样例答案均由独立的字面前缀自动机及反向 DP 核对。完整记录在 tools/。
权值涵盖正负数，模式串允许重复，问号填入字母互异但可以与固定字符相同。唯一整数答案，无需 SPJ。
