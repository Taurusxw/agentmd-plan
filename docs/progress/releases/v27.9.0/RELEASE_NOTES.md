# Agentmd Plan v27.9.0

## 中文

`v27.9.0` 增加效率优先、质量有下限的多 Agent 模型路由。普通任务保持单 Agent；只有独立并行、上下文隔离或重大风险复核的收益高于协调与 token 成本时才派遣。

### 主要内容

- 全局纲要增加子 Agent 收益门禁和强制治理 reference 路由。
- 新增 `multi-agent-governance.md`，规定关键路径归属、上下文包、结果契约、并发、写入和生命周期。
- 子 Agent 最低为 Terra/high；探索使用 Terra/high，实现使用 Terra/max，重大风险复核使用 Sol/high；更高强度需用户明确选择。
- 默认并发 1，明确独立时最多 2，配置硬上限 3；禁止嵌套派遣、重复工作和同文件并行写入。
- 新增可移植配置模板、三个自定义 Agent 和确定性路由校验脚本。

### 研究依据

- [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Capable language models can outgrow the benefits of collaboration](https://www.nature.com/articles/s42256-026-01268-y), published 2026-07-24
- [Understanding Agent Scaling in LLM-Based Multi-Agent Systems via Diversity](https://arxiv.org/abs/2602.03794)
- [AutoGen Teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)

### 升级说明

同时安装 `artifacts/AGENTS-27.9.0.md`、`skills/seer-codex-rules/`、`config/agents.toml.example` 中的 `[agents]` 配置和 `config/agents/` 角色文件。重启或新建 Codex 任务后验证角色是否被发现；运行 `agent_routing_check.py --json` 检查 live 路由。

## English

`v27.9.0` adds an efficiency-first multi-agent model router with a strong quality floor. Ordinary work remains single-agent; delegation requires a concrete parallel-time, context-isolation, or material-risk-review benefit that exceeds coordination and token cost.

### Highlights

- The global outline adds a subagent benefit gate and mandatory governance-reference routing.
- New `multi-agent-governance.md` guidance covers critical-path ownership, context packets, result contracts, concurrency, writes, and lifecycle closure.
- Every child starts at Terra/high: exploration uses Terra/high, implementation uses Terra/max, and material-risk review uses Sol/high. Higher effort requires explicit user selection.
- Normal concurrency is one, two is allowed for clearly independent work, and three is the hard configured ceiling. Nested delegation, duplicate work, and concurrent same-file writes are prohibited.
- Portable configuration templates, three custom Agents, and a deterministic routing validator are included.

### Upgrade Notes

Install `artifacts/AGENTS-27.9.0.md`, `skills/seer-codex-rules/`, the `[agents]` settings from `config/agents.toml.example`, and the role files under `config/agents/`. Restart or start a new Codex task so role discovery can refresh, then run `agent_routing_check.py --json` against the live configuration.
