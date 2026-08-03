# Verification And Reporting Reference

Use this reference to select the smallest evidence set that proves a change and to report it without turning completion into another workflow.

## Validation Ladder

Move upward only when the lower level cannot cover the changed contract.

| Step | Evidence | Typical Use |
|---|---|---|
| V0 direct | Diff review, syntax/static check, import/reference check, or deterministic file comparison | Text, config, narrow refactor, generated metadata |
| V1 behavior | One focused reproduction, unit/contract test, realistic sample, or rendered inspection | Bug fix, feature, UI, API behavior |
| V2 affected | Tests, typecheck, lint, build, or integration checks for changed modules and their dependents | Shared module, cross-module behavior, public contract |
| V3 full | Full regression, end-to-end, release, migration, security, artifact, and rollback checks | Explicit release gate or genuinely broad risk |

Task-level selection:

- L0: source evidence only; no edit validation.
- L1: one V0 or V1 pass that directly covers the edit.
- L2: one V1 pass; add V2 only when a shared interface, dependent module, or tool-enforced contract changed.
- L3: freeze a small V1/V2 risk matrix before implementation; each check must name the risk it covers.
- L4: run the established phase or release checklist once against the final release state.

Do not run all steps by default. `acceptance-closure.md` owns retries and evidence invalidation; Goal mode uses `goal-mode-closure.md` as its sole iteration budget.

## Full-Suite Triggers

Run V3 full-suite or full-build validation only when at least one applies:

- the user, repository, CI, phase, or release contract explicitly requires it;
- a shared core, public API, schema, dependency graph, build system, runtime configuration, or broad compatibility boundary changed;
- targeted or affected checks cannot observe the requested behavior;
- a release, migration, rollback, or cross-system integration is being accepted.

A high reasoning model, a long conversation, general caution, or a second reviewer does not trigger a full suite. After a relevant repair, rerun the failed and invalidated affected checks, not the entire ladder.

## Security Review Triggers

Run a dedicated security check only when the change affects an actual trust boundary: authentication or authorization, secrets, untrusted input, data exposure or deletion, privilege, network egress, supply-chain dependency, deployment, payment, or another explicitly named security control.

Do not trigger a security scan merely because task text, documentation, tests, or governance rules mention `security`, `permission`, `sandbox`, or `approval`. Runtime sandbox and permission controls remain active without a prose-driven security review.

## Bug-Discriminating Evidence

For a bug fix, prefer evidence that distinguishes the defect from unchanged behavior:

- a focused test or reproduction should fail on the buggy baseline when feasible and pass on the candidate;
- when baseline replay is unsafe or impractical, explain why the chosen evidence still observes the reported failure;
- an existing suite that passed before the fix is regression evidence, not proof that the bug was repaired;
- do not compensate for weak evidence by running more unrelated passing tests.

For features, prove the new acceptance behavior. For refactors, prove preserved public behavior plus the specific structural invariant. Evidence quality matters more than command count.

## Artifact Check Selection

| Artifact | Selective Checks |
|---|---|
| Rule file | `measure_rules.py`, version/date, changed coverage anchors, diff |
| Skill | `quick_validate.py`, changed route/script tests, template-residue check |
| Code | focused behavior test, then affected type/lint/build only when relevant |
| Frontend | affected build and rendered browser or screenshot when layout changed |
| API | changed request/response contract and compatibility evidence |
| Database | migration/schema proof plus rollback or data-integrity check |
| Docs | links/paths, duplication, version references, rendering when visual |
| PDF, image, slides | actual render or visual inspection |

Avoid overlapping commands. If one build already performs the relevant typecheck or generation, do not rerun that check separately unless the project documents a distinct purpose.

## Rule-Skill Commands

Choose only commands activated by the changed surface:

```powershell
python <skill-creator-dir>/scripts/quick_validate.py <skill-dir>
python <skill-dir>/scripts/measure_rules.py <codex-home>/AGENTS.md <project-root>
python <skill-dir>/scripts/guardrail_check.py --project <project-root> --json
python <skill-dir>/scripts/snapshot_state.py --project <private-project-root> --write
```

Use `--strict`, the full unit suite, all routing checks, snapshot refresh, secret scans, or release metadata checks only when their corresponding global-sync, shared-infrastructure, private-state, or release surface changed.

## Evidence Interpretation

- A zero exit code is useful only when the command covers the changed behavior.
- Reuse a passing result until a relevant invalidator from `acceptance-closure.md` occurs.
- Classify failures before acting: task-caused, pre-existing, transient, external block, or unknown.
- If validation cannot run, state the reason, uncovered surface, strongest available substitute, and residual risk.

## Compact Reporting

For L0/L1, state the conclusion, evidence, and material risk in one or two short paragraphs. For L2+, add only the affected documentation/version and traceability decisions.

For rule work, report:

- changed rule destination and version action;
- selected checks and what each proved;
- round/phase/release decision;
- synchronized-copy status and residual risk;
- subagent role/model and closure status only when a child was actually used.

Do not paste every command, checklist question, passing retry, or raw log. Use these risk labels when useful: `No known residual risk`, `Low residual risk`, `Moderate residual risk`, or `High residual risk`.
