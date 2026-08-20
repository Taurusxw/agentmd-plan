# Agentmd Plan v29.1.0

## 中文

`v29.1.0` 减少没有真实消费者的哈希、checksum 和 manifest 工作，并把 post-release 的 permission-aware 多 Agent 派遣及当前 Codex `[agents]` 配置语义纳入正式版本。

### 主要内容

- 普通任务默认不生成完整性元数据；只有字节一致性验收存在实际消费者时才计算一次。
- 哈希不能替代语义、来源、行为、测试或视觉证据；同步与恢复只做一次最终一致性比较。
- 子 Agent 不再默认生成 checksum manifest，mismatch 不得启动重复哈希调试循环。
- 可移植模板使用官方 `[agents].max_concurrent_threads_per_session = 31`，schema-only V2 只保留兼容识别和明确警告。
- 每次派遣记录 capability scope、父任务实际权限、观测来源和相容性结论，并加入波次预算、边际证据停止门与首轮通过/返工记录。
- 当前检出树仅保留 `v29.1.0` 版本化资产和本地 tag；GitHub 保留旧 tags/Releases，Git 历史不改写。

### 升级说明

安装 `artifacts/AGENTS-29.1.0.md`、`skills/seer-codex-rules/` 与 `config/` 中的 `[agents]`/角色模板。新任务会加载更新后的全局规则和 Skill；静态路由检查不能替代每次派遣前的 live permission 检查。

## English

`v29.1.0` removes hash, checksum, and manifest work that has no real consumer, and formally releases the post-release permission-aware dispatch contract and current Codex `[agents]` configuration semantics.

### Highlights

- Ordinary tasks generate no integrity metadata by default; compute it once only when byte identity has an explicit acceptance consumer.
- Hashes cannot replace semantic, provenance, behavioral, test, or visual evidence; synchronization and recovery use one final comparison.
- Subagents do not create checksum manifests by default, and a mismatch cannot start a repeated hash-debug loop.
- The portable template uses the documented `[agents].max_concurrent_threads_per_session = 31`; schema-only V2 remains a warned compatibility input.
- Each dispatch records capability scope, observed parent permissions, observation source, and compatibility decision, with wave budgets, marginal-evidence stop gates, and first-pass/rework accounting.
- The checkout retains only `v29.1.0` versioned assets and the local tag; GitHub keeps historical tags/Releases, and Git history is not rewritten.

### Upgrade Notes

Install `artifacts/AGENTS-29.1.0.md`, `skills/seer-codex-rules/`, and the `[agents]`/role templates under `config/`. A new task loads the updated global rule and Skill; static routing validation does not replace a live permission check before each spawn.
