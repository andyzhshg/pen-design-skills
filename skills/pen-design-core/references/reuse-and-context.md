# 项目 Context 与复用决策

原则：**Skill 保存决策方法，项目保存项目事实。** 运行时从环境建立证据映射，不在 Skill 中缓存 token 值、组件清单、node ID 或目录结构。

## Context Discovery

按需读取，读到足以覆盖目标即停止：

1. active `.pen`：target subtree、variables、themes、components、instances、imports 与邻近命名；
2. 项目约定：`AGENTS.md` / `CLAUDE.md`、设计文档和任务规格；
3. 代码真值：token/theme 配置、component API、states、breakpoints、icons/fonts、tests 与 examples；
4. 用户提供的参考：截图、品牌资料、竞品和 acceptance criteria。

记录每条关键结论的 provenance：来源文件、node ID、文档段落或用户确认。项目文档默认只读；只有调用命令授权且位置符合现有约定时才更新。

## Source-of-Truth Ledger

不要把“设计”或“代码”整体指定为唯一真值。逐类决定：

| 类别 | 常见候选 | 必须确认 |
| --- | --- | --- |
| Design tokens | Pen variables、代码 token、品牌规范 | 权威侧、语义映射、冲突处理 |
| Components | local Pen component、imported library、code component | ownership、API、variants/states |
| Content / behavior | 产品规格、运行代码、设计稿 | 哪一侧代表当前产品行为 |
| Visual direction | 已确认 brief、品牌资料、目标截图 | 哪个 reference 限制构图与质感 |
| Responsive / states | 代码、项目规范、设计 frames | breakpoints、empty/error/loading 等覆盖范围 |

有冲突时把它变成 design frontier 问题；无冲突时直接在 design contract 中记录映射。

## Reuse Ladder

按此顺序寻找候选：

1. 当前项目已有 local variables / components；
2. 项目已采用的 imported design library；
3. 代码侧已有 component / token counterpart；
4. 新建资产。

对候选逐项检查：semantic role、structure/API、variants/states、token/theme model、responsive behavior、ownership/editability、code mapping 与 accessibility。视觉相似本身不构成复用理由。

## 四种决策

- **Reuse**：语义、API/结构、状态和 token 模型匹配；直接使用 instance 或既有资产。
- **Repair**：它本来就是同一资产，缺陷属于当前写入范围且本地可维护；修复 source，再让 instances 继承。
- **Wrap / Extend**：基础语义和结构可复用，但 slot、API 或局部状态不同；保留来源，用 wrapper/composition 表达差异。
- **Create**：没有兼容资产、来源不可修改，或语义/API 差异足以形成独立概念；创建前记录不复用的具体原因。

一次性页面结构可以保留为 frame；只有重复、传播或稳定 API 需要时才 componentize。避免为了“整齐”抽象没有复用收益的结构。

## Context Brief

复杂或跨会话任务在 design contract 中保留精简 context brief：

```markdown
Evidence: 关键来源与定位
Authority: 各类别的 source of truth
Reuse map: Reuse / Repair / Wrap / Create 及理由
Conflicts: 已解决方式或待用户决定项
Write scope: 授权文件与 nodes
Acceptance: 结构、视觉或测试证据
```

引用来源，不复制完整 inventory。只有项目已有明确文档位置且本轮需要跨会话保存时才落盘。

## 完成条件

- 每个复用资产都能追溯来源和 compatibility 判断；
- 每个新建资产都有“为什么现有候选不兼容”的证据；
- 每类真值冲突已解决或进入 frontier；
- 没有静默创建平行 token 或 component system。
