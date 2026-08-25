# Document Index

## Core Documents

| Path | Purpose |
|---|---|
| `../README.md` | 中文项目说明书、安装、验证和隐私边界。 |
| `../README.en.md` | English project manual, installation, validation, and privacy boundaries. |
| `../VERSION` | 当前正式项目版本 `v3.2.0`；验收和公开发布状态见 release record。 |
| `../AGENTS.md` | 本仓库的 Codex 工作规则。 |
| `../CONTRIBUTING.md` | 贡献和验证要求。 |
| `../SECURITY.md` | 私密安全报告流程。 |
| `PROGRESS.md` | 当前公开状态、近期进展和下一步。 |

## Maintained Assets

| Path | Purpose |
|---|---|
| `../artifacts/AGENTS-3.2.0.md` | 已验收、安装并公开发布的 `v3.2.0` 全局规则。 |
| `../config/` | 可移植的多 Agent 默认配置和角色模板。 |
| `../skills/seer-codex-rules/` | 可安装的 Skill 源码。 |
| `progress/rounds/` | 有长期价值的公开开发记录。 |
| `progress/releases/v3.2.0/` | `v3.2.0` 正式发布说明与验收记录。 |

## Recent Governance Record

- `progress/rounds/2026-08-25-round-001-gpt-5p6-output-discipline.md`：将 GPT-5.6 过度生产反馈收束为结果优先、纠正失效、复杂度门禁和达标硬停止。
- `progress/rounds/2026-08-20-round-001-integrity-evidence-governance-29.1.0.md`：将普通任务改为默认零哈希，并限制同步/恢复场景只做一次最终一致性证明。
- `progress/rounds/2026-08-20-round-002-release-30.0.0-governance.md`：冻结 major 候选的路由基线、验证计划、两目标发布边界和 Nature 排除项。
- `progress/rounds/2026-08-16-round-001-current-codex-subagent-governance.md`：记录当时的容量键、派遣权限证据、波次停止门和真实任务评测；容量与模型配置均为历史资料，非当前默认值。
- `progress/rounds/2026-08-11-round-001-handover-lifecycle-permission-aware-dispatch.md`：冻结已消费的交接快照，并为子 Agent 派遣增加父任务实时 permission mode 门禁与静态非证明信号。
- `progress/rounds/2026-08-04-round-001-agent-first-multi-agent-governance-29.0.0.md`：以显式非 Ultra 授权、自适应 V2 fan-out、多模型分工和单位有效结果 token 控制取代固定单 Agent/1-3 上限。
- `progress/rounds/2026-08-03-round-004-latest-effective-global-rule-28.2.0.md`：定义宿主加载优先的最新有效规则，阻止旧上下文降级和最高版本号自主切换。
- `progress/rounds/2026-08-03-round-003-centralized-governance-ownership-28.1.0.md`：将持久化改为逐项授权，并限制全局主规则和治理 Skill 只能由专有项目直接维护。
- `progress/rounds/2026-08-03-round-002-gpt-5p6-execution-efficiency.md`：收紧重复验证、权限确认和安全复核，形成 GPT-5.6 证据预算。
- `progress/rounds/2026-08-03-round-001-provenance-sync-27.12.0.md`：修复 live/public/private provenance 漂移并完成正式发布。
