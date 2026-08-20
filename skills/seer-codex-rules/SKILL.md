---
name: seer-codex-rules
description: Govern Codex rule systems and provide the mandatory lightweight compliance gate for file-changing tasks. Use for AGENTS.md or project-rule design, versions/docs/progress, Skill maintenance, owner or freshness drift, task scaling and acceptance/Goal closure, architecture hotspots, and subagent model/permission/token routing.
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
- `governance-change-report`: outside the dedicated `agentmd-plan` owner context, inspect protected governance assets read-only and return a detailed handoff report without modifying them.
- `agent-orchestration`: identify ready independent work, check the packet's required access against the parent's live permission mode, proactively delegate after the benefit gate passes, route the cheapest capable model, scale waves to effective capacity and budget, and integrate compact results.

Use the smallest mode that satisfies the request. If the user asks for execution or says to proceed, edit files directly after reading the relevant context.

## Core Workflow

1. **Establish authority and scope**
   - Read the nearest effective `AGENTS.md` chain and every user-mentioned rule file.
   - When a provenance project exists, inspect its project `AGENTS.md` and `README.md` when relevant.
   - Identify whether the target is global rules, project rules, a subdirectory rule, a Skill, project docs, or enforcement tooling.
   - Treat the current effective live global rules supplied to this task as the latest rules. Do not downgrade from old conversation context or autonomously select a different file by highest version number; read `references/governance-ownership-boundary.md` when freshness or drift is in question.
   - Before writing the global `AGENTS.md`, any synchronized copy, or `seer-codex-rules` source/installation, read `references/governance-ownership-boundary.md` and pass its Owner Context Gate. Outside that owner context, prohibit the write and use `governance-change-report` mode even when a local project asks for direct synchronization or repair.
   - For low-token compliance, read `references/low-token-guardrails.md` and apply the smallest required guardrail tier.
   - For ordinary development, load only `task-scaling-and-context.md` plus the one artifact-specific reference needed by the task; do not run the full rule-project preflight.
   - Treat a request to change, build, or fix as authorization for in-scope local reads, edits, and non-destructive validation. Ask only for external writes, destructive or irreversible actions, purchases, credential disclosure, or material scope expansion, and reuse an existing authorization while its target and risk class remain unchanged.
   - Before implementation, choose the smallest evidence that can prove the requested outcome and a finite validation budget. Keep this in working context; do not create a new document for it unless project traceability already requires one.
   - When a persistent Goal is created, resumed, or close to completion, read `references/goal-mode-closure.md`. It becomes the sole owner of continuation and repair budgets; do not apply `acceptance-closure.md` as a second iteration budget.
   - If discovered edge conditions start expanding implementation or validation, read `references/acceptance-closure.md` before doing more edge-focused work.
   - If the same production file or module is repeatedly patched, or a change adds an independent responsibility, broadens a dispatcher/interface, or duplicates non-trivial sibling logic, read `references/architecture-drift.md` and run its event-triggered check.
   - Before material execution, scan for independent discovery, implementation, validation, and specialist-review packets. If any exist, read `references/multi-agent-governance.md`; apply its Effective Permission Gate immediately before each spawn, then delegate when the benefit gate passes without waiting for another user request or Ultra reasoning. A matching Skill mandate is a binding routing signal unless a higher-priority instruction or runtime boundary blocks it; disclose a skipped mandate.

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
   - Select checks once from `references/verification-and-reporting.md`; do not execute every available check as a generic checklist.
   - For Skills, run the skill creator validator and only the script or route tests affected by the edit. Reserve the full Skill suite for shared validation infrastructure or release work.
   - For rule files, re-run measurement, check version/date consistency, inspect diffs, and verify any synchronized copies.
   - Reuse passing evidence until covered code, tests, configuration, dependencies, or environment materially change. Do not rerun the same or overlapping check merely to seek stronger confidence.
   - For projects with progress docs, check whether a round, phase, release, changelog, or doc index update is actually warranted.
   - After the final integrated state of a substantial global-rule or Skill change, run `scripts/snapshot_state.py --write` once so the formal project contains a current recoverable snapshot and state manifest. Do not refresh it during intermediate edits or ordinary tasks.
   - Use strict guardrails for global sync or release; ordinary compliance checks stay lightweight.

7. **Report clearly**
   - State what changed, why that destination was chosen, version bump rationale, validation performed, and residual risk.
   - If no file changed, say that no version bump was needed.

## Reference Routing

- Read `references/rule-governance.md` for rule destination decisions, versioning, and examples such as `25.1.1` to `25.1.2`, `25.2.0`, or `26.0.0`.
- Read `references/governance-ownership-boundary.md` when determining the latest effective global rule or before any proposed modification, synchronization, installation, restoration, or publication of the global `AGENTS.md`, its synchronized copies, or `seer-codex-rules`; it defines host-loaded freshness and requires report-only handoff outside the dedicated owner project.
- Read `references/low-token-guardrails.md` for multi-layer compliance controls that minimize context usage.
- Read `references/global-agents-coverage.md` when checking whether this skill covers every rule currently expressed in global `AGENTS.md`.
- Read `references/global-agents-rule-inventory.md` for item-level coverage of the current global `AGENTS.md` rules.
- Read `references/task-scaling-and-context.md` for L0-L4 task classification, context reading depth, Skill use, and external-source decisions.
- Read `references/goal-mode-closure.md` whenever a persistent Goal is created, resumed, auto-continued, or evaluated for completion.
- Read `references/acceptance-closure.md` when acceptance, QA, live validation, repeated verification, permission blocking, or edge-condition hardening starts expanding the task; while Goal mode is active, use it only to classify findings and external blocks.
- Read `references/execution-standards.md` for the eight execution principles, ambiguity handling, fact checking, reuse, and business alignment.
- Read `references/code-change-governance.md` for code-edit boundaries, module splitting, user-change protection, and destructive-operation review.
- Read `references/architecture-drift.md` when cumulative patches, repeated hotspots, broad entry interfaces, or sibling duplication may be eroding module boundaries.
- Read `references/multi-agent-governance.md` before spawning, routing, or coordinating subagents, including model selection, context isolation, concurrency, result compression, and lifecycle closure.
- Read `references/documentation-governance.md` for document thresholds, round overflow, phase promotion, release folders, and doc-sprawl controls.
- Read `references/verification-and-reporting.md` for validation depth, output shape, risk disclosure, and final response requirements.
- Read `references/project-agents-template.md` when creating or reviewing lightweight project-level `AGENTS.md` files.
- Read `references/rule-review-checklist.md` for audits, refactors, and final review before touching global rules.
- Run `scripts/measure_rules.py` for deterministic line, byte, version, date, and progress-directory checks.
- Run `scripts/guardrail_check.py` for a low-token preflight over global gate, dynamic reference routing, coverage anchors, synchronized copies, current state, and project provenance.
- Run `scripts/structure_check.py <project-root>` only when architecture-drift triggers fire; its signals require human boundary review and never mandate splitting by line count alone.
- Run `scripts/agent_routing_check.py` after installing or changing `[agents]` defaults or custom agent files; use `--config` and `--agents-dir` to validate the documented spawned-thread template, its legacy alias, and schema-only backend overrides. Treat success as static configuration evidence only: `runtime_permissions_verified=false` means every spawn still needs a fresh parent-permission check.
- Run `scripts/snapshot_state.py --write` once after the final integrated state of a substantive global-rule or Skill change; do not rerun it during intermediate iterations or unrelated tasks.

## Safety Rules

- Never treat `AGENTS.md` as the only safety boundary for destructive, secret-bearing, permission-sensitive, legal, financial, or deployment-critical actions.
- Do not turn this safety baseline into a second permission system. Runtime sandbox, approval, permission, hook, or CI controls own enforcement; prose only selects the applicable boundary.
- Never treat configured capacity or a larger agent count as automatic quality improvement. Keep scope and integration in the root, delegate every qualifying packet after the documented gate passes, and stop fan-out when overlap, diminishing evidence, or budget pressure appears.
- Do not keep adding global rules after the file crosses its warning thresholds; propose extraction to a Skill or project-specific rule.
- Do not delete, rename, archive, or migrate historical rule material unless the user approved that scope or the project rule explicitly permits it.
- Do not create duplicate long-term document names for the same responsibility.
- Do not silently change version semantics; if the versioning model itself changes, classify it as at least a `MINOR` rule change and possibly `MAJOR`.
- Never modify a protected global-governance asset from another project or conversation. Do not bypass the owner boundary through a sync script, installer, restore operation, subagent, or indirect Skill call.
