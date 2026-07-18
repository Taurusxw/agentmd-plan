# Goal Mode Closure

Use this reference only for a persistent Goal that can resume or auto-continue across turns. Its purpose is to make completion finite without weakening real correctness or safety requirements.

## Core Invariant

`required work` means work needed to satisfy the frozen Completion Contract, repair a regression introduced by the current change, or address a material security, permission, privacy, data-integrity, irreversible-loss, or release-safety risk. It does not mean every improvement discovered while the Goal remains active.

Admit only the smallest work needed to contain or explicitly escalate a material safety risk; do not use this exception to justify unrelated quality improvements.

## Completion Contract

Before implementation, normalize the Goal objective into this compact contract:

```text
Outcome: <one observable deliverable>
Frozen Criteria: <3-5 pass/fail conditions>
Non-Goals: <important exclusions, at most 3>
Validation Budget: <fixed checks and at most one task-scoped repair/retest>
Closure: complete immediately when all criteria pass; optional findings are follow-ups.
```

Keep the contract in the Goal objective so continuations can use it without rereading project history. Do not create a separate project document unless L3/L4 handoff already requires one.

## Normalize Open-Ended Language

Do not execute words such as "fully", "completely", "perfect", "all cases", "no omissions", "as much as possible", or "best" as unbounded requirements. Convert each into an observable criterion or declared support boundary. Ask only when the ambiguity materially changes data, permissions, deployment, destructive behavior, or critical user experience.

After implementation begins, Frozen Criteria remain unchanged unless:

- the user explicitly expands or changes scope;
- a criterion is internally contradictory or impossible and needs a user decision;
- a material safety risk requires a narrowly scoped addition.

Do not silently rewrite the contract merely because a stronger implementation or proof is imaginable.

## Required-Work Admission

Classify every new finding before acting:

| Finding | Current Goal |
|---|---|
| A Frozen Criterion fails on supported input | Required: fix and run the smallest affected check |
| Current changes introduce a direct regression | Required: repair the regression |
| Material security, permission, privacy, data, irreversible-loss, or release-safety risk | Required or explicitly escalated |
| External auth, rate limit, unavailable service, hardware, or human evidence blocks an optional check | Residual risk; do not keep retrying |
| Realistic improvement outside Frozen Criteria | Follow-up; do not implement automatically |
| Hypothetical or unsupported edge | Omit or record briefly; not required |
| New module, dependency, platform, schema, migration, or public contract | Scope expansion; require user approval |

A cheap fix is not automatically required. Ordinary edge work needs both evidence and failure of a Frozen Criterion.

## Execution State Machine

1. `contract`: create or normalize the Completion Contract once.
2. `core`: implement only work that advances a Frozen Criterion.
3. `verify`: run the fixed validation list once; do not add gates after it passes.
4. `repair`: if a task-scoped failure appears, allow one focused repair and affected retest.
5. `classify`: route new findings through Required-Work Admission.
6. `close`: when all Frozen Criteria pass, mark the Goal `complete` immediately.

Do not create or launch another Goal automatically. List at most three useful follow-ups in the final answer.

## One-Probe Rule

An unproven edge gets at most one cheap, focused reproduction attempt. If it cannot be reproduced against supported input or the declared contract, stop. Do not build a recovery branch, fixture suite, or validation framework for it in the current Goal.

## No Recursive Hardening

Tests, scripts, fixtures, validators, and release checks created to prove the Frozen Criteria are supporting evidence. Do not recursively harden their hypothetical edge conditions unless their failure prevents them from proving a criterion or creates a material safety risk.

Once a check passes, do not rerun it unless relevant code, data, configuration, or environment changed. Prefer affected checks over another full-suite pass.

## No-Progress Circuit Breaker

Every continuation must do at least one of these:

- move a Frozen Criterion from failing or unknown to passing;
- reduce a verified blocker that prevents a Frozen Criterion;
- produce the fixed acceptance evidence needed for closure.

If one continuation makes none of this progress, allow one diagnostic continuation only when a Frozen Criterion is still genuinely blocked. If the next continuation also makes no contract progress:

- close immediately when all criteria already pass;
- stop optional hardening and report residual risk;
- when a real criterion remains blocked, follow the active Goal tool's blocked-status threshold without inventing substitute work.

This circuit breaker does not lower a platform-required blocked threshold and does not allow completion when a Frozen Criterion is still unmet.

## Completion Decision

1. Any Frozen Criterion still fails: continue only the required repair path.
2. A true external blocker prevents a criterion: record evidence and follow blocked-status rules.
3. All Frozen Criteria pass: mark `complete`, even if optional improvements remain.
4. Optional findings exist: list zero to three follow-ups; they are not `required work`.

Use one compact status line during continuation or closure: `Goal contract: <passed>/<total>; blocker: <none/brief>; optional findings: <count>; action: <continue|complete|blocked-audit>.`

Do not paste the full contract every turn unless it changed through an authorized scope decision.
