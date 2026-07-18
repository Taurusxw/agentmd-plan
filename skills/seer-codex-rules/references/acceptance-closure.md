# Acceptance Closure

Use this reference when a task risks turning into endless acceptance, repeated QA, expanding release gates, or long-running validation loops.

## Core Rule

Acceptance proves the current goal is good enough to close. It must not keep generating new mandatory work unless the user explicitly expands scope or a true blocker prevents safe completion. For persistent Goal mode, `goal-mode-closure.md` freezes the completion contract that defines what "original goal" and `required work` mean.

## Edge-Condition Scope Gate

Apply this gate only when an edge condition is encountered or supported by evidence. Do not spend time enumerating hypothetical edge cases before implementing the requested behavior.

Classify each newly discovered condition before developing it:

| Class | Current-Task Action |
|---|---|
| Core defect | Fix now when valid, supported input fails or the original acceptance criteria cannot pass. |
| Critical risk | Fix or explicitly escalate when security, permissions, privacy, data integrity, irreversible loss, or release safety is materially affected. |
| Evidenced hardening | Fix only when the condition is realistic, directly related to the goal, locally solvable, and covered by a focused test. |
| Speculative edge | Record briefly as a non-blocking risk or omit when it requires several unlikely assumptions and has no observed evidence. |
| Scope expansion | Ask for a scope decision or create a follow-up when handling it requires a new module, dependency, schema, public contract, migration, or comparable expansion. |

An ordinary edge condition enters the current scope only when all of these are true:

1. Evidence exists in a user example, supported input, failing test, production symptom, documented contract, or credible operational scenario.
2. It directly affects the original goal or declared support boundary.
3. The fix is proportionate and can be verified without opening a new workstream.

Critical security, permission, privacy, and data-integrity risks may override the ordinary admission test. A cheap fix alone is not enough reason to expand scope, and defensive code must not silently broaden the supported contract.

At public or external trust boundaries, validate malformed input according to the documented contract. For internal states that should be impossible, prefer a clear invariant or explicit failure over a large recovery tree unless recovery is an actual requirement.

## Edge-Development Budget

- L1: fix only the directly requested behavior and proven defects; do not add speculative hardening.
- L2: allow at most one focused edge-hardening pass after the core workflow works; route further non-blocking findings to follow-up.
- L3: use the planned risk and acceptance checklist; every newly discovered edge still passes the scope gate.
- L4: use the phase or release checklist; a new mandatory edge requires a true blocker, critical risk, or explicit scope expansion.
- If two consecutive implementation or validation iterations improve only hypothetical robustness and do not advance the original user outcome, stop and close or propose a separate task.

Keep the gate low-token: one short classification and decision is enough unless the condition is a blocker or critical risk.

## Closure Budget

Before running more validation, classify the current state:

| State | Action |
|---|---|
| Original acceptance criteria passed | Stop, summarize, and close. |
| Core user workflow verified by targeted tests or realistic sample | Stop unless a blocker remains. |
| External site/auth/risk-control blocks live validation | Record as residual risk or optional follow-up, not an automatic release blocker. |
| New issue is outside original goal | Create follow-up or risk note; do not keep expanding current task. |
| New issue blocks the original goal | Fix it, run the smallest relevant verification, then stop. |

Default validation budget:

- L1: one direct verification pass.
- L2: one targeted test pass plus one focused retry if the first pass reveals a task-scoped bug.
- L3: planned acceptance checklist; no new gates after checklist passes unless a blocker appears.
- L4: phase/release acceptance checklist; new gates require explicit scope decision.

## Stop Conditions

Stop and produce the final answer when any of these is true:

- the requested behavior is implemented and directly verified;
- the user says "别磨叽", "别堆验收", "确认没问题就结束", or equivalent;
- remaining validation depends on external auth, rate limits, paid services, unavailable hardware, or human-only data;
- further work would harden tools rather than validate the requested user outcome;
- the next check would be another variant of an already passing check.

## Anti-Patterns

Avoid:

- adding new release gates while trying to close an existing release;
- treating optional live evidence as mandatory after core workflow tests pass;
- fixing the acceptance harness indefinitely instead of shipping the user-requested change;
- turning every discovered edge case into current-scope work;
- updating many docs repeatedly for each minor validation pass;
- keeping the goal active only because a stronger proof could theoretically exist.

## External Validation Blocks

When live validation is blocked by login, permission, rate limit, risk control, geo, third-party instability, or unavailable user credentials:

1. classify it as external blocked evidence;
2. preserve the best local or fixture-based proof;
3. state residual risk;
4. close if the user goal is otherwise verified;
5. create optional follow-up only if useful.

Do not keep retrying the same blocked live path unless the user provides new credentials, new environment, or explicitly asks for another attempt.

## New Findings During Acceptance

Use this rule:

- `blocks original goal`: fix now.
- `affects release safety materially`: ask or record explicit scope decision.
- `hardens future process`: follow-up, not current blocker.
- `nice-to-have or broader improvement`: backlog.

If acceptance iterations produce process hardening rather than user-visible progress, apply the Goal no-progress circuit breaker. When the frozen criteria pass, close automatically and list optional follow-ups without opening another phase or Goal. Ask only when an unresolved blocker materially changes scope.

## Final Answer Requirements

When closing after bounded acceptance, include:

- what acceptance criteria were covered;
- what was not covered and why;
- whether remaining items are blockers or follow-ups;
- clear completion status.

Keep it concise. Do not paste every validation loop unless the user asks for an audit trail.
