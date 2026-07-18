# Progress

## Current State

- 当前项目发布版本为 `v27.8.0`，包含已验证的全局纲要和配套 Skill。
- `seer-codex-rules` 已作为可浏览源码纳入仓库。
- 项目采用 MIT License，并完成首次公开发布净化。

## Recent Progress

- 增加 Goal 模式冻结完成契约、必做工作准入、一次探测、禁止递归加固和无进展断路器。
- guardrail 现在校验全局“完成契约”门禁以及 Goal reference 的关键停止锚点。
- 增加累计架构漂移门禁：结合近期 round/Git 热点、规模、宽接口和同目录重复逻辑判断，不以行数单独要求拆分。
- 增加 `structure_check.py` 和独立单元测试，并在真实多轮项目中验证热点识别。
- 增加独立中英文说明书、项目版本文件和 `v27.6.0` release 文档。
- 将活动全局规则从 `27.5.1` 切换到 `27.6.0`，同步配套 Skill 覆盖清单和护栏脚本。
- 为 `seer-codex-rules` 增加边界条件准入门槛和 L1-L4 加固预算，阻止假设性边界持续扩大当前任务。
- 将全局规则压缩为纲要，将详细治理流程下沉到 Skill references。
- 增加低 token guardrail、覆盖检查、体量测量和私有状态快照脚本。
- 移除公开历史中的本机路径、私有备份、live 状态和二进制快照。
- 增加 README、LICENSE、CONTRIBUTING 和 SECURITY 基础社区文件。

## Next Steps

- 根据实际使用反馈继续完善跨平台路径和安装体验。
- 根据跨语言项目反馈扩展结构信号解析，同时保持事件触发和人工语义复核。
- 仅在有明确收益时增加 GitHub 安全和社区自动化。

## Risks

- 规则系统仍依赖 Codex 正确触发 Skill；脚本和最终披露用于降低而非消除偏移。
- `27.8.0` 是可复用正式版本，文字门禁可以显著降低目标漂移，但无法替代平台 Goal 状态机和用户范围决策。

## Detailed Records

- `docs/progress/releases/v27.8.0/RELEASE_NOTES.md`
- `docs/progress/rounds/2026-07-18-round-002-goal-mode-closure.md`
- `docs/progress/rounds/2026-07-18-round-001-architecture-drift-gate.md`
- `docs/progress/rounds/2026-07-14-round-002-activate-global-27.6.0.md`
- `docs/progress/rounds/2026-07-14-round-001-edge-condition-scope-gate.md`
- `docs/progress/rounds/2026-07-13-round-001-public-open-source-release.md`
