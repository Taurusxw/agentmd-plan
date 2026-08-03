# Agentmd Plan v27.12.0

## 中文

`v27.12.0` 将已安装的全局规则、公开 artifact、Skill 覆盖清单和私有恢复状态重新统一，并增加来源型研究默认进入 Seer Knowledge 的长期路由。

### 主要内容

- 发布与 live 全局规则字节一致的 `artifacts/AGENTS-27.12.0.md`。
- 将全局覆盖矩阵和逐条 inventory 锚定到 `27.12.0` 及其 SHA-256。
- 显式路由 `seer-capture` 的研究与成书工作流，同时保持普通开发输入默认不自动入库。
- 修复 README、进度概览、公开 Skill 和私有恢复状态停留在旧版本造成的 provenance 漂移。
- 保留单 Agent 默认、Terra/high 最低路由、Terra/max 实现和 Sol/high 重大风险复核策略。

### 升级说明

安装 `artifacts/AGENTS-27.12.0.md` 与 `skills/seer-codex-rules/`，按需合并 `config/agents.toml.example` 和 `config/agents/`。安装后运行 README 中的严格 guardrail、模型路由和单元测试命令。

## English

`v27.12.0` reunifies the installed global rules, public artifact, Skill coverage inventory, and private recovery state while adding a durable route that sends source-bearing research to Seer Knowledge by default.

### Highlights

- Publishes `artifacts/AGENTS-27.12.0.md` byte-identical to the live global rules.
- Anchors the global coverage matrix and itemized inventory to version `27.12.0` and its SHA-256.
- Explicitly routes `seer-capture` research and Book workflows while keeping ordinary development inputs out of automatic capture.
- Repairs provenance drift across the manuals, progress overview, public Skill, and private recovery state.
- Preserves the single-agent default, Terra/high minimum routing, Terra/max implementation, and Sol/high material-risk review policy.

### Upgrade Notes

Install `artifacts/AGENTS-27.12.0.md` and `skills/seer-codex-rules/`, then merge `config/agents.toml.example` and `config/agents/` as needed. Run the strict guardrail, model-routing, and unit-test commands documented in the README after installation.
