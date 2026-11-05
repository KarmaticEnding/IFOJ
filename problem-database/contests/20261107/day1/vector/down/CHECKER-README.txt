vector 本地 SPJ 与可视化

checker.cpp 为下发的自测 SPJ，与正式评测 SPJ 分别实现。
testlib.h 来自 Mike Mirzayanov 的官方仓库，未作修改。
来源与版本见 TESTLIB-SOURCE.json。原文件保留其版权与许可声明。

编译（Linux / MinGW）：
g++ -O2 -std=c++14 checker.cpp -o checker

运行：
./checker input.in contestant.out answer.ans

例如：
./checker 2.in my.out 2.ans

第三个文件须存在，这是 testlib 的标准接口；本题不读取其内容。
退出码为 0 表示通过；其他退出码表示错误或格式问题，提示写在标准错误输出。
随附 checker 是 Linux x86-64 可执行文件，其他系统请编译 checker.cpp。

坐标序列必须从 (1,1) 开始，恰好有 n*m 个格子，所有格子及有符号位移向量均不得重复。
(dx,dy) 与 (-dx,-dy) 通常是不同向量。不要只比较绝对值，也不要要求与样例答案一致。

visualizer.html 为独立离线文件，直接用浏览器打开即可。
填写 n、m 后，在“操作序列”中每行填 x y，点击“载入序列”验证和播放。
也可以从 (1,1) 开始依次点击网格，文本框将生成相同格式的坐标序列。
支持撤回、复制、逐步播放、缩放、滚动及定位当前点。
网格按可见区域绘制，支持合法的百万格输入；密集路径仅显示最近若干步以便观察。
没有网络请求，也不会上传输入。最终判定以正式评测为准。
