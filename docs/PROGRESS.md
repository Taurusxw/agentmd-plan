# Progress

## Current State

- 当前正式发布为 `v29.0.0`；live 全局规则、Downloads 副本、Skill、Agent 路由、公开 artifact 与 release 记录一致。
- 新任务已验证 Sol/high 非 Ultra 显式派遣可突破三个子 Agent：31/31 创建请求被接受，直接观察到 22 个子 Agent 同时运行；旧任务仍保留创建时的四总槽位快照。
- `seer-codex-rules` 已作为可浏览源码纳入仓库。
- 项目采用 MIT License，并完成首次公开发布净化。

## Recent Progress

- 正式发布 `v29.0.0`，并按 local latest-only 策略清理当前树的旧 artifact/release 文档与本地旧 tags；GitHub 旧 tags/Releases 和 Git commit 历史保持不变。
- 增加 `29.0.0` Agent-first 候选：收益门禁通过即由适用规则明确要求主动派遣，无需再次点名或使用 Ultra。
- 完成 31 子 Agent 压力验证：无 collaboration-limit 创建失败，但满载出现 `429`、图像处理失败、关闭超时和原始结果冲突，进一步证明容量不是利用率目标。
- 移除 1/2/3 固定治理上限；按就绪独立包、有效空闲槽位与任务/时间/token 预算自适应分波，容量不是利用率目标。
- 将可移植和 live 配置迁移到 V2 含根总容量 32；静态校验区分 V1 子线程 `N+1` 与 V2 总槽位 `N`，并拒绝冲突键。
- 将角色路由调整为 Terra/medium 探索与默认、Terra/high 实现、Sol/high 深度复核；异构派遣默认 fresh context，复杂度驱动升降档。
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

- 从真实任务记录波次、活跃槽位、上下文 fork、单位有效结果 token、返工和耗时；依据收益和递减回报使用分波，而非默认填满 31 个子槽位。
- 根据实际使用反馈继续完善跨平台路径和安装体验。
- 根据跨语言项目反馈扩展结构信号解析，同时保持事件触发和人工语义复核。
- 仅在有明确收益时增加 GitHub 安全和社区自动化。

## Risks

- Codex 不保证 active task 对磁盘规则变更自动热重载；规则必须由宿主在新任务或明确重载后供应，才能成为该任务的有效指令。
- 配置/提示接受 32 或更高容量不代表账号、后端或宿主保证真实并发；实时容量和平台硬限制始终优先。
- 多 Agent 往往以更多总 token 换取时间、覆盖或质量；便宜模型、fresh context、去重和分波停止规则只能优化单位有效结果成本，不能保证绝对节省。
- 规则系统仍依赖 Codex 正确触发 Skill；脚本和最终披露用于降低而非消除偏移。
- 自定义 Agent 的发现可能需要新任务或重启；脚本可验证配置，但不能证明每次语义派遣都完全正确。

## Detailed Records

- `docs/progress/rounds/2026-08-04-round-001-agent-first-multi-agent-governance-29.0.0.md`
- `docs/progress/releases/v29.0.0/RELEASE_NOTES.md`
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
