# T1 product — 前缀乘积

完整范围 n<=1000000，1<=b_i<=10^18；a 必须为正整数。计数模数为 100000007。
20 个独立测试点，每点 5 分，五档 10/20/20/20/30，题面表格不含分值列。
标准程序 GPT/product.cpp；文件输入输出 product.in / product.out；定义 LOCAL 或 __TUACK__ 时使用标准流。

所有 data/*.ans 和 down/*.ans 只含计数。无解的 .ans 只含 -1，而选手必须输出两行 -1。
题面展示样例 down/1..3 的完整输出另外保存在 .out；down/4..8 为五档满规模大样例。
正式 SPJ data/chk/chk.cpp 与下发 SPJ down/checker.cpp 分别实现，使用已记录来源和哈希的官方原版 testlib.h。

复现：先 python3 tools/verify.py，通过后 python3 gen.py。生成器验证源码哈希、拒绝覆盖数据；正式数据与大样例由 Python 精确整数模型独立核对，并逐份通过两个 SPJ。
计数为 0 不意味着无解。题面及检查器都区分这两种情况。单调、交替变化、首项平方与非平方、后期不整除及乘法溢出边界均有覆盖。
