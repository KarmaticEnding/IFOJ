本地检查程序使用说明

编译：g++ -O2 -std=c++14 checker.cpp -o checker
运行：./checker input.in contestant.out reference.ans

reference.ans 必须只含一个整数：正确的方案数模 100000007，或无解时的 -1。
contestant.out 必须包含两行：有解时为计数和 n 个正整数；无解时为两行 -1。
计数为 0 仍须输出合法构造。允许输出与样例不同的合法构造。

checker 为 Linux x86-64 预编译版本；其他系统请使用源码编译。
本地 checker 独立重算计数并用除法校验；正式评测程序信任 .ans 计数并用 128 位乘法校验，二者分别实现。
testlib.h 为 Mike Mirzayanov 官方未修改原版，来源、版本和 SHA256 见 TESTLIB-SOURCE.json。
1.out、2.out、3.out 是题面展示用的完整样例输出；所有 .ans 仍只存计数。
