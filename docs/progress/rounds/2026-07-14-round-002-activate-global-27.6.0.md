# 2026-07-14 Round 002: activate global 27.6.0

## Status

completed

## Goal

停止使用活动版本 `27.5.1`，全面采用精简全局纲要 `27.6.0` 及其配套 `seer-codex-rules` Skill。

## Background

`27.6.0` 已作为公开候选完成结构、覆盖和低 token 护栏验证，但此前尚未安装为维护环境的活动全局规则。维护者确认旧版本不再使用，并要求正式切换。

## Scope

- 将全局活动规则和同步副本统一替换为 `27.6.0` artifact。
- 将配套 Skill 源码、覆盖矩阵、规则清单和护栏脚本同步到活动 Skill。
- 刷新仓库外私有状态清单和 Skill 恢复快照。
- 保留一次切换前恢复备份，不维持双版本并行。

## Implementation Steps

1. 检查活动文件、同步副本和候选 artifact 的版本与哈希。
2. 在仓库外备份 `27.5.1` 规则和切换前 Skill。
3. 安装 `27.6.0` 规则及同代 Skill。
4. 校验版本、日期、同步哈希、覆盖锚点、Skill 结构和体量阈值。

## Key Decisions

- `27.6.0` 成为唯一活动全局版本，`27.5.1` 仅作为恢复证据保留。
- 全局文件保持精简，详细行为继续由 Skill references 按需加载。
- 安装不改写已定版 artifact，因此版本日期保持 `2026-07-10`。

## Change List

- 活动全局 `AGENTS.md`：`27.5.1` 更新为 `27.6.0`。
- 同步副本：更新为相同 artifact。
- 活动 `seer-codex-rules`：同步 `27.6.0` 覆盖和护栏实现。
- `docs/PROGRESS.md` 和本轮记录。

## Tests And Verification

- 比较活动规则、同步副本和 canonical artifact 的 SHA256。
- 运行 `measure_rules.py --strict`。
- 运行 Skill 结构校验和 `guardrail_check.py --strict`。
- 独立检查覆盖清单来源版本、来源哈希和仓库外私有快照状态。

## Documentation Updates

更新进度总览并新增本轮记录；现有文档索引已经覆盖 `rounds/` 目录，无需逐文件增加索引。

## Risks And Follow-Up

文本规则和 Skill 门禁可以显著降低执行偏移，但不能替代权限、测试、CI 或人工安全确认。

## Next Step

后续规则细节优先更新 Skill；只有全局纲要或门禁语义改变时才推进全局版本。
