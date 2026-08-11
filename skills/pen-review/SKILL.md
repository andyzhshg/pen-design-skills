---
name: pen-review
description: "只读检查 Pen 设计，不进行修改（Review a Pen design read-only）。"
---

# Pen Review：只读体检

使用 `$pen-review` frontier 和 **read-only** 写入边界运行 `$pen-design-core`。

在已确认范围内检查 object-tree 与 layout 风险、命名、literal-value drift、variable bindings、component reuse、themes、responsive behavior、accessibility signals、hierarchy、density 和 visual craft。存在项目标准时与其对照。

先报告证据，再给建议。按照 user impact、propagation risk 和 repair cost 排序。区分客观事实与视觉判断。

不修改 `.pen`、代码或项目设计文档。局部视觉改动推荐 `$pen-polish`；组件缺陷推荐 `$pen-component`；系统 foundation 问题推荐 `$pen-system`。

完成条件：所有已确认 review lenses 均已覆盖；每个发现都有证据和 scope；最高价值修复项拥有清楚且互不重叠的 owner。
