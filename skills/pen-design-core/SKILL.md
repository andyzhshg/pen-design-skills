---
name: pen-design-core
description: "处理 Pen/pen.dev、`.pen` 与 Pencil MCP 任务的共享工作流（shared workflow）：读取当前状态，针对未解决的设计决策进行访谈，执行有边界的修改，并核验结构与视觉结果。当其他 Pen 命令委派到这里，或用户用中文/英文提出新建设计、修改画布、检查页面、提升质感、构建组件、同步设计与代码等 Pen 请求时使用。"
---

# Pen Design Core：共享设计流程

所有 Pen 命令都执行同一条不变量循环。由调用它的命令决定交付物、写入边界和完成条件。

## 加载对应分支

- 当需求包含真正的设计分叉，或调用命令要求确认 brief 时，读取 [references/interview.md](references/interview.md)。
- 进行任何 `.pen` 体检或修改前，读取 [references/workflow.md](references/workflow.md)。
- 当任务位于已有项目、需要决定 Reuse / Repair / Wrap / Create，或涉及设计—代码真值时，读取 [references/reuse-and-context.md](references/reuse-and-context.md)。
- 当任务授权写入、需要从失败中恢复，或要在中断后续跑时，读取 [references/execution-and-recovery.md](references/execution-and-recovery.md)。
- 当任务检查结构或视觉质量、执行 `$pen-review` / `$pen-polish`，或需要 screenshot 判断时，读取 [references/quality.md](references/quality.md)。
- 当任务执行 Design → Code、Code → Design、token-only sync，或需要记录设计—实现差异时，读取 [references/design-code.md](references/design-code.md)。

## 1. 预检（Preflight）

检查当前会话实际暴露的 Pen/Pencil MCP 工具和编辑器状态。以 live schema 为准；社区 Skill 中的工具名只可作为示例，不是 API contract。

确认当前 `.pen` 文件、selection、目标项目、调用命令和授权写入范围。如果目标文件未打开或 MCP 不可用，报告准确的前置条件并停止。

停止在 Preflight 时，只交付本轮实际观察到的 evidence、所需前置条件和下一步。把用户描述的症状保留为 hypothesis；目标与可观察状态建立前，不确认 diagnosis / design direction，也不声称已完成 screenshot、检查或 comparison。

完成条件：目标文件、目标范围、命令 profile 与可用读写操作全部已知。

## 2. 查清事实（Discovery）

读取能覆盖目标的最小 object-tree 子树。按命令需要检查相关 variables、themes、components、instances、imports、layout、项目设计文档，以及代码侧 tokens / components。为关键结论保留 provenance，并按类别确认 source of truth；不要把项目 inventory 缓存在 Skill 中。

事实由 Agent 负责查明。先从环境寻找证据，再向用户提问。

完成条件：所有能从 Pen、仓库或用户提供的参考资料中查明的问题都有证据。

## 3. 访谈决策（Interview）

把尚未确定的决策组织成 design tree。每轮一次性询问当前 frontier，并为每题给出推荐答案。收到回答后重新计算 frontier。

如果是只有一种合理解释的微小修改，直接声明 target、assumption 和 acceptance check，不启动长访谈。对于设计标准、组件、页面、质感打磨或同步等实质任务，等待 frontier 清空。

完成条件：没有决策被静默假设，且用户确认 design contract。

## 4. 建立设计契约（Design Contract）

汇总 goal、target nodes、需要保留的 invariants、source-of-truth ledger、复用资产与决策、已选方向、授权文件、验收证据和 out of scope。

只有设计系统、重要页面/流程或跨会话工作才默认考虑落盘。遵循项目已有的设计文档约定；没有约定时，先提出位置再写入。

## 5. 执行命令（Execute）

只使用 live MCP 中存在的操作。把每个 mutation batch 作为带 precondition、postcondition 和 checkpoint 的 mini-transaction；通过 Pen/MCP 写入 `.pen`，不要直接编辑 JSON。

完成条件：每个授权 batch 都有 verified checkpoint，且没有未解释的 partial 或 unexpected 状态。

## 6. 核验（Verify）

按 quality evidence ladder 覆盖命令专属 lenses。先读回 structure、layout 与 system 证据，再用最小 screenshot 回答明确的视觉问题；区分 structural fact、risk 与 visual judgment。

完成条件：每个结论都有 evidence、owner 和 acceptance check；写入任务的 before/after 使用同一 scope；主观打磨连续三轮仍未收敛时，索要参考图或更明确的方向。

## 7. 交付（Handoff）

报告已改 nodes/files、结构证据、实际 artifact 支持的视觉证据、刻意保留的差异、剩余风险，以及是否需要先保存设计，磁盘脚本才能观察到结果。没有本轮 screenshot artifact 时明确报告 `not captured`，不要把计划中的截图写成已完成 evidence。

只有调用命令的完成条件已满足，或已经报告具体 blocker 时才结束。
