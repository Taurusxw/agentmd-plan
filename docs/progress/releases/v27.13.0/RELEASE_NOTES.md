# Agentmd Plan v27.13.0

## 中文

`v27.13.0` 面向 Codex 与 GPT-5.6 的长流程开发效率，减少重复权限确认、重叠回归测试和无真实触发条件的安全复核，同时保留 sandbox、approval、CI 与发布门禁等运行时安全边界。

### 主要内容

- 将修改、构建、修复和优化请求视为目标范围内本地编辑与非破坏性验证的一次授权。
- 建立 V0 直接、V1 行为、V2 受影响范围、V3 全量发布验证阶梯，低层证据足够时立即停止升级。
- 缓存已通过证据，只有覆盖面被相关代码、测试、配置、依赖、生成输入或环境变化失效时才重跑。
- 仅在共享核心、公开接口、数据、依赖、构建或真实信任边界变化时触发全量回归或安全专项。
- 让 Goal 成为持续任务的唯一迭代预算，消除 Skill 重读、双重验收预算和机械多轮覆盖审计。
- 保留单 Agent 默认、Terra/high 最低路由、Terra/max 实现和 Sol/high 重大风险复核策略。

### 升级说明

安装 `artifacts/AGENTS-27.13.0.md` 与 `skills/seer-codex-rules/`。按需合并 `config/agents.toml.example` 和 `config/agents/`，然后运行 README 中的严格 guardrail、模型路由和单元测试命令。

## English

`v27.13.0` improves long-running development efficiency for Codex with GPT-5.6. It reduces repeated permission prompts, overlapping regression runs, and security reviews without a real trigger while preserving runtime boundaries such as sandboxing, approvals, CI, and release gates.

### Highlights

- Treats change, build, fix, and optimization requests as one authorization for in-scope local edits and non-destructive validation.
- Adds a V0 direct, V1 behavioral, V2 affected, and V3 full-release validation ladder that stops when lower evidence is sufficient.
- Reuses passing evidence until a relevant code, test, configuration, dependency, generated-input, or environment change invalidates its coverage.
- Triggers full regression or dedicated security review only for shared-core, public-contract, data, dependency, build, or actual trust-boundary changes.
- Makes Goal mode the sole iteration budget for persistent work and removes Skill rereads, duplicate acceptance budgets, and mechanical multi-round coverage audits.
- Preserves the single-agent default, Terra/high minimum routing, Terra/max implementation, and Sol/high material-risk review policy.

### Upgrade Notes

Install `artifacts/AGENTS-27.13.0.md` and `skills/seer-codex-rules/`. Merge `config/agents.toml.example` and `config/agents/` as needed, then run the strict guardrail, model-routing, and unit-test commands documented in the README.
