# AGENTS.md 27.9.0 候选补丁说明

本次版本动作：`27.8.0 -> 27.9.0`，属于 `MINOR`。

## 变更原因

现有规则约束任务分级、边界收束和 Goal 完成，但没有规定何时值得派遣子 Agent、如何按工作类型选择模型，以及如何限制上下文复制、重复劳动、并发和生命周期。未固定模型时，子 Agent 还会回退继承父 Agent，造成所有工作使用同一高成本模型。

## 修改内容

1. 全局纲要增加多 Agent 收益门禁和强制 Skill 路由，不把更多 Agent 当作默认质量提升。
2. Skill 新增 `multi-agent-governance.md`，采用中心化编排、单 Agent 默认和父 Agent 保留关键路径的工作模型。
3. 默认子 Agent 为 Terra/high；探索为 Terra/high，边界清晰的实现为 Terra/max，重大风险复核为 Sol/high；更高强度只由用户明确启用。
4. 普通并发为 1，明确独立时最多 2，配置硬上限为 3；禁止嵌套派遣、重复工作和同文件并行写入。
5. 默认使用紧凑上下文包和压缩结果，不复制完整历史，不返回原始长日志，完成后立即关闭 Agent。
6. 新增可移植配置模板和 `agent_routing_check.py`，确定性校验 fallback、角色模型、推理强度、权限和禁止嵌套锚点。

## 研究依据

- Codex 官方支持 `[agents]` 默认项和自定义 Agent 文件中的模型、推理、sandbox 与指令覆盖。
- 2026-07-24 的 Nature Machine Intelligence 研究显示，多 Agent 收益依赖任务结构，强模型可能超出协作收益阈值。
- 2026 年 Agent Scaling 研究显示，同质扩张边际收益迅速下降，异构通道比 Agent 数量更关键。
- AutoGen、Claude Code、LangGraph 和 OpenAI Agents SDK 的成熟模式共同支持单 Agent 起步、中心化集成、独立任务并行和明确终止。

## 低 Token 边界

- 普通任务不加载多 Agent reference，也不派遣子 Agent。
- 只有考虑派遣时才读取一次治理 reference。
- 不增加每轮 token 统计任务；平台未暴露精确子 Agent usage 时只使用派遣数、上下文 fork、返回长度、重复工作和返工等代理指标。
- 更高模型档位不会自动升级，避免深度复核演变成无限算力升级。

## 验证要求

- 全局纲要通过版本、日期、体量、强制路由和并发锚点检查。
- Skill 通过结构校验、reference 路由、Python 编译和全部单元测试。
- 公开模板和 live 配置通过 TOML 与 Agent 路由校验。
- 全局、Downloads、正式 artifact、live Skill、公开 Skill 和私有状态快照保持一致。
