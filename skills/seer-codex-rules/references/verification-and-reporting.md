# Verification And Reporting Reference

Use this reference when deciding how to validate a change and how to report results.

## Validation By Task Level

| Level | Minimum Credible Validation |
|---|---|
| L0 | Evidence review, source references, no edit validation needed |
| L1 | Direct syntax/static check or targeted command when available; otherwise manual diff review |
| L2 | Targeted tests for changed behavior, relevant lint/type/build check when practical, diff review |
| L3 | Broader test suite or integration checks, migration/API/security checks when applicable, documentation review |
| L4 | Full release/phase acceptance, regression checks, artifact review, rollback or risk notes |

If validation cannot run, say why and list the command or manual check that should be run later.

## Validation By Artifact Type

| Artifact | Credible Checks |
|---|---|
| Rule file | `measure_rules.py`, version/date review, diff review, coverage checklist |
| Skill | `quick_validate.py`, template-residue search, reference routing review, script smoke test |
| Code | targeted tests, typecheck, lint, build, import/reference search |
| Frontend | build plus rendered browser or screenshot check when layout matters |
| API | request/response contract tests, schema docs, compatibility notes |
| Database | migration dry run or schema diff, rollback consideration, data model docs |
| Docs | link/path check, duplicate document scan, line threshold review |
| PDF, image, slides, or document layout | actual render or visual inspection |

Do not treat "command exited zero" as the only evidence. State what the command actually covered.

## Rule-Skill Validation Commands

Typical commands for this skill:

```powershell
python <skill-creator-dir>/scripts/quick_validate.py <skill-dir>
python <skill-dir>/scripts/measure_rules.py <codex-home>/AGENTS.md <project-root>
python <skill-dir>/scripts/guardrail_check.py --project <project-root> --json
python <skill-dir>/scripts/snapshot_state.py --project <private-project-root> --write
```

Use path quoting as needed in the active shell.

`guardrail_check.py` performs the template-residue check without treating ordinary prose such as "TODO" as a failure. Use `--strict` for global sync or release after known warnings have been resolved.

## Output Shape

For L0/L1, keep the response short:

```markdown
## Conclusion Or Summary

## Verification

## Risks And Next Step
```

For L2+:

```markdown
## Change Summary

## Code Or Rule Changes

## Documentation Updates

## Tests And Verification

## Traceability Check

## Risks And Follow-Up
```

Do not force headings when a one-paragraph answer is clearer, but never omit important validation or risk facts.

For an active persistent Goal, use the compact status from `goal-mode-closure.md`. Once all Frozen Criteria pass, report `complete`; optional findings remain follow-ups and do not justify another validation loop.

## Traceability Check

For rule and documentation work, explicitly answer:

- Was a round or phase required?
- Was progress overview updated?
- Was changelog updated?
- Was doc index updated?
- Were any duplicate or forbidden document names introduced?
- Were any rules moved between global, project, docs, Skill, or enforcement tools?
- Did any versioned file require a bump?
- What validation ran?
- What risk remains?

## Version Reporting

Always report:

- old version and new version when a versioned file changed;
- no version bump when no versioned file changed;
- bump class and rationale;
- date update if applicable.

For this skill, updates to `seer-codex-rules` do not require global `AGENTS.md` version changes unless global `AGENTS.md` itself is edited.

## Honesty Requirements

Say plainly when:

- a command failed;
- a command was not run;
- a check was only partial;
- a source was not official;
- a rule is an assumption;
- a migration was deferred;
- a deletion or risky operation still needs user confirmation.

## Final Risk Vocabulary

Use clear labels:

- `No known residual risk`: validation covers the changed surface.
- `Low residual risk`: change is local, validation is targeted, no broad behavior change.
- `Moderate residual risk`: validation was partial or change affects shared behavior.
- `High residual risk`: important checks could not run, data/security/deployment is involved, or rollback is unclear.
