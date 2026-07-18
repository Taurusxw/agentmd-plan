# Agentmd Plan

[简体中文](README.md) | [English](README.en.md)

当前版本：`v27.7.0`

Agentmd Plan 是一套可移植、可验证、低 token 的 Codex 规则治理方案。全局 `AGENTS.md` 只保留每次任务都应生效的纲要，复杂执行规则由 `seer-codex-rules` Skill 根据任务类型按需加载。

## 解决的问题

- 防止全局 `AGENTS.md` 随规则增加而持续膨胀。
- 让短任务保持轻量，同时为重要开发、迁移和发布保留完整验证与溯源。
- 通过全局门禁、Skill 路由、reference 模块、校验脚本和最终披露降低规则偏移。
- 约束重复验收、过多 round 和低概率边界条件过度开发。
- 在连续补丁侵蚀模块边界前，用事件触发的热点检查恢复结构化与模块化决策。
- 将个人路径、私有备份和 live 状态隔离在公开仓库之外。

## 版本内容

- `artifacts/AGENTS-27.7.0.md`：精简的全局规则纲要。
- `skills/seer-codex-rules/`：规则设计、任务分级、代码与文档治理、round/phase/release、验收收束和版本治理 Skill。
- `skills/seer-codex-rules/scripts/`：规则体量、Skill 路由、结构热点、同步状态和恢复快照检查脚本。
- `docs/`：公开项目状态、文档索引和必要的开发与发布记录。
- `VERSION`：项目当前发布版本。

## 工作机制

```text
全局 AGENTS.md
  -> 强制加载 seer-codex-rules/SKILL.md
      -> 判断 L0-L4 和 guardrail 等级
          -> 只加载当前任务需要的 reference
              -> 修改、验证、留痕、收束
```

普通文件修改任务只需加载 Skill 路由、任务分级和一个产物相关 reference。规则同步、迁移或发布才启用更完整的 guardrail，避免为了合规机械消耗上下文。

## 安装

1. 备份现有的 `<codex-home>/AGENTS.md` 和同名 Skill。
2. 将 `skills/seer-codex-rules/` 复制到 `<codex-home>/skills/seer-codex-rules/`。
3. 审阅 `artifacts/AGENTS-27.7.0.md`，确认符合自己的工作方式。
4. 将该 artifact 安装为 `<codex-home>/AGENTS.md`。
5. 运行下方校验命令，确认版本、Skill 路由和同步状态。

`<codex-home>` 通常由环境变量 `CODEX_HOME` 指定；未设置时一般是 `<user-home>/.codex`。

## 核心治理规则

### 任务分级

- `L0`：只读分析，不修改文件，不写开发留痕。
- `L1`：微小变更，最小修改和直接验证，默认不新增 round。
- `L2`：常规开发，运行针对性测试并按现有项目体系留痕。
- `L3`：重要变更，先评估影响，记录决策并扩大验证范围。
- `L4`：阶段、迁移或发布，使用 phase/release 结构完成交接。

### 验收与边界收束

- 原始验收标准通过后停止追加门槛。
- 新发现只有在阻塞原始目标或涉及重大安全、权限、隐私和数据风险时，才自动进入当前任务。
- 普通边界条件必须有证据、直接关联目标，并能通过适度修改和针对性测试闭环。
- L2 最多执行一次额外边界加固；连续两次只增强假设性健壮性时停止当前任务。

### 架构漂移控制

- 只有同一生产模块连续成为补丁热点，或当前改动会增加职责、入口接口、重复逻辑和测试耦合时，才加载架构漂移 reference 和脚本。
- 三个连续任务或最近十条记录中的五条触及同一文件，构成热点信号；超过 800 非空行和 20 个入口分支是辅助信号。
- 行数本身不要求拆分。两个信号时冻结新增职责，三个以上信号时升级到 L3 并明确模块边界。
- `structure_check.py` 只提供证据，不自动重构，也不会替代对序列化运行时代码和有意重复的语义判断。

### 留痕控制

- 同一目标连续推进优先更新已有记录。
- round 编号按日期重置，同一天的独立目标才递增。
- 目录容量只能改变记录位置，不能成为跳过必要留痕的理由。
- 多日、多轮或发布工作升级为 phase/release，避免 round 无限堆积。

## 校验

在仓库根目录运行：

```powershell
python skills/seer-codex-rules/scripts/measure_rules.py --strict artifacts/AGENTS-27.7.0.md
python -m py_compile skills/seer-codex-rules/scripts/guardrail_check.py skills/seer-codex-rules/scripts/measure_rules.py skills/seer-codex-rules/scripts/snapshot_state.py skills/seer-codex-rules/scripts/structure_check.py
python -m unittest discover -s skills/seer-codex-rules/tests -p test_structure_check.py -v
python skills/seer-codex-rules/scripts/guardrail_check.py --strict --project . --global-agents artifacts/AGENTS-27.7.0.md --downloads-agents artifacts/AGENTS-27.7.0.md --skill skills/seer-codex-rules --json
```

安装到个人环境后，可以使用 `snapshot_state.py --write` 在私有位置创建状态清单和 Skill 恢复快照。不要把包含个人路径的 live manifest 或备份提交到公开仓库。

## 升级与回退

- 发布版本、Git tag 和 GitHub Release 使用 `vMAJOR.MINOR.PATCH`。
- 全局工作模型或兼容边界变化升级 `MAJOR`。
- 新增长期规则、Skill 路由或治理能力升级 `MINOR`。
- 不改变行为的错字、格式和链接修正升级 `PATCH`。
- 回退时恢复升级前的全局规则和 Skill，并重新运行同步与覆盖检查。

## 隐私与安全

公开仓库不包含个人机器路径、历史私有备份、live 状态、凭据或二进制恢复包。文字规则不能替代 sandbox、approval、权限、测试、CI 或人工安全确认。

## 参与和许可

提交改进前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请按照 [SECURITY.md](SECURITY.md) 私下报告。

本项目采用 [MIT License](LICENSE)。
