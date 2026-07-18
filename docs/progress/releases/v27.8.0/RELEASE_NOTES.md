# Agentmd Plan v27.8.0

## 中文

`v27.8.0` 为持续运行的 Goal 增加冻结完成契约，阻止自动续跑把可选边界、验收工具加固和更强证明不断变成必做工作。

### 主要内容

- 全局纲要增加 Goal 完成契约门禁。
- 新增按需加载的 `goal-mode-closure.md`。
- 完成条件限制为 3-5 条可观察标准，并显式记录非目标和固定验证预算。
- 新发现只有在契约失败、当前改动回归或重大安全风险时才进入当前 Goal。
- 增加一次探测、禁止递归加固、无进展断路器和自动 `complete`。
- guardrail 和单元测试验证全局门禁及关键停止锚点。

### 升级说明

同时安装 `artifacts/AGENTS-27.8.0.md` 与 `skills/seer-codex-rules/`。Goal reference 只在持续 Goal 创建、恢复、自动续跑或关闭时加载，普通任务不增加上下文成本。

## English

`v27.8.0` adds a frozen Completion Contract for persistent Goals so auto-continuations cannot keep turning optional edges, acceptance-tool hardening, and stronger hypothetical proof into required work.

### Highlights

- The global outline adds a Goal Completion Contract gate.
- New on-demand `goal-mode-closure.md` guidance.
- Completion is limited to 3-5 observable criteria with explicit non-goals and a fixed validation budget.
- New findings enter the current Goal only for contract failures, current-change regressions, or material safety risks.
- One-probe, no-recursive-hardening, no-progress circuit-breaker, and automatic `complete` rules.
- Guardrail anchors and unit tests protect the global gate and critical stopping semantics.

### Upgrade Notes

Install both `artifacts/AGENTS-27.8.0.md` and `skills/seer-codex-rules/`. Load the Goal reference only when a persistent Goal is created, resumed, auto-continued, or closed; ordinary tasks incur no added context cost.
