# Code Change Governance Reference

Use this reference when rule work touches coding standards, file movement, module boundaries, or safety constraints for source edits.

## Edit Scope

Make the smallest complete change that satisfies the task.

Allowed:

- editing files directly required by the user goal;
- updating tests and docs that prove or explain the change;
- adding a helper when it removes real duplication or complexity;
- small refactors required to avoid fragile code.

Avoid:

- unrelated cleanup;
- broad formatting churn;
- replacing project patterns with personal preferences;
- adding a framework or dependency without clear benefit;
- moving files merely to make a new structure look tidy.

## Existing Pattern First

Before editing code, identify:

1. module ownership and nearby naming style;
2. existing helpers or services that already solve part of the problem;
3. tests that define behavior;
4. public contracts or generated files;
5. project commands for lint, typecheck, test, and build.

Use `rg` or `rg --files` first for code and file discovery.

## Module Splitting Triggers

Split a file or module when at least one is true:

- it mixes unrelated responsibilities;
- navigation is difficult because unrelated concerns are interleaved;
- tests must mock too much to exercise one behavior;
- repeated logic has started spreading;
- public API and private implementation are tangled;
- a stable small interface can hide a complex implementation.

Do not split when the result is only shallow wrappers, pass-through functions, or extra files with no clearer boundary.

## Cumulative Drift Bridge

The smallest complete change is a per-task rule, not permission to patch the same hotspot forever. Load `architecture-drift.md` when recent rounds or commits repeatedly touch one production module, or when the current patch adds an independent responsibility, broadens a dispatcher/interface, duplicates non-trivial sibling logic, or makes tests depend on unrelated subsystems.

Treat line count as a navigation signal only. Refactor when combined evidence shows a stable boundary with a smaller interface and better locality; do not create shallow wrappers merely to reduce file size.

## Deep Module Standard

Prefer modules with:

- a small, stable external interface;
- meaningful internal implementation depth;
- clear ownership of one domain concept or technical concern;
- low knowledge leakage into callers;
- tests focused on behavior rather than incidental implementation.

Avoid modules that expose many knobs, require callers to know internals, or duplicate the same responsibility under different names.

## User Change Protection

Assume unexpected changes are user-owned unless proven otherwise.

Rules:

- Do not revert unrelated user changes.
- If touched files contain user changes, read and work with them.
- Stage or edit explicit paths only when the worktree is mixed.
- Ask before destructive cleanup, file deletion, history rewriting, or mass movement.
- If user changes make the requested task impossible, explain the conflict and ask for direction.

## File Delete, Rename, And Migration Review

Before deleting, renaming, or migrating files:

1. Search references with `rg`.
2. Check imports, docs, scripts, tests, configs, and CI.
3. Identify generated versus user-authored content.
4. Decide whether compatibility aliases or redirects are needed.
5. Get user confirmation for ambiguous historical or user-authored material.

For documentation migration, prefer an index or summary before archiving.

## Error Handling And Temporary Workarounds

Do not hide errors with broad catches, empty fallbacks, or silent defaults.

Temporary workaround is acceptable only when:

- the user goal is urgent or blocked;
- the workaround is localized;
- the final response names it clearly;
- a follow-up or TODO is recorded in the right place for L2+ work.

Do not write empty comments such as "set variable" or "call function." Add comments only when they explain a non-obvious boundary, algorithm, compatibility issue, or risk.

## Post-Edit Consistency Checks

After edits, check:

- imports and exports;
- renamed paths;
- type signatures;
- tests and fixtures;
- docs that reference changed behavior;
- formatting and generated files;
- package scripts or lockfiles when dependencies changed.
