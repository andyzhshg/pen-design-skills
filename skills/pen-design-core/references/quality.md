# 结构与视觉质量（Quality）

原则：**cheap-first，证据先于建议。** 先用 object tree、resolved layout 和 bindings 回答确定性问题，再用一张聚焦 screenshot 回答视觉问题。脚本只发现 candidates，不替代设计判断。

## Evidence Ladder

按顺序执行，前一级已足以回答时不升级成本：

1. **Structure**：hierarchy、node type、names、component/instance relationships；
2. **Layout**：resolved bounds、fit/fill、alignment、gap/padding、overflow、clipping、text growth；
3. **System**：variables、themes、literal drift、duplicate tokens、instance reuse、state coverage；
4. **Product**：真实 content、behavior、responsive targets、empty/loading/error states、accessibility signals；
5. **Visual**：聚焦 screenshot 中的 hierarchy、density、balance、rhythm、brand signal 与 craft；
6. **Comparison**：与 confirmed brief、reference 或 before state 对照。

截图前先写出它要回答的问题和最小 scope。一个视觉里程碑使用一张聚焦图；object tree 能回答的问题不靠截图猜。只把本轮实际观察到的结果称为 evidence；尚未执行的 screenshot、audit 或 comparison 明确标为 next check。

Screenshot evidence 必须对应本轮工具实际返回的 image artifact，并标明 target node / region。没有 artifact 时写 `Screenshot: not captured`，只列入 blocker 或 next check；不得出现在 Reads、已完成检查或 visual evidence 中。

## Review Lenses

按调用命令确认的 scope 覆盖相关 lenses：

- **Integrity**：broken refs、invalid bindings、unexpected literals、duplicate assets、naming drift；
- **Layout**：overlap、clipping、overflow、unstable sizing、misalignment、broken reflow；
- **Coverage**：themes、variants、interaction states、responsive frames、content extremes；
- **Accessibility**：contrast candidates、text legibility、target size、focus/error/disabled signals；
- **Hierarchy**：第一、第二、第三视觉落点是否符合 product priority；
- **Craft**：spacing rhythm、radius、type scale、icon style、border/shadow strength 是否一致；
- **Identity**：真实内容与品牌信号能否区分产品，是否仍是 generic template。

## Failure Classes

| Class | 主要信号 | 第一杠杆 |
| --- | --- | --- |
| Busy | 注意力竞争者过多、强调信号泛滥 | **Pare**：删除或降级最弱竞争者 |
| Empty | 信息纹理和视觉锚点不足 | 增加真实 content / metadata / anchor |
| Generic | 选择安全但缺乏产品特征 | **Amplify**：强化一个品牌或构图信号 |
| Weak hierarchy | 多个元素争夺第一层级 | 重排尺度、位置、对比和 primary action |
| Inconsistent craft | spacing、type、icon、surface 漂移 | **Finalise**：统一系统细节 |
| Responsive failure | 小尺寸仅被压缩，内容与导航未重排 | 改变 composition 与 priority |

一次 polish 只处理一个 primary class。强度太高但元素应保留时使用 **Soften**，不要误用 Pare。

## Finding Contract

每个发现使用：

```markdown
Lens / Severity:
Evidence: node、property、bounds、screenshot region 或 comparison
Fact or judgment: structural fact | risk | visual judgment
Impact / propagation:
Owner: system | component | page | code
Repair lever:
Acceptance check:
```

按 user impact、propagation risk、evidence confidence 和 repair cost 排序。不要用伪精确总分掩盖判断。

## Review 与 Polish

- `$pen-review` 保持 read-only：覆盖已确认 lenses，输出有 owner 的优先发现，不执行 repair。
- `$pen-polish` 先确认 primary failure class、替代信号和 preserve invariants；只修改对应杠杆，并用同一 ladder 验证 before/after。
- 系统性问题交给 `$pen-system`，组件 source 问题交给 `$pen-component`，代码映射问题交给 `$pen-sync-code`。

## Read-only Audit Script

当磁盘 `.pen` 已保存且需要全量统计时运行：

```bash
python3 <pen-design-core-directory>/scripts/audit_pen.py path/to/file.pen
python3 <pen-design-core-directory>/scripts/audit_pen.py --mode contrast path/to/file.pen
```

脚本读取明文 JSON，只报告 structure/token/contrast candidates；resolved layout、imports 语义和最终视觉仍以 live Pen/MCP 为准。脚本观察磁盘文件，MCP 观察 editor memory；运行前确认保存边界。

完成条件：所有已确认 lenses 都有证据；事实与视觉判断分开；最高优先发现拥有 owner、repair lever 和 acceptance check；截图数量与问题一一对应。
