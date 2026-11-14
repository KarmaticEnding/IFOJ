classic 本地检查程序

编译（C++14，checker.cpp 与 testlib.h 在同一目录）：
  g++ -O2 -std=c++14 checker.cpp -o checker

运行：
  ./checker input.in contestant.out reference.ans
Windows 可将 ./checker 换成 checker.exe。

返回 0 表示通过；非零表示未通过，详细信息写入标准错误。
reference.ans 是本题提供的完整三行参考输出（无路时仅为 -1）。
先将你的程序运行结果保存到 contestant.out，再调用检查程序。
实际路径可以不同；检查程序会精确比较未取模的长度。
只让第一行取模值相同而输出非最短路径，不能通过检查。

本地 SPJ 与正式评测 SPJ 是分别编写的两个实现。
testlib.h 来源及校验值见 TESTLIB-PROVENANCE.txt，未作修改。
