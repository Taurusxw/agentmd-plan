# 2026-08-03 Round 002: GPT-5.6 Execution Efficiency

## Status

completed

## Goal

Reduce repeated regression tests, permission questions, security reviews, and acceptance loops in current Codex with GPT-5.6 while preserving real runtime safety boundaries and credible evidence.

## Evidence

- GPT-5.6 official guidance says leaner prompts can improve evaluated coding-agent performance and materially reduce tokens, and warns that repeated approval wording can cause unnecessary requests for safe in-scope actions.
- The current global and Skill rules define validation, acceptance, permission, and safety behavior in several modules without a single precedence rule.
- A read-only Terra/high audit found duplicated validation baskets, start/end Skill re-entry, Goal and ordinary acceptance budgets, broad permission triggers, and a five-round coverage phrase.
- OpenAI Agents SDK, AutoGen, and LangGraph use explicit loop limits or termination conditions; OpenHands and Claude Code use runtime risk/permission layers so safe sandboxed actions can proceed without repeated prompts.
- Agentless demonstrates the value of a simple bounded localization-repair-validation workflow. A July 2026 study of 3,730 validation events found that many positive events did not distinguish the original bug, supporting evidence quality over test count.

## Decisions

- Advance the global rules from `27.12.0` to `27.13.0` as a `MINOR` behavior improvement and publish it as the formal project release after the candidate passes its release gate.
- Authorize in-scope local edits and non-destructive validation from change requests; confirm only real external, destructive, costly, credential-bearing, or scope-expanding actions.
- Reuse one authorization while action class, target, and material risk remain unchanged.
- Select validation through V0 direct, V1 behavior, V2 affected, and V3 full steps; require a trigger before moving upward.
- Keep passing evidence until a relevant invalidator appears and rerun only failed or invalidated affected checks.
- Make Goal mode the sole continuation budget and keep ordinary acceptance as a finding classifier.

## Changed Surfaces

- `artifacts/AGENTS-27.13.0.md` and its patch note.
- Skill router, task scaling, acceptance, Goal, low-token, code-change, verification, rule review, coverage, and guardrail anchors.
- Chinese and English manuals, project rules, progress overview, document index, release records, and this round.
- Installed global and Skill copies plus ignored private recovery state.

## Validation

- Run the Skill creator validator.
- Run the affected guardrail unit tests and Python compilation for the changed guardrail script.
- Measure the global candidate and compare synchronized hashes.
- Run strict guardrail against the candidate/live state after snapshot refresh.
- Inspect diff, Markdown links, stale version references, private paths, and whitespace.

## Residual Risk

Prompt rules reduce model over-execution but cannot hard-limit every future Codex loop. Runtime approval and sandbox behavior remain platform-owned, and the new static anchors verify rule presence rather than perfect semantic compliance.
