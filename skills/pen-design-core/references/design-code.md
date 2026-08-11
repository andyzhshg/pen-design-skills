# Design ↔ Code Reconciliation

原则：**同步是 reconciliation，不是复制。** 先建立 mapping contract，再修改单一 target side；按类别选择 authority，不把设计或代码整体宣布为唯一真值。

## Sync Profile

先确认一种方向：

- **Design → Code**：Pen 表达已确认结构与视觉；代码侧实现并保留 stack、public API 和 behavior contracts。
- **Code → Design**：代码表达当前 product behavior；Pen 侧重建设计表示并保留 semantic API、states 与 responsive rules。
- **Token-only**：只对齐 variables/tokens，不顺带重写 components 或 pages。

明确 source side、target side、授权 files/nodes、stack、checks 和 visual comparison scope。同一批次只写一个 side；双向改动拆成两个已确认阶段。

## Mapping Contract

为每个 in-scope 项记录：

```markdown
Category / semantic role:
Pen source: variable、component、node 或 theme
Code source: token、component、API 或 file
Authority: Pen | code | project spec | user decision
Transform: naming、units、composition 或 state mapping
Status: exact | mapped | intentional divergence | unsupported | conflict
Target write:
Verification:
```

`exact` 表示语义与表示一致；`mapped` 表示语义一致但表示需要转换；`intentional divergence` 必须有原因；`unsupported` 记录工具或平台缺口；`conflict` 进入 design frontier。

## Category Rules

### Tokens / Variables

按 semantic role 与 type 映射，再比较 theme values。允许明确的 unit/name transform，例如 `16px ↔ 1rem`；保留转换依据。优先复用 target 侧已有 token，近似值先判定是映射、漂移还是新语义。

### Components / APIs

映射 component boundary、props、slots、variants、states、defaults 与 ownership。视觉相似不等于 API 兼容；优先调用 target 侧已有 abstraction。设计无法表达的 runtime behavior 留在 code contract，不伪造成 Pen 属性。

### Layout / Responsive

翻译 layout intent：flow、alignment、gap、container、priority、reflow 与 breakpoint behavior。使用 target stack 的原生布局；不要逐坐标转译，也不要把桌面 frame 等比缩小成移动端。

### Content / States / Assets

使用固定 comparison content 覆盖 default、loading、empty、error、disabled 和 content extremes。复用项目 icons/fonts/assets 并保留 provenance；运行时数据、focus、animation 和 platform-specific behavior 可作为有意差异。

## Reconciliation Loop

1. 盘点两侧 in-scope assets 与项目约定；
2. 逐类确认 authority，生成 mapping contract 与 unresolved conflicts；
3. 用户确认 conflicts、write scope 与 intentional divergences；
4. 按 dependency 顺序应用 target-side mini-transactions：tokens → components → composition → states；
5. 每批在 target native surface 读回并运行 checks；
6. 固定 viewport、theme、state 与 content，做一张聚焦 visual comparison；
7. 更新 mapping status 与 divergence ledger。

## Verification Matrix

| Surface | 证据 |
| --- | --- |
| Code | format/lint、types、tests、build、public API 与 runtime state behavior |
| Pen | variable bindings、component instances、resolved layout、theme/state coverage |
| Shared | 同 viewport/theme/content/state 的 hierarchy、density、type、spacing 与 alignment 对照 |
| Divergence | 每项差异的原因、owner、是否暂时、后续 acceptance |

视觉 comparison 只证明可见结果；tests 只证明已编码 contract。两者都需要。

## Divergence Ledger

记录 `item → reason → authority → owner → permanent/temporary → verification`。合理差异包括 platform convention、accessibility、runtime-only behavior、技术限制和已确认改善。未记录的差异视为 drift。

完成条件：所有 in-scope mapping 均有非 `conflict` 状态；target native checks 通过；聚焦 visual comparison 完成；intentional / unsupported 差异有 ledger；未授权 side 保持不变。
