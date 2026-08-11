# Pen 发现与核验（Discovery and Verification）

## 工具真值（Tool Truth）

执行前检查 live Pen/Pencil MCP schema。当前官方流程可能把 editor state 单独暴露，并把读写操作组合在一个 execute 类工具中；社区 Skills 可能使用其他工具名。工具名变化时保留工作流，不保留过期语法。

如果 MCP 要求先打开 `.pen` 文件，把它作为明确前置条件。写入使用 MCP/Editor 操作；直接解析 JSON 只用于 read-only analysis。

## Discovery 顺序

1. Active file 与 selection
2. Target subtree 与 resolved layout
3. 已有 variables、themes、components、instances 与 imports
4. 相关设计文档，以及代码侧 tokens / components
5. Gaps、conflicts 与 reuse candidates

## Verification Ladder

1. 读回已修改 nodes 与 properties。
2. 检查 layout bounds、overflow、clipping、text growth 与 container sizing。
3. 检查 variable bindings、component instances、命名与项目 invariants。
4. 截取一张聚焦 screenshot。
5. 与已确认的 design contract 对照。
6. 记录刻意差异与剩余风险。

体检任务只执行这条 read-only ladder。写入任务在每个 mutation batch 后执行同样的 readback；批次切分、checkpoint 与失败恢复见 `execution-and-recovery.md`。
