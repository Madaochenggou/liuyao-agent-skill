# 历法依赖审查

当前精确模式使用 `lunar-python==1.4.9`，其 PyPI 页面和上游仓库标示 MIT 许可证，支持公历、农历、干支、节气和八字接口。版本、许可证与 API 入口需在升级时重新核对；项目不复制其源码，运行时依赖由 `pyproject.toml` 声明。

本项目固定通过 `Solar -> Lunar` 计算，并保留输入时区、节气前后界限、月干支、日干支、时干支和旬空。`lunar-python` 的节气时刻是库内算法结果，不能被本项目再次包装成天文观测事实；升级或更换库必须用固定样本交叉验证。

已验证样本：`2026-11-24T10:00:00+08:00` → 丙午年、己亥月、壬寅日、乙巳时，旬空辰巳。早子时/晚子时和部分换日规则属于流派差异，接口保留 `day_boundary` 字段，当前默认午夜换日。

来源：[PyPI lunar-python](https://pypi.org/project/lunar-python/)、[上游仓库](https://github.com/6tail/lunar-python)。
