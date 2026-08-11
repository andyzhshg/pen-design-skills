# 小批执行与恢复（Execution and Recovery）

把每个 mutation batch 视为可验证的 **mini-transaction**：

```text
Observe → Plan → Mutate → Read back → Checkpoint
```

只有 postcondition 读回通过的 batch 才算完成。Mutation 通常不是 idempotent；重试前先证明它没有产生副作用。

## Batch Contract

每个 batch 在执行前明确：

```markdown
Intent: 这一批只改变什么
Targets: 准确 node IDs / variables / files
Preconditions: 执行前必须为真的状态
Operation: live MCP schema 中的最小操作
Postconditions: 读回后必须观察到的结果
Write scope: 允许影响的边界
```

按语义切 batch，不按任意 node 数量切。通常依次处理 foundations、skeleton/layout、content/states、surface；一个 batch 只承担一种连贯变化，并能独立检查和修补。

创建或插入前先检查预期资产是否已存在。保留工具返回的 node ID、operation ID、error 或 repair identifier，供 readback 与恢复使用。

## Checkpoint Ledger

每批结束立即记录最小 ledger：

```markdown
Batch: B3 — Add empty state
Evidence before: target 与 preconditions
Operation ref: 工具返回标识
Evidence after: postconditions 的读回结果
Status: verified | partial | rejected | blocked
```

短任务保留在会话；跨会话任务才写进项目已有的工作记录。Checkpoint 引用证据，不复制完整 object tree。

## Failure Triage

| 状态 | 证据 | 下一步 |
| --- | --- | --- |
| Rejected | 操作报错且读回无变化 | 修正 input，只重试失败操作 |
| Partial | 仅部分 postconditions 成立 | 盘点已应用子集，补最小差异 |
| Wrong result | 操作成功但 contract 不满足 | 分类偏差，做有边界的 forward fix |
| Stale target | node ID / selection / file 已变化 | 重新 discovery，重建 target mapping |
| Tool unavailable | MCP、文件或编辑器状态不满足 | 保存 checkpoint，报告准确前置条件 |
| Ambiguous | 无法证明是否产生副作用 | 停止 mutation，先恢复可观察状态 |

恢复优先使用 forward repair。只有 rollback 目标明确、不会覆盖用户后续修改且 live tool 支持时才回滚；否则把选择交给用户。

## Recovery Protocol

1. 保留原始 error、operation ref 与最近 verified checkpoint。
2. 重新读取 target scope；把实际状态与 postconditions 逐项对照。
3. 标记 applied、missing、unexpected 三类差异。
4. 为 missing / unexpected 生成最小 repair batch。
5. 读回 repair 结果；通过后新增 checkpoint，再继续后续 batch。

Readback 未证明“零副作用”时，不重放整个 batch。Create、insert、duplicate、append 等操作尤其容易重复资产。

## Resume Protocol

上下文中断或换会话后：

1. 重新确认 active file、项目与授权 scope；
2. 读取 design contract 和最后一个 checkpoint；
3. 验证旧 node IDs，失效时根据 provenance 重新映射；
4. 读回最后一个 verified postcondition，确认项目未漂移；
5. 从第一个 unverified batch 继续，而不是从计划开头重放。

外部脚本读取磁盘时，明确 editor memory 与 saved file 的边界；需要磁盘证据就先完成安全保存，再运行检查。

## 停止条件

遇到 write scope 不明确、状态 ambiguous、恢复可能覆盖用户修改、工具要求用户完成前置动作，或连续 repair 仍无法建立稳定 readback 时，停止写入并交付 checkpoint 与 blocker。

完成条件：所有授权 batch 都有 verified postcondition；ledger 中没有未解释的 partial / unexpected 状态；handoff 能从证据还原当前结果和下一步。
