# Agentmd Plan

[简体中文](README.md) | [English](README.en.md)

当前正式版本：`v30.0.0`

当前检出树、公开 artifact、维护环境安装、Git tag 和 GitHub Release 均为 `30.0.0`。独立 Skills 分发仓库通过单独提交发布且不创建 Release；GitHub 保留历史 tags/Releases 和 Git commit 历史，当前检出树遵循 latest-only 本地资产策略。

Agentmd Plan 是一套可移植、可验证、低 token 的 Codex 规则治理方案。全局 `AGENTS.md` 只保留每次任务都应生效的纲要，复杂执行规则由 `seer-codex-rules` Skill 根据任务类型按需加载。

## 解决的问题

- 防止全局 `AGENTS.md` 随规则增加而持续膨胀。
- 让短任务保持轻量，同时为重要开发、迁移和发布保留完整验证与溯源。
- 通过条件化治理路由、Skill 路由、reference 模块、校验脚本和最终披露降低规则偏移。
- 约束重复验收、过多 round 和低概率边界条件过度开发。
- 让目标内本地修改和非破坏性验证默认直行，并对重复权限确认、回归测试和安全复核设置事件触发与证据复用规则。
- 为持续运行的 Goal 冻结有限完成条件，防止自动续跑把可选边界不断变成必做工作。
- 在连续补丁侵蚀模块边界前，用事件触发的热点检查恢复结构化与模块化决策。
- 只在独立工作包具有明确净收益且运行时允许时派遣，按可用容量和任务预算自适应分波，并用紧凑上下文与互斥写入控制协调成本。
- 将个人路径、私有备份和 live 状态隔离在公开仓库之外。
- 截图、文档、链接和调研默认只分析、不持久化；只有用户对当次明确材料指定 `[入库]`、Knowledge 或具体 Book 时才调用 `seer-capture`，授权不跨对话或相邻任务继承。
- 全局主 `AGENTS.md` 和 `seer-codex-rules` 只允许在 `agentmd-plan` 专有项目内修改；其他项目只能提交详细变更报告，不能直接同步或覆盖。
- 每个任务执行宿主实际加载的最新有效全局规则；旧对话和历史文件不能降级，磁盘或远端的最高版本号也不能触发自主切换。

## 版本内容

- `artifacts/AGENTS-30.0.0.md`：已验收并发布的全局规则 artifact。
- `config/`：可选的多 Agent 配置与角色示例；其中的容量和模型标识不是当前治理默认值，必须由实际运行时能力和任务需要决定。
- `skills/seer-codex-rules/`：规则设计、任务分级、代码与文档治理、round/phase/release、验收收束和版本治理 Skill。
- `skills/seer-codex-rules/scripts/`：规则体量、Skill 路由、结构热点、同步状态和恢复快照检查脚本。
- `docs/`：公开项目状态、文档索引和必要的开发与发布记录。
- `VERSION`：项目当前发布版本。

当前检出树只维护最新发布资产，以减少本地重复文件；GitHub 继续保留旧 tags 和 Releases，Git commit 历史也不改写。

## 工作机制

```text
全局 AGENTS.md
  -> 按任务匹配加载适用 Skill
      -> 治理敏感任务加载 seer-codex-rules
          -> 判断 L0-L4、guardrail 和独立工作包
              -> 净收益门禁通过才派遣并按运行时容量/预算分波
                  -> 只加载当前任务需要的 reference
                      -> 修改、验证、留痕、收束
```

匹配现有 Skill 的任务照常加载该 Skill。`seer-codex-rules` 只在规则或 `AGENTS.md`、版本/progress/文档治理、发布/迁移/全局同步、架构漂移、Goal/验收扩张或多 Agent 协作等治理敏感情形加载；普通 L1/L2 与单文件工作不因一次本地修改而触发它。收益门禁通过才派遣，避免为了合规或填满容量机械消耗上下文。

## 安装

1. 备份现有的 `<codex-home>/AGENTS.md`、`config.toml`、`agents/` 和同名 Skill。
2. 将 `skills/seer-codex-rules/` 复制到 `<codex-home>/skills/seer-codex-rules/`。
3. 审阅 `artifacts/AGENTS-30.0.0.md`，确认符合自己的工作方式。
4. 将该 artifact 安装为 `<codex-home>/AGENTS.md`。
5. 如需采用可选示例，再将 `config/agents.toml.example` 的 `[agents]` 表合并进 `<codex-home>/config.toml`，并将 `config/agents/*.toml` 复制到 `<codex-home>/agents/`。`[features.multi_agent_v2]` 是非公开、不可移植的运行时输入，不是文档化模板或迁移目标；不要在新配置中采用它。
6. 运行下方校验命令，确认版本、Skill 路由、模型角色和同步状态。

`<codex-home>` 通常由环境变量 `CODEX_HOME` 指定；未设置时一般是 `<user-home>/.codex`。

## 核心治理规则

### 任务分级

- `L0`：只读分析，不修改文件，不写开发留痕。
- `L1`：微小变更，最小修改和直接验证，默认不新增 round。
- `L2`：常规开发，运行针对性测试并按现有项目体系留痕。
- `L3`：重要变更，先评估影响，只运行与真实风险逐项对应的验证矩阵。
- `L4`：阶段、迁移或发布，对最终状态执行一次既定 phase/release 清单。

### 执行效率与授权

- 修改、构建、修复或优化请求默认授权目标内本地读取、编辑、格式化和非破坏性验证，不再逐项询问。
- 只有外部写入或发布、破坏性或不可逆操作、付费、凭据披露、目标或风险等级实质扩大时确认；同一授权范围只确认一次。
- 验证按直接证据、目标行为、受影响范围、全量发布四级递进；低层证据足够时不升级。
- 普通任务默认不生成 hash、checksum 或 manifest；只有验收明确要求字节一致性且有实际消费者时才计算一次，不能替代语义、来源、行为、测试或视觉验证。
- 已通过证据只有在覆盖的代码、测试、配置、依赖、生成输入或环境改变后才失效；相同或重叠检查不重复运行。
- 全量回归和安全扫描采用事件触发，任务或文档仅出现“安全/权限”等词不构成触发。
- 缺陷修复优先使用能区分修复前后的测试；修复前也通过的通用测试只算回归证据。

### 集中治理所有权

- 全局主 `AGENTS.md`、同步副本以及 `seer-codex-rules` 源码和安装副本由 `agentmd-plan` 专有项目集中维护。
- 其他项目即使发现漂移、缺陷或改进机会，也只能只读核查并输出包含证据、建议差异、版本影响、跨项目风险、验证和回退的变更报告。
- 报告由用户转交本项目对话后再评估实施；自动同步、安装器、脚本、恢复任务和子 Agent 均不得绕过该边界。

### 最新有效规则

- “最新”以宿主实际供应给当前任务的 live 全局规则为准，不扫描磁盘、Git 历史或远端 Release 选择最高语义版本。
- 旧对话、缓存摘要、历史 artifact、README、快照或项目文档不得把当前任务降级到旧规则。
- 规则在任务运行中改变时不假设自动热重载；新任务或宿主明确重载后生效，并继续服从有效指令优先级和集中治理所有权。

### 验收与边界收束

- 原始验收标准通过后停止追加门槛。
- 新发现只有在阻塞原始目标或涉及重大安全、权限、隐私和数据风险时，才自动进入当前任务。
- 普通边界条件必须有证据、直接关联目标，并能通过适度修改和针对性测试闭环。
- L2 最多执行一次额外边界加固；连续两次只增强假设性健壮性时停止当前任务。

### Goal 模式收束

- 创建或恢复持续 Goal 时，在目标对象中保存结果、3-5 条冻结完成条件、非目标、固定验证预算和结束规则。
- “全面、彻底、最佳、没有遗漏”等开放表达必须转换成可观察条件，不能直接形成无限 `required work`。
- 新发现只有在完成条件失败、当前改动引入回归或出现重大安全风险时才进入当前 Goal；其他内容最多列为 3 条后续项。
- 一轮没有推进完成条件时，只允许一次针对真实阻塞的诊断；条件全部通过后立即 `complete`，不递归加固测试和验收工具。

### 架构漂移控制

- 只有同一生产模块连续成为补丁热点，或当前改动会增加职责、入口接口、重复逻辑和测试耦合时，才加载架构漂移 reference 和脚本。
- 三个连续任务或最近十条记录中的五条触及同一文件，构成热点信号；超过 800 非空行和 20 个入口分支是辅助信号。
- 行数本身不要求拆分。两个信号时冻结新增职责，三个以上信号时升级到 L3 并明确模块边界。
- `structure_check.py` 只提供证据，不自动重构，也不会替代对序列化运行时代码和有意重复的语义判断。

### 多 Agent 与模型路由

- 识别独立的发现、实现、验证和专业复核工作包；只有工作包有界、可独立验证、写入互斥、运行时允许，且速度、隔离、能力路由或重大风险覆盖的收益明确高于协调与 token 成本时才派遣。
- 每波数量取就绪独立包、实时空闲槽位和任务/时间/token 预算的最小值；治理层不设 1/2/3 固定上限，配置容量也不是利用率目标。
- 可选角色示例中的模型和推理档位只作历史配置参考，不是治理默认值；每次派遣按实际可用能力、任务复杂度和成本选择兼容角色。
- 每次派生前先写明工作包所需的只读/写入/网络/审批访问，并核对父任务当前有效 permission mode；角色文件中的静态 `sandbox_mode` 只表示默认能力，不能证明本次子 Agent 的最终权限。
- 任务包同时记录具体路径、工具、服务或外部副作用目标，父任务实际观察到的有效访问及其观测来源，以及本次派遣的相容性结论；不能只写一个不可审计的 `checked=yes`。
- 写任务只交给实现 worker。父任务权限不足或旧任务状态异常时，根任务继续完成可做工作，只请求一次必要授权或建议在正确权限的新任务重新派生，避免子 Agent 循环询权。
- 主 Agent 保留需求、关键路径、写入所有权、分波汇总、集成和最终验证；一个文件或生成物同时只允许一个写入者。
- 每个非平凡波次冻结验收信号和任务级上限；只有新增证据可能改变决定或关闭明确缺口时才续派，并记录首轮通过、返工和拒绝原因。
- 当前编排器支持时，优先使用紧凑的新鲜上下文；具体上下文参数属于宿主适配，不是可移植配置契约。嵌套默认关闭，只有父任务包明确授权递归子树并重过同一门禁时才允许。
- 31 个 spawned-agent 子线程（通常 32 个含根槽位）只是历史配置与压力观察，不是治理默认容量；每个任务以运行时硬限制和有效空闲槽位为准。

### 留痕控制

- 同一目标连续推进优先更新已有记录。
- round 编号按日期重置，同一天的独立目标才递增。
- 目录容量只能改变记录位置，不能成为跳过必要留痕的理由。
- 多日、多轮或发布工作升级为 phase/release，避免 round 无限堆积。

## 校验

在仓库根目录运行：

```powershell
python skills/seer-codex-rules/scripts/measure_rules.py --strict artifacts/AGENTS-30.0.0.md
python -m py_compile skills/seer-codex-rules/scripts/agent_routing_check.py skills/seer-codex-rules/scripts/guardrail_check.py skills/seer-codex-rules/scripts/measure_rules.py skills/seer-codex-rules/scripts/snapshot_state.py skills/seer-codex-rules/scripts/structure_check.py
python -m unittest discover -s skills/seer-codex-rules/tests -p "test_*.py" -v
python skills/seer-codex-rules/scripts/agent_routing_check.py --config config/agents.toml.example --agents-dir config/agents --json
python skills/seer-codex-rules/scripts/guardrail_check.py --strict --project . --global-agents artifacts/AGENTS-30.0.0.md --downloads-agents artifacts/AGENTS-30.0.0.md --skill skills/seer-codex-rules --json
codex --strict-config doctor --summary
codex debug prompt-input probe
```

安装到个人环境后，不带路径运行 `agent_routing_check.py --json` 可检查 live 静态配置；输出固定声明 `runtime_permissions_verified=false`，每次派生仍须重新核对父任务实时 permission mode。`snapshot_state.py --write` 可创建私有状态清单和 Skill 恢复快照。不要提交包含个人路径的 live manifest 或备份。

## 升级与回退

- 发布版本、Git tag 和 GitHub Release 使用 `vMAJOR.MINOR.PATCH`。
- 全局工作模型或兼容边界变化升级 `MAJOR`。
- 新增长期规则、Skill 路由或治理能力升级 `MINOR`。
- 不改变行为的错字、格式和链接修正升级 `PATCH`。
- 回退时恢复上一已验收版本的全局规则、Skill、`config.toml` 和自定义 Agent 文件；源仓库发布与维护环境安装是两个独立目标，必须分别确认并重新运行受影响检查。

## 隐私与安全

公开仓库不包含个人机器路径、历史私有备份、live 状态、凭据或二进制恢复包。文字规则不能替代 sandbox、approval、权限、测试、CI 或人工安全确认。

## 参与和许可

提交改进前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请按照 [SECURITY.md](SECURITY.md) 私下报告。

本项目采用 [MIT License](LICENSE)。
