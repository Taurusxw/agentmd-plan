# AGENTS.md 3.2.0 补丁说明

本次发布将未发布候选 `30.2.0` 按维护者要求重编号为 `3.2.0`。版本线归一不改写历史 tags、Releases 或 Git 提交。

## 行为改进

1. 用户要求的交付物优先；计划、状态、测试、审计、manifest、hash 和文档只能作为支持证据。
2. 用户或权威证据纠正前提后，立即作废所有依赖旧前提的假设、计划、结论、待执行动作和验证结果，只重建受影响路径。
3. 新文件、抽象、fallback、泛化边界和额外功能必须由当前契约、复现失败、既有项目惯例或重大风险支持。
4. 请求结果和固定验收通过后停止；无相关失效或用户扩展时，不再写入、复核、重验或继续优化。
5. 最终与状态输出以结果和必要证据为主，省略例行工具叙述、重复规则/状态、泛化称赞、道歉、安慰和无用收尾。

## Skill 配套

- `execution-standards.md` 区分真实交付、必要证据和可选流程，并定义纠正失效链。
- `goal-mode-closure.md` 禁止用计划、测试或报告替代 Goal Outcome。
- `acceptance-closure.md` 增加最终验证后的 mutation barrier。
- `verification-and-reporting.md` 明确证据不能掩盖未完成交付，并收紧低价值输出。
- guardrail 与定向测试固定上述全局和 Skill 语义锚点。

## 发布边界

- 本地检出树、artifact、release 目录和本地 tag 只保留 `3.2.0`。
- Git 历史与 GitHub 历史 tags/Releases 保留，不做强推或历史重写。
- live 全局规则、Downloads 副本和维护环境 Skill 同步到 `3.2.0`；当前任务不假设热重载。
- 独立 Skills 分发仓库、Nature 工作和历史多 Agent 压测不属于本次发布。
