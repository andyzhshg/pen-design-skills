---
name: ask-pen
description: "选择适合当前 Pen 设计任务的显式命令（Choose the right Pen command）。"
---

# Ask Pen：命令导航

只负责选择流程，不执行被选中的命令。

| 命令 | 适用任务 | 交付结果 |
| --- | --- | --- |
| `$pen-system` | 新建或演进 variables、themes、组件政策、命名和长期设计标准 | 一套连贯的设计系统基线 |
| `$pen-component` | 构建或改进一个可复用组件或紧密组件族 | 组件及其必要状态通过核验 |
| `$pen-page` | 根据已确认需求与复用资产组装新页面或流程 | `.pen` 中通过核验的页面 |
| `$pen-review` | 在不修改文件的前提下诊断结构、维护性、层级或视觉质感 | 按优先级排列、有证据的问题报告 |
| `$pen-polish` | 在确认方向后改善现有页面 | 有明确边界的视觉打磨 |
| `$pen-sync-code` | 双向对齐 Pen variables / components / layout 与项目代码 | 已映射、已核验的设计—代码变更 |

只有在两个命令都合理时，才问一个路由问题。推荐其中一个命令，并用一句话解释边界。

常见分叉：

- 先诊断、再修改：先用 `$pen-review`；接受方向后再用 `$pen-polish`。
- 缺少基础还是只缺一个组件：共享规则用 `$pen-system`；单个复用单元用 `$pen-component`。
- 在 `.pen` 中做视觉探索还是写可抛弃代码：前者用 `$pen-page`；后者使用项目里的 `prototype` Skill。

当用户知道该调用哪个命令以及原因时结束。
