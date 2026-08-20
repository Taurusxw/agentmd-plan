# AGENTS.md 29.1.0 正式补丁说明

本次正式版本动作：`29.0.0 -> 29.1.0`，按最高影响属于 `MINOR`。全局规则、项目 `VERSION`、Git tag、GitHub Release、release 目录和公开 artifact 统一使用 `29.1.0`。

## 变更原因

普通开发、文档和多 Agent 结果中出现了没有实际消费者的 SHA/checksum/manifest 工作，它只能证明字节一致性，却被误用为语义、行为或验收代理。同时 post-release 的多 Agent 配置与派遣证据需要按当前 Codex 官方配置语义正式收束。

## 修改内容

1. 普通任务默认不计算、不记录 hash、checksum 或 manifest；只有验收明确要求字节一致性并存在实际消费者时才使用一次。
2. 哈希不能替代语义审查、来源证明、行为测试或视觉检查；同步和恢复场景只保留一次最终一致性比较。
3. 子 Agent 结果不默认创建 checksum manifest；mismatch 只触发一次现状重读和根任务判断，不进入重复哈希循环。
4. 可移植配置改用官方人类可读 `[agents].max_concurrent_threads_per_session = 31`，通常连同根任务形成 32 个总槽位；schema-only V2 仅作为带警告的兼容输入。
5. 每次派遣记录具体 capability scope、父任务实际有效访问、观测来源和相容性决定，静态角色配置不再被当作运行时权限证明。
6. 加入任务级波次预算、边际证据停止门、首轮通过与返工/拒绝原因；容量仍不是利用率目标。

## 版本依据

本次新增长期全局规则、Skill 证据边界、派遣契约和配置验证能力，但不替换 `29.0.0` 的 Agent-first 工作模型或指令优先级，因此升级 `MINOR` 到 `29.1.0`。

## 状态边界

- 不重复 `v29.0.0` 已完成的 31 子 Agent 压测；配置和后端容量仍须服从新任务的实际运行时限制。
- 静态路由检查不能证明子 Agent 的最终文件、网络、MCP 或审批权限，每次派生仍需核对父任务 live permission mode。
- 当前检出树仅保留最新发布资产和本地 tag；GitHub 的旧 tags/Releases 与 Git commit 历史均保留。
- 回退依赖 Git 历史或使用者自己的本地备份，不覆盖未提交工作。
