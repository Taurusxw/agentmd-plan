# AGENTS.md

> Global Codex operating outline.
> 版本：30.0.0
> 定版日期：2026-08-20

## Core conduct

1. Understand and verify before judging or changing. Reuse the project's architecture, conventions, tools, and documentation.
2. Keep changes small, complete, reviewable, and proportionate to risk. Preserve user and unrelated work.
3. Read-only requests remain read-only. A change request authorizes in-scope local edits and non-destructive validation; confirm only external writes, destructive or irreversible actions, purchases, credentials, or material scope expansion.
4. Runtime sandbox, approval, permission, hooks, tests, and CI enforce boundaries. Do not replace them with prose or repeated confirmation.
5. Use the smallest credible validation, reuse valid evidence, and close once the stated acceptance is met. Report changes, validation, gaps, and residual risk honestly.

## Rule locations and authority

1. Follow the effective instruction hierarchy; nearer project and directory rules may add narrower requirements.
2. Keep universal habits here, project facts in project `AGENTS.md`, local conventions in subdirectory rules, and branching workflows in Skills. Put hard controls in runtime tooling.
3. An `AGENTS.override.md` is allowed for a clearly temporary, narrow exception required by the current task. Name its target and restoration owner, preserve the prior effective rules, and remove or restore it when the exception ends; the user need not name the override file verbatim.
4. The host-loaded live global rules are current for the task. Do not replace them from old context, artifacts, snapshots, or a higher version found elsewhere.
5. Global rules, synchronized copies, and `seer-codex-rules` are maintained only by an explicit governance task in the `agentmd-plan` owner project. Elsewhere, inspect read-only and provide a detailed change report.

## Task scale

| Level | Default closure |
|---|---|
| L0 analysis | Read evidence and report; do not write traceability. |
| L1 small change | Minimal edit and direct check. |
| L2 normal development | Focused behavior check and existing project traceability where applicable. |
| L3 material change | Plan affected risks, decisions, and targeted validation. |
| L4 phase or release | Use the established phase or release record. |

Escalate for public contracts, data, authorization, deployment, dependencies, compatibility, difficult rollback, or material cross-module risk.

## Governance Skill triggers

Use `seer-codex-rules` for rule or `AGENTS.md` work; version, progress, or documentation governance; releases, migrations, global synchronization or recovery; architecture drift; Goal or acceptance expansion; and multi-agent routing. Ordinary L1/L2 file edits use the project workflow and focused validation without a universal compliance check.

For a matching Skill, read its `SKILL.md` and only the references it routes for the current work. If a governance-sensitive check fails or cannot run, report that limitation rather than claiming compliance.

## Execution and closure

Search affected code, configuration, tests, and docs before editing. Avoid unrelated refactors, duplicated rules, overloaded modules, and speculative hardening. Check references, imports, paths, types, names, generated outputs, and user-visible rendering when they are affected.

Documentation and version records follow actual impact and project conventions; do not create process artifacts merely because a file changed. A byte comparison is off by default and is used once only when an actual global/live synchronization or recovery consumer requires it.

For a persistent Goal, freeze a small completion contract before implementation. New findings enter current scope only when they block that contract, are a regression introduced by the work, or present a material safety risk; otherwise record a follow-up.

## Multi-agent work

Before delegation, identify independent packets and delegate only when a bounded, disjoint packet has a concrete net benefit. Keep scope, critical-path decisions, write ownership, integration, final validation, and user reporting in the root.

Immediately before each spawn, assess required access and capability scope against the parent's current effective access. Use compact packets and compact evidence; role configuration is not runtime permission proof. Stop fan-out when work overlaps, evidence repeats, coordination outweighs benefit, or acceptance is covered. Read `seer-codex-rules/references/multi-agent-governance.md` for the detailed gate.
