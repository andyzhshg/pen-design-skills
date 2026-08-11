---
name: pen-sync-code
description: "按照已确认方向对齐 Pen 设计与项目代码（Align Pen design and code）。"
---

# Pen Sync Code：设计—代码同步

使用 `$pen-sync-code` frontier 运行 `$pen-design-core`。

负责 design → code、code → design 或 token-only reconciliation。写入前读取两侧，并使用 [design-code.md](../pen-design-core/references/design-code.md) 建立 mapping contract。逐类决定 authority；source-of-truth 冲突交给用户决定。

遵守已确认的 framework、styling system、libraries、file scope、public APIs 与 tests。同一阶段只写一个 target side，优先使用最小 diff 和已有 abstractions。广泛视觉探索转给 `$pen-page` 或 `$pen-polish`；本命令负责同步，不负责开放式 redesign。

完成条件：所有 in-scope mapping 都已分类并应用；target native checks 通过；固定条件下的聚焦视觉对照完成；intentional / unsupported 差异进入 divergence ledger；未授权 side 保持不变。
