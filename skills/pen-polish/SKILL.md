---
name: pen-polish
description: "确认视觉方向后打磨现有 Pen 页面（Polish an existing Pen page）。"
---

# Pen Polish：页面打磨

使用 `$pen-polish` frontier 运行 `$pen-design-core`。

负责对现有页面进行有边界的 refinement。把用户描述的症状作为 hypothesis；先读回准确 target，并用实际 structure 与聚焦 screenshot 诊断首要 failure class：busy、empty、generic、weak hierarchy、inconsistent craft 或 responsive failure。目标或视觉证据不可用时停止在 Preflight，不提前确认修改方向。随后确认应该出现的替代信号、需要保留的 invariants 和允许的修改深度。

只修改诊断所对应的杠杆。除非用户明确扩大 scope，否则保持 structure、behavior 与 design-system contracts 稳定。问题尚未确定时先用 `$pen-review`。

完成条件：目标问题明显减弱；结构检查仍然通过；聚焦 before/after evidence 支持结论；剩余差异均为刻意保留。主观打磨三轮仍不收敛时停止，并索要更明确的 reference 或方向。
