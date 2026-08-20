# Global AGENTS Rule Inventory

This inventory maps `<codex-home>/AGENTS.md` version `29.1.0` to detailed `seer-codex-rules` modules and explicitly routed companion Skills.

Source global version: `29.1.0`
Source global SHA256: `2A84F623607689C1709B6F3F3C6E17154B7CF9326A4369238CB7101F43BECCC5`
Coverage verified: `2026-08-20`

## 1. Core Principles

| Global Rule | Coverage |
|---|---|
| Understand and verify before judging or editing | `execution-standards.md`, `task-scaling-and-context.md` |
| Prefer project architecture, naming, tools, and docs | `execution-standards.md`, `code-change-governance.md` |
| Keep changes small and complete | `code-change-governance.md` |
| Persistent changes are reviewable, verifiable, traceable, and handoff-ready | `verification-and-reporting.md`, `documentation-governance.md` |
| Scale workflow by risk and size | `task-scaling-and-context.md` |
| Avoid overloaded files, duplicate rules/docs, and shallow abstractions | `code-change-governance.md`, `documentation-governance.md` |
| Preserve user changes | `code-change-governance.md` |
| Read-only requests do not authorize implementation; change requests authorize in-scope local edits and non-destructive validation | `task-scaling-and-context.md` |
| Confirm external, destructive, costly, credential-bearing, or scope-expanding actions once per unchanged authorization envelope | `task-scaling-and-context.md`, `acceptance-closure.md` |
| Prose is not a second safety boundary; runtime controls enforce applicable risks | `rule-governance.md`, `task-scaling-and-context.md`, `verification-and-reporting.md` |
| Acceptance must close rather than expand the goal | `acceptance-closure.md` |
| Final answers disclose changes, validation, gaps, and risk | `verification-and-reporting.md` |
| Scan independent work before material execution and proactively delegate every packet that passes the benefit gate without requiring another user request or Ultra reasoning | `multi-agent-governance.md`, `low-token-guardrails.md`, `task-scaling-and-context.md` |
| Adapt each wave to ready packets, effective runtime capacity, and budget without a fixed governance ceiling or capacity-utilization target | `multi-agent-governance.md`, `low-token-guardrails.md` |
| Keep scope, critical path, write ownership, wave synthesis, integration, and final validation in the root; prevent duplicate or same-file work and close completed children | `multi-agent-governance.md` |
| Keep source-bearing research analysis-only by default; require explicit per-material Knowledge or Book authorization; prevent authorization carryover across conversations and workflows; preserve development-input isolation; record original/clickable/lawful-download links and truthful restrictions for every authorized deliverable | `<codex-home>/skills/seer-capture/SKILL.md`, `<codex-home>/skills/seer-capture/references/research-and-book-workflow.md` |
| Allow global `AGENTS.md`, synchronized-copy, and `seer-codex-rules` writes only in the dedicated `agentmd-plan` owner project; require every other project or conversation to produce a detailed user-mediated change report and prohibit indirect bypass | `governance-ownership-boundary.md`, `rule-governance.md`, `low-token-guardrails.md` |
| Always apply the current effective live global rules loaded by the host; prevent old context from downgrading them, prohibit autonomous highest-version switching, preserve instruction priority, and keep drift repair inside the owner boundary | `governance-ownership-boundary.md`, `low-token-guardrails.md`, `rule-governance.md` |

## 2. Instruction And Rule Locations

| Global Rule | Coverage |
|---|---|
| Follow valid instruction hierarchy and local project rules | `rule-governance.md`, `task-scaling-and-context.md` |
| Global rules contain only the always-on outline | `rule-governance.md` |
| Project and subdirectory rules contain narrower facts | `project-agents-template.md`, `rule-governance.md` |
| Complex workflows use Skills; knowledge uses docs; hard gates use tools | `rule-governance.md` |
| Do not create overrides without request | `rule-governance.md` |
| Explain material conflicts and tradeoffs | `execution-standards.md`, `verification-and-reporting.md` |

## 3. Task Levels

| Global Rule | Coverage |
|---|---|
| L0 read-only analysis | `task-scaling-and-context.md`, `verification-and-reporting.md` |
| L1 tiny change | `task-scaling-and-context.md`, `verification-and-reporting.md` |
| L2 normal development | `task-scaling-and-context.md`, `documentation-governance.md` |
| L3 important change | `task-scaling-and-context.md`, `documentation-governance.md`, `verification-and-reporting.md` |
| L4 phase or release | `task-scaling-and-context.md`, `documentation-governance.md` |
| Upgrade for contracts, data, auth, security, deploy, dependency, compatibility, rollback, cross-layer, duration, or handoff | `task-scaling-and-context.md` |
| Repeated patch hotspots plus responsibility, interface, duplication, or test-coupling drift upgrade to L3 | `task-scaling-and-context.md`, `architecture-drift.md` |
| Analysis-only requests remain L0 | `task-scaling-and-context.md` |

## 4. Mandatory Skill Gate

| Global Rule | Coverage |
|---|---|
| Read matching Skills before execution | `task-scaling-and-context.md`, `execution-standards.md` |
| File-changing development reads the Seer compliance gate once and reuses it at completion | `low-token-guardrails.md` |
| Ordinary work loads only the needed references | `low-token-guardrails.md`, `task-scaling-and-context.md` |
| Rule and release work runs guardrails | `low-token-guardrails.md`, `rule-review-checklist.md` |
| Final answers disclose Skill use and uncovered risk | `verification-and-reporting.md` |
| Missing or invalid mandatory Skill blocks compliance claims | `low-token-guardrails.md`, `verification-and-reporting.md` |
| Skills cannot override higher instructions or safety controls | `rule-governance.md` |
| Time-sensitive facts use current primary sources | `task-scaling-and-context.md`, `execution-standards.md` |
| Multi-agent, subagent, model-routing, context-isolation, and collaboration-token tasks load the dedicated governance reference | `multi-agent-governance.md`, `low-token-guardrails.md` |

## 5. Execution And Edit Baselines

| Global Rule | Coverage |
|---|---|
| Search facts first and prefer `rg` | `code-change-governance.md` |
| Execute safe in-scope work without reconfirmation and clarify only true authorization-boundary changes | `execution-standards.md`, `task-scaling-and-context.md` |
| Reuse existing modules and mature tools | `execution-standards.md`, `code-change-governance.md` |
| Avoid unrelated cleanup, hidden errors, and permanent hacks | `code-change-governance.md` |
| Prefer deep modules and meaningful boundaries | `code-change-governance.md` |
| Check imports, paths, types, tests, docs, and generated outputs | `code-change-governance.md` |
| Confirm delete, rename, migration, and history rewrite | `code-change-governance.md` |
| Preserve unexpected user-owned changes | `code-change-governance.md` |
| Run an event-triggered architecture-drift review for cumulative hotspots | `architecture-drift.md`, `code-change-governance.md` |
| Treat line count as a signal rather than a mandatory split verdict | `architecture-drift.md`, `code-change-governance.md` |

## 6. Documentation, Traceability, And Versions

| Global Rule | Coverage |
|---|---|
| Update docs by impact; avoid duplicate trees | `documentation-governance.md` |
| Documentation depth follows L0-L4 | `documentation-governance.md` |
| Continue the same round for the same objective | `documentation-governance.md` |
| Reset round numbering by date and route overflow without skipping records | `documentation-governance.md` |
| Organize after 30 rounds, archive after 100, promote themes after 5-8 | `documentation-governance.md` |
| Keep `PROGRESS.md` concise | `documentation-governance.md` |
| Extract global detail at size thresholds | `documentation-governance.md`, `rule-governance.md` |
| Detailed templates and algorithms live in the Skill | `documentation-governance.md` |
| Use MAJOR.MINOR.PATCH by highest impact | `rule-governance.md` |
| Keep history in artifacts, private state, backups, or Git | `rule-governance.md`, `verification-and-reporting.md` |

## 7. Validation And Acceptance Closure

| Global Rule | Coverage |
|---|---|
| Run the smallest credible validation | `verification-and-reporting.md` |
| Scale tests through direct, behavior, affected, and full validation steps | `verification-and-reporting.md` |
| Run full regression or security review only on explicit contract or real changed-boundary triggers | `verification-and-reporting.md` |
| Reuse passing evidence until a relevant change invalidates its coverage | `acceptance-closure.md`, `verification-and-reporting.md`, `goal-mode-closure.md` |
| Prefer bug-discriminating evidence over more unrelated passing checks | `verification-and-reporting.md` |
| Classify task-caused, pre-existing, transient, external, and unknown failures before retrying | `acceptance-closure.md`, `verification-and-reporting.md` |
| Render visual artifacts | `verification-and-reporting.md` |
| A zero exit code is not sufficient evidence | `verification-and-reporting.md` |
| Default to no hash/checksum/manifest; allow integrity metadata only for an explicit byte-identity consumer and never as a substitute for semantic, source, behavioral, test, or visual evidence | `verification-and-reporting.md`, `multi-agent-governance.md` |
| Disclose unrun checks and residual risk | `verification-and-reporting.md` |
| Stop after acceptance; classify external blocks as residual risk | `acceptance-closure.md` |
| Only blockers and material safety findings expand current scope | `acceptance-closure.md` |
| Persistent Goals freeze finite pass/fail criteria before implementation | `goal-mode-closure.md`, `acceptance-closure.md` |
| Passing Goal criteria close immediately; optional findings are not required work | `goal-mode-closure.md`, `verification-and-reporting.md` |

## 8. Completion Check

| Global Rule | Coverage |
|---|---|
| Report changed behavior and direct evidence once | `verification-and-reporting.md` |
| Decide docs, progress, index, release, and version updates once | `documentation-governance.md`, `rule-review-checklist.md` |
| Report material risk plus used Skills and references compactly | `verification-and-reporting.md`, `low-token-guardrails.md` |
| Keep short tasks concise and larger tasks structured | `verification-and-reporting.md` |
