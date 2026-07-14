# Agentmd Plan v27.6.0

## 中文

`v27.6.0` 是 Agentmd Plan 的首个正式 GitHub Release。它将全局 `AGENTS.md` 收缩为始终生效的低 token 纲要，并把详细执行规则交给 `seer-codex-rules` 按需加载。

### 主要内容

- 92 个非空行的精简全局纲要。
- 所有文件修改任务使用轻量 Skill 门禁。
- L0-L4 任务分级和 G0-G4 guardrail 分级。
- round 按日期重置、容量整理和 phase/release 升级规则。
- 验收预算、重复验证停止条件和边界条件开发准入门槛。
- 全局规则体量、Skill 路由、同步状态和恢复快照脚本。
- 独立中文和英文说明书。

### 升级说明

升级前备份现有全局规则和 Skill，然后同时安装 `artifacts/AGENTS-27.6.0.md` 与 `skills/seer-codex-rules/`。不要只替换其中一个，否则覆盖锚点和详细规则可能不一致。

## English

`v27.6.0` is the first formal GitHub Release of Agentmd Plan. It reduces the global `AGENTS.md` to a low-token always-on outline and delegates detailed execution rules to the on-demand `seer-codex-rules` Skill.

### Highlights

- A concise global outline with 92 non-empty lines.
- A lightweight Skill gate for every file-changing task.
- L0-L4 task levels and G0-G4 guardrail tiers.
- Date-scoped round numbering, capacity organization, and phase/release promotion.
- Acceptance budgets, repeated-validation stop conditions, and an admission gate for edge-condition development.
- Scripts for rule size, Skill routing, synchronized state, and recovery snapshots.
- Separate Chinese and English manuals.

### Upgrade Notes

Back up the existing global rules and Skill, then install both `artifacts/AGENTS-27.6.0.md` and `skills/seer-codex-rules/`. Replacing only one side can leave coverage anchors and detailed rules out of sync.
