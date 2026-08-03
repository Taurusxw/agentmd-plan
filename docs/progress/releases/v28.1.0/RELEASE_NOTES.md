# Agentmd Plan v28.1.0

## 中文

`v28.1.0` 将资料分析与持久化写入明确分离，并把全局 Codex 治理资产收归 `agentmd-plan` 专有项目集中维护，防止一个项目的局部规则变化影响所有其他对话。

### 主要内容

- 截图、文档、媒体、文件、链接、阅读和调研默认只分析，不再自动调用 `seer-capture`。
- 只有当次明确命名的材料被指定 `[入库]`、Knowledge 或具体 Book 时才允许持久化，授权不得跨对话、任务或平台流程继承。
- 全局主 `AGENTS.md`、同步副本和 `seer-codex-rules` 源码/安装副本只允许在 `agentmd-plan` 专有项目内修改。
- 其他项目和对话必须保持只读，输出包含证据、建议差异、版本影响、跨项目风险、验证和回退的变更报告，由用户转交专有项目。
- 禁止通过同步脚本、安装器、恢复任务、自动化、其他 Skill 或子 Agent 绕过所有权门禁。
- guardrail 增加集中所有权锚点、必需 reference 和单元测试。

### 升级说明

安装 `artifacts/AGENTS-28.1.0.md` 与 `skills/seer-codex-rules/`。本次 Git 和 GitHub 发布只包含最终 `28.1.0`，未创建中间 `28.0.0` 提交、tag 或 Release。

## English

`v28.1.0` separates source analysis from persistent writes and centralizes global Codex governance in the dedicated `agentmd-plan` owner project, preventing a local project rule from changing every unrelated conversation.

### Highlights

- Keeps screenshots, documents, media, files, links, reading, and research analysis-only by default instead of invoking `seer-capture` automatically.
- Requires explicit per-material routing to Knowledge or a named Book and prevents authorization carryover across conversations, tasks, or platform workflows.
- Allows writes to the global `AGENTS.md`, synchronized copies, and `seer-codex-rules` source/installations only inside the dedicated `agentmd-plan` project.
- Requires every other project or conversation to remain read-only and return an evidence-backed change report for user-mediated handoff.
- Prohibits bypass through sync scripts, installers, restore tasks, automation, another Skill, or a subagent.
- Adds deterministic guardrail anchors, a required ownership reference, and unit coverage.

### Upgrade Notes

Install `artifacts/AGENTS-28.1.0.md` and `skills/seer-codex-rules/`. This Git and GitHub publication contains only the final `28.1.0`; no intermediate `28.0.0` commit, tag, or Release was created.
