---
name: pen-component
description: "构建或改进一个可复用 Pen 组件或组件族（Build or refine a reusable component）。"
---

# Pen Component：组件构建

使用 `$pen-component` frontier 运行 `$pen-design-core`。

负责一个 reusable component 或一个紧密耦合的组件族。写入前检查它的 semantic role、anatomy、properties、slots、variants、states、variable bindings、已有 Pen instances 和代码侧 API。

复用当前设计系统。如果缺少 foundation，准确报告 gap，不静默创建平行系统。广泛 foundation 工作转给 `$pen-system`，页面构图转给 `$pen-page`。

完成条件：每个已确认 state 都有正确结构和 bindings；适合时至少核验一个代表性 instance；聚焦 screenshot 与结构检查结论一致。
