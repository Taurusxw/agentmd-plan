# 2026-08-03 Round 003: Explicit Persistence And Centralized Governance 28.1.0

## Status

completed

## Goal

Make source persistence explicit and prevent every non-owner project or conversation from directly changing the global `AGENTS.md` or `seer-codex-rules`, while preserving a detailed user-mediated proposal path.

## Evidence

- A prior Knowledge-project change altered global persistence behavior and affected unrelated conversations.
- Ordinary reading and research previously defaulted to Knowledge persistence without a per-material write instruction.
- The global and Skill rules did not identify one exclusive project with direct write authority.
- The formal `agentmd-plan` project already owns global artifacts, coverage inventory, recovery state, versioning, and release records.

## Decisions

- Keep ordinary reading, screenshots, files, URLs, and research analysis-only unless the user explicitly names the material and Knowledge or Book destination.
- Scope persistence authorization to the current named material, batch, route, and task; never inherit it across conversations or workflows.
- Make `agentmd-plan` the exclusive direct-write owner for global rules, synchronized copies, and `seer-codex-rules` source/installations.
- Require a three-part Owner Context Gate: canonical workspace, project ownership declaration, and an explicit governance-maintenance task.
- Keep every non-owner context read-only and require a detailed change report for user transfer, even when that context requests a direct write.
- Prohibit indirect bypass through synchronization, installation, restoration, automation, another Skill, or a subagent.
- Publish `27.13.0 -> 28.1.0` as `MAJOR` because both the default persistence model and global-governance write boundary change incompatibly.
- Keep only the final `28.1.0` candidate in this Git update; do not create a `28.0.0` commit, tag, or Release.

## Changed Surfaces

- Global candidate and project ownership rule.
- Bilingual manuals and routing language for explicit per-material Knowledge/Book authorization.
- Skill router and new `governance-ownership-boundary.md` reference.
- Guardrail required phrases, required reference anchors, and unit tests.
- Coverage matrix, rule inventory, bilingual manuals, progress, and candidate rationale.
- Installed global and Skill copies plus ignored private recovery state.

## Validation

- Skill creator validation, Python compilation, and all nine unit tests.
- Strict measurement and guardrail against candidate, live copies, installed Skill trees, and private state.
- Exact hash comparison across global copies and all three Skill trees.
- Version-boundary, documentation-link, and Git whitespace inspection.
- Git commit, remote `main`, `v28.1.0` tag, GitHub Release, remote `VERSION`, license, and visibility verification.

## Residual Risk

Prose and guardrail anchors strongly constrain compliant Agents but do not create an operating-system identity boundary between conversations. Runtime filesystem permissions cannot distinguish projects using the same user account, so repository ownership and the always-on global gate remain the practical enforcement layers.
