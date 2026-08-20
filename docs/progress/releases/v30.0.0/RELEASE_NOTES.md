# Agentmd Plan v30.0.0

## Status

Candidate validation and maintainer-environment installation passed. Source commit, Git tag, GitHub Release, and final publication record remain pending.

## 中文

`v30.0.0` 是一次 major 治理候选：匹配的 Skills 照常加载，`seer-codex-rules` 仅在治理敏感情形路由；多 Agent 仅在净收益门禁通过时派遣，并继续保留互斥写入、有效权限核对和紧凑结果契约。

### 主要内容

- 匹配 Skills 照常加载；`seer-codex-rules` 仅用于规则/`AGENTS.md`、版本/progress/文档治理、发布/迁移/全局同步、架构漂移、Goal/验收扩张和多 Agent 等治理敏感工作。普通 L1/L2 与单文件工作不因本地修改而触发它。
- 派遣以独立工作包、实时有效槽位和任务预算为输入；容量不是利用率目标。
- 继续采用默认零哈希边界：完整性比较只服务有明确消费者的字节一致性断言，不能替代语义、来源、行为、测试或视觉证据。
- 自有 Seer 优化覆盖 `seer-capture`、`seer-project-space-health`、`seer-math-exam`、`seer-mathbook` 和 `seer-prepare-open-source-release`，分别收窄普通捕获、深度清理、数学严谨性引用、精确图形实现和开源发布路由。第三方 Skills 保持只读审计。所有 `nature-*` 源码、版本、测试、安装副本和 `.agents` 重复副本均冻结，不属于本次变更；观察结果只可作为未来审计候选。
- 两仓发布路径中的源仓库与独立分发仓库是两项独立的 release target，维护环境安装也必须分别授权和验收；本地 checkout 在授权清理后只保留最新版本化资产，Git/GitHub 历史保持不改写。

## English

`v30.0.0` is a major governance candidate: matching Skills load normally, while `seer-codex-rules` routes only for governance-sensitive work. Multi-agent work dispatches only after the net-benefit gate passes and retains exclusive writes, effective-access checks, and compact-result contracts.

### Highlights

- Matching Skills load normally; `seer-codex-rules` applies only to rules/`AGENTS.md`, version/progress/documentation governance, release/migration/global sync, architecture drift, Goal/acceptance expansion, and multi-agent work. Ordinary L1/L2 and single-file edits do not trigger it merely because they are local changes.
- Dispatch is sized from independent packets, live effective capacity, and task budget; capacity is not a utilization target.
- The default zero-hash boundary remains: integrity comparison serves only an explicit byte-identity consumer and cannot replace semantic, provenance, behavioral, test, or visual evidence.
- Self-owned Seer optimization covers `seer-capture`, `seer-project-space-health`, `seer-math-exam`, `seer-mathbook`, and `seer-prepare-open-source-release`, narrowing ordinary capture, deep-cleanup, mathematical-rigor, exact-figure implementation, and open-source release routing. Third-party Skills remain read-only audit targets. All `nature-*` source, version, test, installed-copy, and `.agents` duplicate-copy assets are frozen and outside this release scope; observations are future audit candidates only.
- The source and separate distribution repositories are independent targets in the two-repository release path, and maintainer-environment installation also requires separate authorization and acceptance. After authorized cleanup, the local checkout retains latest versioned assets only; Git/GitHub history is not rewritten.

## Pending Release Fields

- Candidate validation: pending release-owner evidence.
- Maintainer-environment installation: pending separate authorization and evidence.
- Git commit and annotated tag: pending.
- GitHub Release and publication URL: pending.
