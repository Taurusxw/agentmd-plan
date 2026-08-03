# Agentmd Plan v29.0.0

## 中文

`v29.0.0` 将固定的单 Agent 默认与 1/2/3 并发治理替换为 Agent-first 自适应编排，并正式验证 Sol/high 在非 Ultra 下可以突破三个并发子 Agent。

### 主要内容

- 适用规则通过收益门禁后即明确授权主动派遣，无需用户重复点名或使用 Ultra。
- 波次大小由就绪独立包、实时空闲槽位和任务/时间/token 预算共同决定，容量不是利用率目标。
- V2 模板配置 32 个含根总槽位，并区分 V1 子线程与 V2 总容量语义。
- 默认使用 Terra/medium 探索、Terra/high 实现和 Sol/high 深度复核；异构角色使用 fresh context。
- 31/31 子 Agent 创建请求在 fresh Sol/high 会话中成功，直接观察到 22 个同时运行；满载同时暴露限流、工具失败、关闭延迟与结果仲裁成本。
- 当前检出树仅保留最新发布 artifact/release 文档与本地 tag；GitHub 保留旧 tags/Releases，Git commit 历史不改写。

### 升级说明

安装 `artifacts/AGENTS-29.0.0.md`、`skills/seer-codex-rules/` 与 `config/` 中的 V2/角色模板，并在新任务中验证实际容量。

## English

`v29.0.0` replaces the fixed single-agent default and one/two/three-agent governance ceiling with adaptive agent-first orchestration, and verifies that explicit non-Ultra Sol/high workflows can exceed three concurrent children.

### Highlights

- Applicable rules explicitly authorize proactive delegation after the benefit gate without requiring Ultra or repeated user prompting.
- Wave size follows ready independent packets, effective free slots, and task/time/token budget; capacity is not a utilization target.
- The V2 template configures 32 total slots including the root and distinguishes V1 child capacity from V2 total capacity.
- Routes Terra/medium exploration, Terra/high implementation, and Sol/high deep review through fresh heterogeneous contexts.
- A fresh Sol/high session accepted 31/31 child requests and directly observed 22 running at once, while saturation exposed throttling, tool failures, shutdown delay, and adjudication cost.
- The current checkout retains only the latest release artifact/documents and local tag; GitHub keeps older tags/Releases, and Git commit history is not rewritten.

### Upgrade Notes

Install `artifacts/AGENTS-29.0.0.md`, `skills/seer-codex-rules/`, and the V2/role templates under `config/`, then verify effective capacity in a fresh task.
