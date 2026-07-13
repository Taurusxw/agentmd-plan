# Acceptance Closure

Use this reference when a task risks turning into endless acceptance, repeated QA, expanding release gates, or long-running validation loops.

## Core Rule

Acceptance proves the current goal is good enough to close. It must not keep generating new mandatory work unless the user explicitly expands scope or a true blocker prevents safe completion.

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

If three consecutive acceptance iterations produce process hardening rather than user-visible progress, stop and ask whether to close or open a new phase.

## Final Answer Requirements

When closing after bounded acceptance, include:

- what acceptance criteria were covered;
- what was not covered and why;
- whether remaining items are blockers or follow-ups;
- clear completion status.

Keep it concise. Do not paste every validation loop unless the user asks for an audit trail.
