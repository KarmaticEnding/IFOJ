# span — 跨度

标准程序 GPT/span.cpp，文件输入输出 span.in / span.out。定义 LOCAL 或 __TUACK__ 时使用标准流。
20 个测试点每点 5 分，八档分值 5/10/10/10/15/10/20/20。题面表格不展示分值列。
down/1..3 为题面展示样例，down/4..11 分别为八档满规模大样例；只有文件大样例标注测试点限制。

复现：先运行 python3 tools/verify.py，再运行 python3 gen.py。生成器验证源码哈希并拒绝覆盖已有输入输出。
程序验证通过后才生成数据。所有数据答案经普通莫队加线段树独立核对；小规模与少查询数据另有完整扫描核验。
tools/data-manifest.json 记录每点长区间大答案数、累计区间长度、累计答案枚举量、实际莫队移动量和文件哈希。
tools/complexity-benchmarks.json 记录逐询问扫描、莫队后候选枚举、直接 span 前缀扫描的限时实测。
所有区间与候选均从 1 编号，不出现的 span 为 0。唯一整数答案，无需 SPJ。

The negative benchmarks also include scan_values.cpp, which stores exact current spans and scans the contiguous value array, so candidate checking is O(1). The 40000 tier is additionally tested with a branch-free quadratic baseline that clips irrelevant values to a dummy slot.
