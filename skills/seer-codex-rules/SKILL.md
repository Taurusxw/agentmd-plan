---
name: seer-codex-rules
description: Design, revise, audit, version, compact, migrate, and maintain Codex rule systems, and act as a lightweight compliance gate for file-changing development tasks. Use for AGENTS.md, project rules, Codex workflows, task-level checks, documentation governance, progress records, versioning, rule migration, or start/end compliance checks that route to detailed rule modules.
---

# Seer Codex Rules

## Overview

Use this skill to govern Codex rule systems without letting global `AGENTS.md` become an unmaintainable manual. Keep universal behavior in global rules, project facts in project rules, detailed repeatable workflows in Skills, and hard enforcement in tools such as sandboxing, approvals, hooks, tests, or CI.

## Operating Modes

- `compliance-check`: apply the lightweight start/end rule check for an ordinary file-changing development task.
- `audit-only`: inspect rule files and produce findings; do not edit.
- `patch-rules`: update an existing global, project, or module rule file.
- `design-system`: propose a new rule architecture, version policy, or documentation model.
- `migrate-rules`: move oversized or specialized guidance from `AGENTS.md` into a Skill or project document.
- `skill-maintenance`: create or refine a Codex Skill that carries complex workflow rules.

Use the smallest mode that satisfies the request. If the user asks for execution or says to proceed, edit files directly after reading the relevant context.

## Core Workflow

1. **Establish authority and scope**
   - Read the nearest effective `AGENTS.md` chain and every user-mentioned rule file.
   - When a provenance project exists, inspect its project `AGENTS.md` and `README.md` when relevant.
   - Identify whether the target is global rules, project rules, a subdirectory rule, a Skill, project docs, or enforcement tooling.
   - For low-token compliance, read `references/low-token-guardrails.md` and apply the smallest required guardrail tier.
   - For ordinary development, load only `task-scaling-and-context.md` plus the one artifact-specific reference needed by the task; do not run the full rule-project preflight.

2. **Measure before changing**
   - Run `scripts/measure_rules.py` on existing rule files or documentation directories when size, versioning, duplication, or round organization matters.
   - Check current version headers, dates, line counts, byte size, and progress directory counts before deciding the change shape.
   - For global-rule parity work, read `references/global-agents-coverage.md` and mark every global section as covered, deliberately omitted, or delegated.

3. **Choose the rule home**
   - Keep global `AGENTS.md` for universal habits, task levels, safety baselines, and concise default workflows.
   - Use project `AGENTS.md` for stack, commands, project-specific directories, completion standards, and collaboration boundaries.
   - Use subdirectory `AGENTS.md` for local module rules that should not affect the whole project.
   - Use a Skill for repeatable, branching, detailed, or cross-project workflows that would bloat global rules.
   - Use docs such as `docs/RULES.md`, `docs/ARCHITECTURE.md`, or `docs/PROGRESS.md` for project knowledge, not universal agent behavior.
   - Use sandbox, permissions, hooks, tests, or CI for hard blocking; do not rely on prose for high-risk enforcement.

4. **Classify impact and version bump**
   - Read `references/rule-governance.md` when modifying versioned rule files or deciding `PATCH`, `MINOR`, or `MAJOR`.
   - Apply the highest-impact change across the edited file.
   - Do not bump versions for discussion, research, backups, or unchanged files.
   - Treat substantive updates to this skill as skill maintenance; do not bump global `AGENTS.md` unless that file changes.

5. **Edit conservatively**
   - Remove or relocate duplication instead of adding another synonymous section.
   - Preserve user-authored changes and existing project conventions.
   - Do not create extra README, changelog, notes, or summary files inside a Skill unless the skill standard explicitly requires them.
   - For Skills, keep `SKILL.md` concise and route detailed material to one-level `references/` files.

6. **Validate**
   - For Skills, run the skill creator validator on the skill directory.
   - For rule files, re-run measurement, check version/date consistency, inspect diffs, and verify any synchronized copies.
   - For projects with progress docs, check whether a round, phase, release, changelog, or doc index update is actually warranted.
   - After substantial changes to this Skill, run `scripts/snapshot_state.py --write` so the formal project contains a current recoverable snapshot and state manifest.
   - Use strict guardrails for global sync or release; ordinary compliance checks stay lightweight.

7. **Report clearly**
   - State what changed, why that destination was chosen, version bump rationale, validation performed, and residual risk.
   - If no file changed, say that no version bump was needed.

## Reference Routing

- Read `references/rule-governance.md` for rule destination decisions, versioning, and examples such as `25.1.1` to `25.1.2`, `25.2.0`, or `26.0.0`.
- Read `references/low-token-guardrails.md` for multi-layer compliance controls that minimize context usage.
- Read `references/global-agents-coverage.md` when checking whether this skill covers every rule currently expressed in global `AGENTS.md`.
- Read `references/global-agents-rule-inventory.md` for item-level coverage of the current global `AGENTS.md` rules.
- Read `references/task-scaling-and-context.md` for L0-L4 task classification, context reading depth, Skill use, and external-source decisions.
- Read `references/acceptance-closure.md` when acceptance, release, QA, preflight, live validation, or repeated verification starts expanding the task.
- Read `references/execution-standards.md` for the eight execution principles, ambiguity handling, fact checking, reuse, and business alignment.
- Read `references/code-change-governance.md` for code-edit boundaries, module splitting, user-change protection, and destructive-operation review.
- Read `references/documentation-governance.md` for document thresholds, round overflow, phase promotion, release folders, and doc-sprawl controls.
- Read `references/verification-and-reporting.md` for validation depth, output shape, risk disclosure, and final response requirements.
- Read `references/project-agents-template.md` when creating or reviewing lightweight project-level `AGENTS.md` files.
- Read `references/rule-review-checklist.md` for audits, refactors, and final review before touching global rules.
- Run `scripts/measure_rules.py` for deterministic line, byte, version, date, and progress-directory checks.
- Run `scripts/guardrail_check.py` for a low-token preflight over global gate, dynamic reference routing, coverage anchors, synchronized copies, current state, and project provenance.
- Run `scripts/snapshot_state.py --write` after substantive Skill changes to refresh the canonical Skill snapshot and `artifacts/current-state.json`.

## Safety Rules

- Never treat `AGENTS.md` as the only safety boundary for destructive, secret-bearing, permission-sensitive, legal, financial, or deployment-critical actions.
- Do not keep adding global rules after the file crosses its warning thresholds; propose extraction to a Skill or project-specific rule.
- Do not delete, rename, archive, or migrate historical rule material unless the user approved that scope or the project rule explicitly permits it.
- Do not create duplicate long-term document names for the same responsibility.
- Do not silently change version semantics; if the versioning model itself changes, classify it as at least a `MINOR` rule change and possibly `MAJOR`.
