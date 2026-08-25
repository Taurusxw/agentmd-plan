---
name: seer-codex-rules
description: Govern rules/AGENTS.md, version/progress/docs, release/migration/global sync/recovery, Goal/acceptance expansion, architecture drift, multi-agent routing; not routine L1/L2 edits.
---

# Seer Codex Rules

Keep the global outline short. Put project facts in project rules, detailed repeatable governance in references, and enforceable boundaries in runtime controls.

## Modes

- `compliance-check`: a targeted governance check only for rules or `AGENTS.md`, version/progress/docs governance, release/migration/global sync or recovery, architecture drift, Goal/acceptance expansion, or multi-agent work.
- `audit-only`: inspect governance material and report findings without editing.
- `patch-rules` or `migrate-rules`: refine, compact, or relocate an existing rule system.
- `skill-maintenance`: maintain this Skill and its direct support resources.
- `agent-orchestration`: assess independent packets, live effective access, and net benefit before delegation.
- `governance-change-report`: outside the owner project, inspect protected assets read-only and prepare a user-mediated report.

Routine L1/L2 code, configuration, or documentation edits do not invoke a universal compliance check. Follow their project workflow and run focused validation.

## Use

1. Read the effective `AGENTS.md` chain and identify the target, authority, write set, and smallest proof of completion.
2. Before writing protected global governance assets, read [governance ownership](references/governance-ownership-boundary.md) and pass its Owner Context Gate. Otherwise use report-only mode.
3. Read only the reference that matches the sensitive trigger:
   - rule destination or versions: [rule governance](references/rule-governance.md);
   - scale and authorization: [task scaling](references/task-scaling-and-context.md);
   - documentation/progress: [documentation governance](references/documentation-governance.md);
   - global candidate coverage: [global coverage](references/global-agents-coverage.md) and [rule inventory](references/global-agents-rule-inventory.md);
   - Goal or acceptance expansion: [Goal closure](references/goal-mode-closure.md) or [acceptance closure](references/acceptance-closure.md);
   - repeated hotspot or broadened responsibility: [architecture drift](references/architecture-drift.md);
   - child routing: [multi-agent governance](references/multi-agent-governance.md).
   - execution, change boundaries, project-rule templates, or final governance review: [execution standards](references/execution-standards.md), [code-change governance](references/code-change-governance.md), [project template](references/project-agents-template.md), or [rule review](references/rule-review-checklist.md).
   - lowest-cost governance routing: [low-token guardrails](references/low-token-guardrails.md).
4. Keep changes in the narrowest responsible file. Use a temporary `AGENTS.override.md` only when the current task clearly needs a narrow exception with a named scope and restoration plan; the user need not name the override file verbatim.
5. Choose the affected script via [verification and reporting](references/verification-and-reporting.md): `measure_rules.py` for rule size, `structure_check.py` for drift, `agent_routing_check.py` for routing, or `skill_catalog_check.py` for global catalog discovery/enablement. Scripts are under `scripts/`.
6. Use `scripts/guardrail_check.py` for governance-sensitive global/rule checks, not ordinary edits. Run `scripts/quick_validate.py <skill-dir>` when available for Skill maintenance. A byte comparison is off by default; perform one final comparison only for an actual global/live sync or recovery consumer.

Plans, checks, reports, documentation, manifests, and other governance artifacts are supporting evidence, not substitutes for the requested deliverable. If the user or authoritative evidence corrects a premise, discard the dependent route and evidence before continuing. Once the selected proof passes, stop; do not add post-validation writes, checks, or process work.

## Multi-agent boundary

Delegate only a bounded, independently verifiable, disjoint packet with a named net benefit. Immediately before every spawn, compare the packet's required access and capability scope with the parent's current effective access. Keep scope, critical-path decisions, write ownership, integration, final validation, and the final answer in the root. Static roles and configuration never prove runtime permission.

Use compact fresh packets unless continuity materially helps. Child returns contain the conclusion or patch, exact evidence, focused validation, and one residual risk; do not request raw logs or integrity metadata by default. Recursive delegation requires explicit authorization in the parent packet and the same gates.

## Reporting

State the changed destination, version rationale when applicable, focused evidence, and residual risk. Lead with the result; omit routine tool narration, repeated status or rules, generic praise or apology, and unnecessary sign-offs. Do not claim compliance when a required governance check is unavailable or fails.
