# Agentmd Plan

[简体中文](README.md) | [English](README.en.md)

当前正式发布：`v28.1.0`

Agentmd Plan 是一套可移植、可验证、低 token 的 Codex 规则治理方案。全局 `AGENTS.md` 只保留每次任务都应生效的纲要，复杂执行规则由 `seer-codex-rules` Skill 根据任务类型按需加载。

## 解决的问题

- 防止全局 `AGENTS.md` 随规则增加而持续膨胀。
- 让短任务保持轻量，同时为重要开发、迁移和发布保留完整验证与溯源。
- 通过全局门禁、Skill 路由、reference 模块、校验脚本和最终披露降低规则偏移。
- 约束重复验收、过多 round 和低概率边界条件过度开发。
- 让目标内本地修改和非破坏性验证默认直行，并对重复权限确认、回归测试和安全复核设置事件触发与证据复用规则。
- 为持续运行的 Goal 冻结有限完成条件，防止自动续跑把可选边界不断变成必做工作。
- 在连续补丁侵蚀模块边界前，用事件触发的热点检查恢复结构化与模块化决策。
- 用单 Agent 默认、Terra/high 起步的模型路由、紧凑上下文包和并发上限控制子 Agent 的协调与 token 成本。
- 将个人路径、私有备份和 live 状态隔离在公开仓库之外。
- 截图、文档、链接和调研默认只分析、不持久化；只有用户对当次明确材料指定 `[入库]`、Knowledge 或具体 Book 时才调用 `seer-capture`，授权不跨对话或相邻任务继承。
- 全局主 `AGENTS.md` 和 `seer-codex-rules` 只允许在 `agentmd-plan` 专有项目内修改；其他项目只能提交详细变更报告，不能直接同步或覆盖。

## 版本内容

- `artifacts/AGENTS-28.1.0.md`：与当前 live 全局规则一致的正式发布纲要。
- `config/`：Terra/high 子 Agent 兜底，以及 Terra/high 探索、Terra/max 实现和 Sol/high 深度复核角色模板。
- `skills/seer-codex-rules/`：规则设计、任务分级、代码与文档治理、round/phase/release、验收收束和版本治理 Skill。
- `skills/seer-codex-rules/scripts/`：规则体量、Skill 路由、结构热点、同步状态和恢复快照检查脚本。
- `docs/`：公开项目状态、文档索引和必要的开发与发布记录。
- `VERSION`：项目当前发布版本。

## 工作机制

```text
全局 AGENTS.md
  -> 强制加载 seer-codex-rules/SKILL.md
      -> 判断 L0-L4 和 guardrail 等级
          -> 默认单 Agent；考虑派遣时运行收益门禁和模型路由
              -> 只加载当前任务需要的 reference
                  -> 修改、验证、留痕、收束
```

普通文件修改任务只需读取一次 Skill 路由、任务分级和一个产物相关 reference，结束时复用已有上下文。规则同步、迁移或发布才启用更完整的 guardrail，避免为了合规机械消耗上下文。

## 安装

1. 备份现有的 `<codex-home>/AGENTS.md`、`config.toml`、`agents/` 和同名 Skill。
2. 将 `skills/seer-codex-rules/` 复制到 `<codex-home>/skills/seer-codex-rules/`。
3. 审阅 `artifacts/AGENTS-28.1.0.md`，确认符合自己的工作方式。
4. 将该 artifact 安装为 `<codex-home>/AGENTS.md`。
5. 将 `config/agents.toml.example` 的 `[agents]` 表合并进 `<codex-home>/config.toml`，并将 `config/agents/*.toml` 复制到 `<codex-home>/agents/`。
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
- 已通过证据只有在覆盖的代码、测试、配置、依赖、生成输入或环境改变后才失效；相同或重叠检查不重复运行。
- 全量回归和安全扫描采用事件触发，任务或文档仅出现“安全/权限”等词不构成触发。
- 缺陷修复优先使用能区分修复前后的测试；修复前也通过的通用测试只算回归证据。

### 集中治理所有权

- 全局主 `AGENTS.md`、同步副本以及 `seer-codex-rules` 源码和安装副本由 `agentmd-plan` 专有项目集中维护。
- 其他项目即使发现漂移、缺陷或改进机会，也只能只读核查并输出包含证据、建议差异、版本影响、跨项目风险、验证和回退的变更报告。
- 报告由用户转交本项目对话后再评估实施；自动同步、安装器、脚本、恢复任务和子 Agent 均不得绕过该边界。

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

- 单 Agent 是默认路径；任务大、难或要求全面，本身不构成派遣理由。
- 只有独立边界、非阻塞并行、互斥写入和可压缩返回同时成立，并且存在时间、上下文隔离或专业复核收益时才派遣。
- 所有子 Agent 最低从 Terra/high 起步：`explorer_fast` 做只读搜索和摘要，`worker_balanced` 使用 Terra/max 完成边界清晰的实现；`reviewer_deep` 使用 Sol/high 复核重大风险，更高推理强度仅由用户明确启用。
- 主 Agent 保留需求、关键路径、集成和最终验证；普通并发为 1，明确独立时最多 2，配置硬上限为 3。
- 默认发送紧凑任务包，不复制完整历史；禁止子 Agent 嵌套派遣、重复工作和同文件并行写入，完成后立即关闭。

### 留痕控制

- 同一目标连续推进优先更新已有记录。
- round 编号按日期重置，同一天的独立目标才递增。
- 目录容量只能改变记录位置，不能成为跳过必要留痕的理由。
- 多日、多轮或发布工作升级为 phase/release，避免 round 无限堆积。

## 校验

在仓库根目录运行：

```powershell
python skills/seer-codex-rules/scripts/measure_rules.py --strict artifacts/AGENTS-28.1.0.md
python -m py_compile skills/seer-codex-rules/scripts/agent_routing_check.py skills/seer-codex-rules/scripts/guardrail_check.py skills/seer-codex-rules/scripts/measure_rules.py skills/seer-codex-rules/scripts/snapshot_state.py skills/seer-codex-rules/scripts/structure_check.py
python -m unittest discover -s skills/seer-codex-rules/tests -p "test_*.py" -v
python skills/seer-codex-rules/scripts/agent_routing_check.py --config config/agents.toml.example --agents-dir config/agents --json
python skills/seer-codex-rules/scripts/guardrail_check.py --strict --project . --global-agents artifacts/AGENTS-28.1.0.md --downloads-agents artifacts/AGENTS-28.1.0.md --skill skills/seer-codex-rules --json
```

安装到个人环境后，不带路径运行 `agent_routing_check.py --json` 可检查 live 配置；`snapshot_state.py --write` 可创建私有状态清单和 Skill 恢复快照。不要提交包含个人路径的 live manifest 或备份。

## 升级与回退

- 发布版本、Git tag 和 GitHub Release 使用 `vMAJOR.MINOR.PATCH`。
- 全局工作模型或兼容边界变化升级 `MAJOR`。
- 新增长期规则、Skill 路由或治理能力升级 `MINOR`。
- 不改变行为的错字、格式和链接修正升级 `PATCH`。
- 回退时恢复升级前的全局规则、Skill、`config.toml` 和自定义 Agent 文件，并重新运行同步、模型路由与覆盖检查。

## 隐私与安全

公开仓库不包含个人机器路径、历史私有备份、live 状态、凭据或二进制恢复包。文字规则不能替代 sandbox、approval、权限、测试、CI 或人工安全确认。

## 参与和许可

提交改进前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请按照 [SECURITY.md](SECURITY.md) 私下报告。

本项目采用 [MIT License](LICENSE)。
