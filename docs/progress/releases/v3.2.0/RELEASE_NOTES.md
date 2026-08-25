# Agentmd Plan v3.2.0

## Status

Prepared on 2026-08-25 for publication after final source validation and maintainer-environment installation. Publication evidence will be recorded on `main` after GitHub confirms the release.

## 中文

`v3.2.0` 将 GPT-5.6 社区集中反馈的“过度生产”转成紧凑的全局行为与按需 Skill 细则，并按维护者要求将版本编号从 30.x 归一到 3.x。

### 主要内容

- 交付优先：计划、测试、审计、manifest、hash、文档和状态记录不能替代用户交付物。
- 纠正失效：前提被纠正后，废弃所有依赖旧前提的假设、计划、结论、动作和验证，只重建受影响路径。
- 复杂度准入：新增抽象、fallback、泛化边界或额外功能必须由当前契约、复现失败、项目惯例或重大风险支持。
- 达标硬停止：最终相关验证必须位于最后一次必要写入之后；通过后不再追加写入、复核或优化。
- 精简汇报：保留结果、必要证据和实质风险，省略例行工具叙述、重复状态/规则和泛化仪式话术。
- 配套更新 execution、Goal、acceptance、verification、coverage、inventory、guardrail 和定向测试。

## English

`v3.2.0` turns recurring GPT-5.6 over-production reports into compact global behavior and on-demand Skill guidance, while normalizing the maintainer-selected version line from 30.x to 3.x.

### Highlights

- Prioritizes the requested deliverable over plans, tests, audits, manifests, hashes, documentation, and status artifacts.
- Invalidates assumptions, plans, conclusions, pending actions, and evidence that depend on a corrected premise.
- Admits new abstractions, fallbacks, generalized edges, or features only for the current contract, a reproduced failure, an established convention, or a material risk.
- Stops after the last required mutation and final relevant check pass.
- Keeps reports outcome-led and removes routine tool narration, repeated state/rules, and generic ceremony.
- Updates execution, Goal, acceptance, verification, coverage, inventory, guardrail, and focused tests together.

## Publication Boundary

- The local checkout retains only the current versioned artifact, release record, and local tag.
- Git history and historical GitHub tags/Releases remain intact; no force-push or history rewrite is used.
- The live global rule, Downloads copy, and maintainer Skill are installed from this release source.
- The separate Skills distribution repository remains an independent publication target and is unchanged.
