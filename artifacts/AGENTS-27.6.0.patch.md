# AGENTS.md 27.6.0 候选补丁说明

本次候选版本动作：`27.5.1 -> 27.6.0`，属于 `MINOR`。

## 变更原因

全局 `AGENTS.md` 已达到 16 KiB 警戒线，同时详细规则已经由 `seer-codex-rules` 覆盖。候选版将全局文件收缩为始终生效的纲要，并强化所有文件修改型开发任务的轻量 Skill 门禁。

## 修改内容

1. 保留核心原则、指令层级、L0-L4、修改底线、留痕和验证底线。
2. 将详细文档表格、round 模板、代码治理细节和输出模板交给 Skill reference。
3. 将 `seer-codex-rules` 明确为所有文件修改型开发任务的开始/结束合规门禁。
4. 普通开发只加载任务分级和一个产物相关 reference；规则、全局同步和发布才运行完整 guardrail。
5. 增加 Skill 缺失、不可读或校验失败时不得宣称合规完成的失败策略。

## 应用边界

- 当前文件是可移植候选 artifact；使用者应审阅后再安装到自己的 `<codex-home>/AGENTS.md`。
- 用户确认后再备份 live 文件、同步两份副本、更新覆盖清单的来源版本/hash，并刷新当前状态清单和 Skill 快照。

## 验证要求

- 候选文件通过 `measure_rules.py --strict`，并处于全局目标体量范围。
- 五轮语义覆盖检查确认旧版每个全局章节均在候选纲要或 Skill reference 中保留。
- 应用后应验证个人 live 文件、私有同步副本和正式 artifact 的一致性。
- 应用后 `guardrail_check.py --strict`、Skill validator 和当前状态校验通过。
