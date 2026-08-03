# 2026-08-03 Round 004: Latest Effective Global Rule 28.2.0

## Status

completed

## Goal

Make every task follow the latest effective global rules without allowing old context to downgrade behavior, autonomous version scanning to bypass the instruction chain, or non-owner projects to modify protected governance assets.

## Evidence

- Conversation summaries, old artifacts, README files, snapshots, and formal Releases can legitimately describe an older rule version.
- Selecting the highest semantic version found on disk or remotely would add token and latency cost and could activate an uninstalled candidate without authorization.
- Codex task instructions are supplied by the host; changing a file during an active task does not prove that the active instruction chain hot-reloaded it.
- The existing Owner Context Gate already defines where drift may be repaired safely.

## Decisions

- Define "latest" as the current effective live global rules actually supplied or explicitly reloaded by the host for the task.
- Prohibit old conversations, cached summaries, artifacts, Releases, README files, snapshots, and project notes from downgrading that loaded rule set.
- Prohibit autonomous local or remote discovery of the highest semantic version as a rule-switching mechanism.
- Preserve normal instruction priority and let project or subdirectory rules add valid narrower behavior.
- Treat mid-task changes as effective only after a new task or explicit host reload.
- Keep freshness checks event-triggered so normal tasks do not spend tokens scanning governance history.
- Keep all reconciliation subject to the Owner Context Gate; non-owner contexts remain report-only.
- Classify `28.1.0 -> 28.2.0` as `MINOR` because it adds a durable global behavior and validation capability without changing the compatibility model.

## Changed Surfaces

- `28.2.0` global candidate and patch rationale.
- Skill router, centralized ownership reference, and low-token guardrails.
- Guardrail anchors and a dedicated unit test.
- Coverage matrix, rule inventory, bilingual manuals, progress, and document index.
- Installed global and Skill copies plus ignored private recovery state.

## Validation

- Skill creator validation and Python compilation passed.
- All ten unit tests passed, including the dedicated latest-effective-rule anchor test.
- Strict measurement passed at 98 non-empty lines and 12,769 bytes.
- Strict guardrail passed with no warnings and a current state manifest anchored to `28.2.0`.
- The candidate, live global file, and Downloads copy share SHA256 `468D961BF23A6DFB1EF47D4344EEEF69655D8A7EB2308271AD6F49FFF724EB9F`.
- The project, Codex, and Skills Manager Skill trees each contain 26 files and share tree SHA256 `49E923A264136EB591BB531D283DDD0AAC275B6C4E8AD8E20FFD97D2C9C34A95`.
- Version-boundary scan and Git whitespace inspection passed; `VERSION` remains the formal `28.1.0` baseline.

## Residual Risk

Prose cannot force a running Codex task to hot-reload a rule file. The mechanism guarantees what compliant tasks do with the instruction chain they actually receive; host reload or a new task remains necessary after a mid-task global-rule update.
