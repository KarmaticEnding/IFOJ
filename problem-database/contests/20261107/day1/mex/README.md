# T4 mex — MEX 计数

改编自 CF1608F：https://codeforces.com/problemset/problem/1608/F 。模数为 998244353。
标准程序 GPT/mex.cpp；文件输入输出 mex.in / mex.out；定义 LOCAL 或 __TUACK__ 时使用标准流。
25 个测试点独立计分，每点 4 分，七档分值依次为 8、12、16、8、16、16、24。
down/1..3 为内嵌样例，down/4..10 分别为七档大样例。

复现顺序：python3 tools/verify.py，成功后 python3 gen.py。生成器拒绝覆盖已有数据文件，并要求当前源码 hash 与校验记录一致。
正式数据与大样例均用另一份未加权 DP 交叉校验，前两档另用真实集合状压核对。
输入 n、k 均取该档上限；b 由不同随机序列的前缀 MEX 加独立扰动生成，另包含少量末尾矛盾的无解数据。
源码及工具为本工程实现，未复制原题选手代码。普通整数答案，无需 SPJ。
