# Pen Skill Blind Forward Test

目标：检查 Skill 能否在未看到预期结论的全新上下文中，稳定选择流程、遵守授权并产出可验证结果。

## 隔离规则

1. 每个 case 使用全新 Agent context；只提供目标 Skill 路径、case prompt 和最小 fixture。
2. 不提供 `must` / `must_not`、预期 route、已知缺陷或开发讨论记录。
3. 使用 fixture 副本或 read-only target；写入 case 只允许修改明确的临时范围。
4. 保存原始 response、tool trace、diff、screenshots 与 blockers，再由独立评分步骤读取 assertions。
5. case 之间重置 fixture；前一 case 的输出不得成为后一 case 的 context。

## 评分维度

- **Routing**：调用命令与 write boundary 是否正确；
- **Discovery**：是否先查环境事实，避免把查资料的问题推给用户；
- **Decision**：是否只询问真正的 design frontier；
- **Execution**：是否使用 batch contract、readback、checkpoint 与最小 repair；
- **Quality**：是否区分 fact/risk/judgment，并使用聚焦证据；
- **Completion**：是否满足命令完成条件，或报告准确 blocker。

## 运行顺序

先跑六个 primary cases，再增加 adversarial variants：省略 `$command`、要求 review 后自动修复、要求双向同时覆盖、MCP 中断后要求重跑整批、以及中文请求中夹杂英文专业词。

本仓库交付 case 与协议，不附带项目 fixture。只有在用户明确授权新 Agent/线程和测试目标时，才执行 blind forward test；静态 validator 通过不能替代这一层。

## Live Integration

离线 blind test 不能证明 MCP mutation 成功。发布前至少使用 disposable live scope 验证：

1. editor state 与 target discovery；
2. 小批 mutation；
3. 独立 structure/layout readback；
4. 聚焦 screenshot artifact；
5. rejected batch 与 rollback readback；
6. 使用工具返回的 repair/edit ID 做最小修补；
7. 保存、关闭、重开后的 IDs、refs 与 bindings。

将 offline decision-boundary evidence 与 live integration evidence 分开报告。
