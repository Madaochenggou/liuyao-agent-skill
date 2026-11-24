# 开源项目调研记录（2026-11-24）

本次只做公开页面和 README 级别审查，没有复制代码或数据：

- [DemonAngela/liuyao_paipan](https://github.com/DemonAngela/liuyao_paipan)：公开仓库页面可见；当前无法据 README 证明其覆盖本项目要求的历法、伏神和全量测试，因此不直接集成。
- [Johnson-Jia/liuyao-divination](https://github.com/Johnson-Jia/liuyao-divination)：README 将其描述为六爻 AI-agent skill 与程序化工具包；需逐条核对其许可证、纳甲和历法实现后才能复用。
- [qilaidev/metaphysics-engine](https://github.com/qilaidev/metaphysics-engine)：README 声明 MIT、Node.js 20+、`lunar-javascript` 和确定性 CLI/API；其 README 也明确算法口径由项目维护，不能把结果视为权威。

结论：这些项目可作为比较对象，不能代替独立标准样本。当前 Python 核心只实现透明的起卦、卦变、基础关系和校验；没有声称完成传统历法、完整八宫纳甲、伏神或统计准确率。引入外部实现前应保存其许可证、版本、测试结果和差异报告。
