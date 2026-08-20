# Progress

## Current State

- `VERSION`、当前检出树、公开 artifact、live/Downloads、治理 Skill、Git tag 和 GitHub Release 均为正式 `v30.0.0`。Skills 分发仓库 `main` 为 `38cd851`，源仓库 release commit 为 `4b4a2d7`；当前检出树遵循 latest-only 本地资产策略，GitHub 历史 tags/Releases 和 Git history 不改写。
- `config/` 的容量和模型标识仅是可选示例；31/32 槽位配置与 Terra/Sol 路由是历史配置/观察，不是当前治理默认值。`features.multi_agent_v2` 是非公开、不可移植的运行时输入，不是可移植模板或迁移目标。
- 当前规则仅在规则或 `AGENTS.md`、版本/progress/文档治理、发布/迁移/全局同步、架构漂移、Goal/验收扩张或多 Agent 协作等治理敏感情形加载 `seer-codex-rules`；普通 L1/L2 与单文件任务不因一次本地修改而触发它。多 Agent 仅在净收益门禁通过时派遣，容量不是目标。
- 历史新任务观察曾以 Sol/high 非 Ultra 请求 31 个子 Agent，并直接观察到 22 个同时运行；它证明容量不是目标，也不构成当前容量或模型默认值。
- `seer-codex-rules` 已作为可浏览源码纳入仓库。
- 项目采用 MIT License，并完成首次公开发布净化。

## Recent Progress

- 正式发布 `v30.0.0`：将 `seer-codex-rules` 改为治理敏感的条件路由，并更新多 Agent 工作模型；保留零哈希边界、permission-aware dispatch、净收益派遣、两仓发布边界和 latest-only 本地资产策略。
- 在隔离分发仓库 worktree 中优化 5 个自有 Seer Skills：`seer-capture`、`seer-project-space-health`、`seer-math-exam`、`seer-mathbook` 和 `seer-prepare-open-source-release`。它们分别收窄捕获、深度清理、数学严谨性引用、精确图形实现和开源发布触发边界。
- 上述 5 个 Seer Skills 已通过 commit `38cd851` 推送到 `skills-manager-backup/main`（不建 Release）并经 canonical symlink 安装；30.0.0 全局 live、Downloads 与治理 Skill 也已安装，私有回退副本与最终恢复状态已保留。
- 最终恢复阶段发现并修复旧 `snapshot_state.py` 对公开 inventory 的常驻 SHA256 依赖；inventory 现在只锚定版本，字节指纹仅由真实恢复消费者现场生成。受影响共享测试 25/25 通过，final strict live/state/global-copy guardrail 无 mismatch。
- 基线曾以 `gpt-5.6-sol` 只读运行 20 个路由提示；候选只重跑非 Nature 的场景 1–15并全部通过。相同 1–15 基线/候选总输入为 `2,700,004 -> 2,287,102`，median 为 `169,355 -> 133,725`；普通 cohort 总输入下降 53.3%、median 下降 60.5%，且没有实际子 Agent 派遣或 hash 命令。
- Nature 场景 16–20 仅作只读审计观察，未来可作为候选输入；本轮不实施任何 Nature 工作。所有 `nature-*` 源码、版本、测试、安装副本和 `.agents` 重复副本均冻结，且不做重复清理。第三方 Skill 尚无获准的禁用动作。
- 用户单独授权后，已创建忽略 Git 的本机回退副本，将 `29.1.0` 全局候选同步到 live 与 Downloads，并将同轮 Skill 增量安装到 live；未修改 Agent 配置，未执行 Git/GitHub、公开发布、HANDOFF 刷新或 31 子 Agent 压测。
- 基于 GPT-5.6 社区多源“SHA theater”报告和 OpenAI 精简提示指导，新增默认零哈希策略：只有字节一致性验收存在实际消费者时才计算一次，禁止用文件、逐页、树或 artifact 哈希替代语义、来源、行为、测试或视觉验证；多 Agent 结果契约也禁止默认生成 checksum/manifest 或因 mismatch 进入重复哈希循环。
- 此前曾同步 permission-aware Skill、角色示例和 31 子线程配置；相关 router/guardrail 与 fresh-task 冒烟证据仅作历史参考，本轮未修改或重复验证这些配置，也不把它们设为默认值。
- 结合当前 OpenAI Codex Subagents、配置与 Skills 官方文档，以及 Anthropic、Google、Microsoft 的多 Agent/评测一手资料，确认现有 Agent-first、渐进加载和自适应分波方向成立，并补入可移植配置边界、任务级波次预算、边际证据停止门和首轮通过/返工指标。
- 缩短 `seer-codex-rules` frontmatter 描述以降低大型 Skill 清单的常驻上下文占用，同时保留规则、文档、验收、架构和多 Agent 触发面。
- 验证 `seer-project-handover` 已区分显式生成与接收时一次性消费；普通接管、实现、验证和收尾不会刷新冻结 HANDOFF，只有以后再次明确请求交接才整体重建。
- 增加 Effective Permission Gate、任务包权限字段、角色相容性检查和静态非证明信号；写包只允许实现 worker，旧任务或权限不足时在根任务收束并只请求一次必要授权或建议新任务。
- 正式发布 `v29.0.0`，并按 local latest-only 策略清理当前树的旧 artifact/release 文档与本地旧 tags；GitHub 旧 tags/Releases 和 Git commit 历史保持不变。
- 增加 `29.0.0` Agent-first 候选：收益门禁通过即由适用规则明确要求主动派遣，无需再次点名或使用 Ultra。
- 完成 31 子 Agent 压力验证：无 collaboration-limit 创建失败，但满载出现 `429`、图像处理失败、关闭超时和原始结果冲突，进一步证明容量不是利用率目标。
- 移除 1/2/3 固定治理上限；按就绪独立包、有效空闲槽位与任务/时间/token 预算自适应分波，容量不是利用率目标。
- `v29.0.0` 阶段的 V2/32 槽位和随后 31 子线程配置均为历史实验；`features.multi_agent_v2` 不公开、不可移植，不应作为模板、兼容路径或迁移输入。
- 历史角色示例曾使用 Terra/medium 探索、Terra/high 实现和 Sol/high 深度复核；当前治理只要求按实际可用能力、复杂度和成本选择兼容角色。
- 允许父任务包显式授权递归子树，但根平铺分波仍是默认；整棵树共享收益、容量、互斥写入和紧凑结果门禁。
- 增加 `28.2.0` 最新有效规则：每个任务实施宿主实际加载的 live 全局规则，旧对话和历史文件不得降级，也不按磁盘或远端最高版本号自主切换。
- 将规则生效点限定为新任务或宿主明确重载，并保持有效指令优先级与 `agentmd-plan` 集中治理边界。
- 为 freshness 语义增加 Skill 路由、低 token 指引、guardrail 锚点和单元测试。
- 正式发布 `v28.1.0`：普通阅读、截图、链接和调研默认只分析，只有当次明确命名的 Knowledge/Book 请求才调用 `seer-capture`。
- 将集中治理所有权门禁推进为 `28.1.0`：除 `agentmd-plan` 专有项目外，其他项目和对话不得修改全局主 `AGENTS.md` 或 `seer-codex-rules`，只能生成详细变更报告交由本项目评估。
- 正式发布 `v27.13.0`，将 GPT-5.6 执行效率治理、同步状态、Git tag 和 GitHub Release 纳入同一发布基线。
- 增加面向 GPT-5.6 的精简授权边界：目标内本地读取、编辑和非破坏性验证不再重复确认，真实外部、破坏性、付费、凭据或范围扩张动作按授权范围确认一次。
- 将验证改为直接、行为、affected、full 四级证据梯，加入通过证据复用、失效条件、失败分类和单次重试策略。
- 将全量回归与安全复核改为真实变更面触发，并要求缺陷修复优先采用能区分修复前后的证据。
- 消除 Skill 开始/结束重读、Goal 与普通验收双重预算、全量命令篮子和覆盖审计“五轮”措辞造成的流程重入。
- 正式发布 `v27.12.0`，将 live 全局规则、Downloads 副本、公开 artifact、覆盖 inventory、公开/live Skill 树和私有恢复状态重新同步。
- 增加 `seer-capture` 来源型研究路由覆盖，并明确开发工作区输入默认不自动入库。
- 修复原 `current-state.json`、README 和进度概览停留在 `27.9.0` 造成的严格 guardrail provenance 漂移。
- 旧版曾增加单 Agent 默认、Terra/high 最低路由和 1/2/3 边界；这些策略由 `29.0.0` 的显式授权、自适应 fan-out 和能力阶梯取代。
- 保留紧凑上下文包、结果压缩、互斥写入和完成即回收，并将绝对禁止嵌套改为父任务包显式授权。
- 增加可移植 Agent 模板、live 配置和确定性 `agent_routing_check.py`。
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

- 从真实普通开发和治理任务继续观察 Skill 误触发率、输入 token、净收益派遣和返工；不重复历史 31-child 压测。
- 从真实任务记录波次、活跃槽位、上下文 fork、单位有效结果 token、返工和耗时；依据收益和递减回报使用分波，不设固定容量目标。
- 根据实际使用反馈继续完善跨平台路径和安装体验。
- 根据跨语言项目反馈扩展结构信号解析，同时保持事件触发和人工语义复核。
- 仅在有明确收益时增加 GitHub 安全和社区自动化。

## Risks

- 文字 guardrail 能阻止把哈希写成默认验收，但无法自动判断每个领域是否存在真实的字节完整性消费者；最终仍需根任务把检查映射到明确断言。
- 子 Agent 的最终有效权限来自派生时重新应用的父任务 live runtime overrides；静态角色配置只能说明默认能力，不能探测或保证本次写入/网络/审批权限。
- `features.multi_agent_v2` 是非公开、不可移植的运行时输入，容量语义也不作为本项目治理契约；不得宣传为可移植模板、兼容路径或迁移目标。`fork_turns` 同样只按当前编排器能力使用。
- Codex 不保证 active task 对磁盘规则变更自动热重载；规则必须由宿主在新任务或明确重载后供应，才能成为该任务的有效指令。
- 历史配置/提示曾接受 32 或更高容量，但不代表账号、后端或宿主保证真实并发；实时容量和平台硬限制始终优先。
- 多 Agent 往往以更多总 token 换取时间、覆盖或质量；便宜模型、fresh context、去重和分波停止规则只能优化单位有效结果成本，不能保证绝对节省。
- 规则系统仍依赖 Codex 正确触发 Skill；脚本和最终披露用于降低而非消除偏移。
- 自定义 Agent 的发现可能需要新任务或重启；脚本可验证配置，但不能证明每次语义派遣都完全正确。
- 当前发布与安装证据已收束；残留风险是新规则只在新任务或宿主明确重载后生效，当前任务不假设热重载。

## Detailed Records

- `docs/progress/rounds/2026-08-20-round-001-integrity-evidence-governance-29.1.0.md`
- `docs/progress/rounds/2026-08-20-round-002-release-30.0.0-governance.md`
- `docs/progress/rounds/2026-08-16-round-001-current-codex-subagent-governance.md`
- `docs/progress/rounds/2026-08-11-round-001-handover-lifecycle-permission-aware-dispatch.md`
- `docs/progress/rounds/2026-08-04-round-001-agent-first-multi-agent-governance-29.0.0.md`
- `docs/progress/releases/v30.0.0/RELEASE_NOTES.md`
- `docs/progress/rounds/2026-08-03-round-004-latest-effective-global-rule-28.2.0.md`
- `docs/progress/rounds/2026-08-03-round-003-centralized-governance-ownership-28.1.0.md`
- `docs/progress/rounds/2026-08-03-round-002-gpt-5p6-execution-efficiency.md`
- `docs/progress/rounds/2026-08-03-round-001-provenance-sync-27.12.0.md`
- `docs/progress/rounds/2026-07-28-round-001-multi-agent-model-routing.md`
- `docs/progress/rounds/2026-07-18-round-002-goal-mode-closure.md`
- `docs/progress/rounds/2026-07-18-round-001-architecture-drift-gate.md`
- `docs/progress/rounds/2026-07-14-round-002-activate-global-27.6.0.md`
- `docs/progress/rounds/2026-07-14-round-001-edge-condition-scope-gate.md`
- `docs/progress/rounds/2026-07-13-round-001-public-open-source-release.md`
