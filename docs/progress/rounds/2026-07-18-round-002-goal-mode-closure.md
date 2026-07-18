# 2026-07-18 Round 002: Goal Mode Closure

## Status

completed

## Goal

Prevent persistent Goal auto-continuations from converting optional edge conditions and validation-tool hardening into endless required work.

## Evidence

- Existing acceptance rules classify discovered edges but do not freeze a finite completion definition before implementation.
- The previous stop rule could ask whether to close after repeated hardening, leaving a persistent Goal waiting instead of completing automatically.
- A 186-round project contained 34 explicitly boundary-oriented round names versus 13 structure-oriented names. This does not prove those fixes were unnecessary, but it demonstrates the need to control automatic scope admission.

## Key Decisions

- Store the compact contract in the Goal objective instead of adding a project document or per-turn script.
- Limit Frozen Criteria to 3-5 observable pass/fail conditions.
- Treat only contract failures, current-change regressions, and material safety risks as automatic `required work`.
- Close automatically when criteria pass; list at most three optional follow-ups without launching another Goal.
- Preserve the active platform's blocked-status threshold when a real criterion remains blocked.

## Change List

- Global `AGENTS.md` candidate `27.8.0`.
- `goal-mode-closure.md` and related Skill routing/reference updates.
- Deterministic global/reference anchor checks and unit tests.
- Chinese and English manuals, coverage inventory, progress, and release records.

## Tests And Verification

- Skill structure and Python compilation.
- Four unit tests covering Goal gate anchors and architecture hotspot behavior.
- Strict candidate/live guardrails, hash synchronization, privacy scans, and GitHub release identity checks.

## Five-Pass Review

1. Contract scope: open-ended language is normalized once into 3-5 observable criteria and explicit non-goals.
2. Admission integrity: optional edges cannot become required work without a contract failure, introduced regression, or material safety risk.
3. Continuation closure: one diagnostic continuation is allowed only for a real blocker; passing criteria close automatically.
4. Safety compatibility: material risks remain admissible and the platform blocked-status threshold is preserved.
5. Token and maintainability: the global outline gains one line, the Goal reference stays below 100 lines, and no per-turn script or extra project document is required.

## Risks And Follow-Up

Prose and anchor checks cannot force every model continuation to classify findings perfectly. The frozen contract, Goal-state completion, and deterministic guardrail reduce drift while leaving material safety findings admissible.
