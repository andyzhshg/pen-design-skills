# 设计访谈（Design Interview）

使用 design tree。只有前置条件已经确定的决策才能进入 **frontier**。

## 规则

1. 从 Pen、仓库和用户提供的参考资料中查明事实。向用户询问决策，不询问可以查到的信息。
2. 一轮询问当前 frontier 上的全部问题。依赖尚未解决问题的分支留到后续轮次。
3. 每个问题都给出推荐答案和真正影响选择的 trade-off。
4. 微小修改保持轻量：当文件与请求共同支持唯一解释时，声明它，不启动访谈。
5. Frontier 清空且用户确认 design contract 前，不做实质写入。`$pen-review` 在确认后仍保持只读。

每个问题使用以下格式：

```markdown
❓ **Q1 — 问题标题**：需要决定的内容与相关选项。

➡️ 推荐答案，以及推荐原因。
```

## 各命令的 Frontier

### `$pen-system`

- 当前 source of truth 是代码 tokens、已有 `.pen`、设计库还是新 brief？
- 系统需要服务哪些平台、themes、density modes 和 accessibility constraints？
- 本轮包含哪些 semantic roles 和 component families？
- 哪些命名与 code mapping 约定必须保持稳定？
- 长期设计决定保存在哪里？

### `$pen-component`

- 组件承担什么 user job 和 semantic role？
- 哪些内容固定，哪些是 property，哪些是 slot？
- 当前必须覆盖哪些 variants 与 states？
- 必须复用哪些已有 variables、components 和代码 API？
- 用什么证据证明各状态已经完整？

### `$pen-page`

- 页面服务谁，哪个 primary action 应占据第一层级？
- 必须呈现哪些真实 content、states 和 responsive targets？
- 已有哪些页面结构与 components 必须复用？
- 哪个 visual direction 或 reference 限制页面构图？
- 哪些内容不能改变，什么视觉与结构证据代表完成？

### `$pen-review`

- 体检的准确 scope 是什么？
- 优先检查 maintainability、design-system consistency、usability、accessibility、visual quality，还是它们的排序组合？
- 使用哪个项目标准或参考作为 comparison source？

### `$pen-polish`

- 首要问题属于 busy、empty、generic、weak hierarchy、inconsistent craft 还是 responsive failure？
- 应该用什么 mood、brand signal 或 reference 替代当前表现？
- 哪些 structure、content 与 interaction 必须保持不变？
- 允许多大程度的视觉变化？
- 什么可见结果代表“已经足够”？

### `$pen-sync-code`

- 方向是 design → code、code → design，还是 token-only sync？
- token、component 和 behavior 冲突时，各自以哪一侧为准？
- 使用哪个 stack、styling system、component library 与 icon library？
- 哪些 files、public APIs、states 和 breakpoints 必须稳定？
- 哪些 tests 与 visual comparisons 能证明已经对齐？

## Design Contract

执行前汇总：

```markdown
目标（Goal）：
目标范围（Target）：
真值来源（Source of truth）：
复用资产（Reuse）：
已选方向（Direction）：
必须保留（Preserve）：
授权写入（Authorized writes）：
验收证据（Acceptance evidence）：
本轮不做（Out of scope）：
```
