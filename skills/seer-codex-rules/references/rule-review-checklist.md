# Rule Review Checklist

Use this checklist before finalizing audits or edits to Codex rule systems.

## Context

- Read the effective rule chain for the target path.
- Read user-mentioned files and the current project rules.
- Identify whether the task is L0, L1, L2, L3, or L4.
- Determine whether the user asked for analysis only or actual edits.

## Scope Fit

- Is each rule in the narrowest correct home?
- Is global `AGENTS.md` limited to universal behavior?
- Are project facts kept in project `AGENTS.md` or project docs?
- Are long branching workflows extracted into Skills?
- Are hard safety controls backed by tools, tests, permissions, hooks, or CI?

## Bloat And Duplication

- Count lines and bytes for edited rule files.
- Search for repeated facts across three or more locations.
- Check whether a new document name duplicates an existing document's responsibility.
- Check whether `docs/DOC_INDEX.md` is becoming harder to maintain than the content.
- Check whether a future Codex would need to read large unrelated sections for a common answer.

## Versioning

- If a versioned rule file changed, classify the highest-impact edit.
- Use `PATCH` only for editorial changes with no behavior change.
- Use `MINOR` for new or materially improved rules.
- Use `MAJOR` for changes to the global operating model or compatibility boundary.
- Do not bump a version for unchanged files, backups, or discussion.
- Update the date when the versioned file content changes.

## Progress Records

- L0: no progress file.
- L1: no round unless the project explicitly requires it.
- L2: update or create a round only when the project already uses `docs/progress/rounds/`.
- L3: record decisions, impact, validation, and risk.
- L4: use phase or release structure.
- Same objective should update the existing round instead of creating noise.
- Same theme across 5-8 rounds should become a phase.

## Validation

- For Skills, run `quick_validate.py` and inspect `agents/openai.yaml`.
- For rule files, run `scripts/measure_rules.py`.
- Inspect diffs for unintended unrelated edits.
- If syncing duplicate copies, compare hashes.
- If deleting, moving, or archiving, verify references and obtain user approval where needed.

## Final Response

Include:

- changed files and destination rationale;
- version bump decision and reason;
- validation commands and results;
- documentation or progress record decision;
- residual risks or items intentionally left for later.
