# Task Scaling And Context Reference

Use this reference when deciding how much process, reading, documentation, and validation a Codex task needs.

## Task Level Decision Tree

Start at the lowest level and upgrade only when a condition applies.

| Level | Use When | Required Behavior |
|---|---|---|
| L0 read-only analysis | Explaining, reviewing, researching, locating, comparing, or answering without file edits | Read only necessary context, cite evidence, avoid progress records, do not modify files |
| L1 tiny change | One localized edit, wording adjustment, small config tweak, no public behavior change | Read the target and immediate neighbors, make the smallest complete edit, run direct verification |
| L2 normal development | Small feature, bug fix, user-visible behavior, 1-3 modules, routine docs impact | Read project rules and relevant docs/tests, update affected docs, run one targeted behavior pass, consider a round if the project already uses rounds |
| L3 important change | API, database, auth, security, architecture, dependency, deployment, data migration, or cross-module refactor | Form a plan, inspect impact, update only affected architecture/interface/change docs, run a risk-mapped validation set |
| L4 phase or release | Multi-day work, migration, release, audit, public delivery, multiple acceptance passes, handoff | Use phase or release structure and its fixed acceptance checklist; do not add gates while closing it |

## Upgrade Conditions

Upgrade at least one level when:

- the change affects public interfaces, data schemas, permissions, deployment, dependencies, compatibility, or user-visible workflows;
- the work touches more than three modules or crosses frontend/backend/service/data boundaries;
- rollback is difficult or failure cost is high;
- the user needs handoff evidence, auditability, or repeatable operations;
- uncertainty requires a plan before implementation;
- the same goal has spread across multiple rounds and needs a phase.
- the same production module is a repeated patch hotspot and the current change also adds a responsibility, broadens an entry interface, spreads duplication, or increases cross-subsystem test coupling; treat this as at least L3 and use `architecture-drift.md`.

Do not upgrade merely because an agent likes process. A safe one-turn fix should remain lightweight.

Words in a request or document such as `security`, `permission`, `deployment`, or `migration` are not upgrade triggers by themselves. Upgrade only when the requested change actually alters that runtime boundary.

Task level does not determine agent count. At every level, identify independently verifiable discovery, implementation, validation, or specialist-review packets; when the benefit gate in `multi-agent-governance.md` passes, proactively delegate them. A large but sequential or tightly coupled task still belongs in the root, while even a read-only task may justify multiple isolated research lanes.

An active persistent Goal does not automatically make work L4. Classify by actual risk and scope, then use `goal-mode-closure.md` to prevent auto-continuations from expanding the frozen objective.

## Reading Depth

Use the minimum context that can make the work correct.

| Level | Read Before Acting |
|---|---|
| L0 | User-mentioned files, nearest rules, specific evidence needed |
| L1 | Nearest rules, target file, immediate imports/tests/config |
| L2 | Project `AGENTS.md`, `README.md`, relevant source, relevant tests, affected docs |
| L3 | L2 plus architecture/API/database/development/rules/progress docs when present |
| L4 | L3 plus phase/release history, changelog, acceptance notes, release artifacts |

If a project lacks a standard doc, do not create the whole standard tree automatically. Create only what the task needs.

## Action Authorization Envelope

Treat authorization as one task-scoped envelope rather than a question before each safe action.

- Answer, explain, review, diagnose, research, and plan requests authorize necessary read-only inspection, but not implementation.
- Change, build, fix, optimize, update, and implement requests authorize in-scope local reading, editing, formatting, and non-destructive validation without another confirmation.
- Ask before external writes or publication, destructive or irreversible actions, purchases, credential disclosure, or material expansion into a new target, system, or risk class.
- If the user already authorized the same action class, target, and material risk in the current task, do not ask again. Reconfirm only when one of those three changes or the runtime requires a fresh approval.
- A denied or unavailable runtime capability is evidence of a boundary, not an invitation to repeat the question. Try one safe in-scope alternative when available, then report the block.

Runtime sandbox, approval, permission, app, and MCP controls remain authoritative. Prose must not simulate them with repeated safety reviews.

## Skill Use

Use a Skill when:

- the task directly names a Skill;
- the task clearly matches an available Skill description;
- the workflow is specialized, repeatable, or has known tooling;
- detailed rules would otherwise lengthen global `AGENTS.md`.

When using a Skill:

1. Read its `SKILL.md` completely.
2. Read only the referenced files needed for the current variant.
3. Prefer bundled scripts or assets when they exist.
4. Validate according to the Skill's own instructions.

When an independent packet exists, read `multi-agent-governance.md` once, apply its explicit delegation authorization, select the cheapest capable role, and do not load unrelated governance references into the child context.

## External Source Decisions

Use external sources when facts are time-sensitive, official behavior may have changed, or the task involves current software, laws, prices, schedules, APIs, cloud services, models, or product rules.

For technical or product behavior:

- prefer official documentation, source code, release notes, or primary references;
- mark assumptions and uncertainty;
- avoid writing guessed APIs, parameters, return values, commands, or limits into rules.

For OpenAI or Codex behavior:

- prefer official OpenAI documentation or local Codex docs/tools when available;
- treat screenshots and memories as secondary evidence.

## Boundary Decisions

Use the Action Authorization Envelope when the answer changes:

- destructive operations;
- data deletion, migration, or irreversible movement;
- security, permission, privacy, payment, legal, or deployment choices;
- user experience tradeoffs that are not inferable from the project;
- document migration that could invalidate existing references.

If a reasonable assumption is safe, reversible, and inside the envelope, proceed without asking and state it only when it materially affects the result.
