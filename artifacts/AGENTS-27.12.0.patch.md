# AGENTS.md 27.12.0 候选补丁说明

本次候选动作：`27.9.0 -> 27.12.0`，按最高影响属于 `MINOR`；项目最新正式发布仍为 `v27.9.0`，本轮不创建 Git tag 或 GitHub Release。

## 变更原因

live 全局规则已经增加来源型研究默认进入 Seer Knowledge 的长期路由，但公开候选、覆盖清单和私有恢复状态仍锚定 `27.9.0`，导致 guardrail 报告版本、哈希、Skill 树和文档 provenance 漂移。

## 修改内容

1. 新增与 live `<codex-home>/AGENTS.md` 字节一致的 `AGENTS-27.12.0.md` 候选。
2. 将全局规则覆盖矩阵和逐条 inventory 锚定到 `27.12.0` 与当前 SHA-256。
3. 显式覆盖 `seer-capture` 及其研究/成书工作流，区分来源型研究与普通开发输入。
4. 更新中英文 README、进度概览、文档索引和本轮记录，明确“正式发布 `v27.9.0`、当前治理候选 `27.12.0`”。
5. 使用 `snapshot_state.py --write` 刷新忽略提交的机器私有 manifest 与 Skill 恢复快照。

## 版本边界

- `VERSION`、Git tag 和 release 目录保持 `27.9.0`，因为用户没有授权正式发布。
- `27.12.0` 是当前已安装规则的可审查候选和恢复锚点，不冒充已发布版本。

## 验证要求

- live 全局、Downloads 副本和 `AGENTS-27.12.0.md` 哈希一致。
- live Skill 与公开 Skill 树一致；覆盖矩阵和 inventory 均锚定当前全局版本/哈希。
- Skill 单元测试、Python 编译、measure、agent routing、严格 guardrail 和私有 state/snapshot 校验通过。
- README、PROGRESS、DOC_INDEX、round、Git diff 与公开隐私边界一致。
