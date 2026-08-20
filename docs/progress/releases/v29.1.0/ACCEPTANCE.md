# v29.1.0 Acceptance

## Status

validated-awaiting-publication

## Release Contract

- `VERSION`, release directory, global artifact, live global file, and Downloads copy use `29.1.0`; the annotated tag and GitHub Release are created only after the staged release state is committed and pushed.
- The global artifact and synchronized live copies are byte-identical; this is the one final release-integrity comparison, not a proxy for semantic or behavioral validation.
- The current checkout retains only the latest versioned artifact/release documents and, after publication, the latest local tag. GitHub retains prior tags/Releases, and Git history is not rewritten.
- The public and installed `seer-codex-rules` trees contain the same 26-file validated release state.
- The portable template uses the documented `[agents]` child-thread key, while the validator treats schema-only V2 as a warned compatibility override rather than a portable default.
- Chinese and English manuals describe the same zero-hash boundary, permission-aware dispatch contract, model routing, capacity semantics, and latest-only release behavior.
- Private handoff, manifests, backups, and recovery snapshots remain ignored and outside the public release.

## Verification Completed

- Skill creator validation and Python compilation passed against the prepared source Skill.
- The full unit suite passed 27/27, including routing, permission evidence, integrity-evidence anchors, guardrail behavior, and architecture-signal coverage.
- The portable router passed for the documented `[agents]` template and three role files while preserving `runtime_permissions_verified=false` and `dispatch_ready=false` as static non-proof signals.
- Strict rule measurement and one final strict `--require-state` guardrail passed with no warnings across global gate, 26-file Skill, project shape, synchronized copy, and private recovery state.
- One final public-release scan found no candidate secrets, machine-specific paths, risky publishable files, files at least 1 MiB, missing Markdown links, whitespace errors, or HANDOFF changes. The unchanged prior Git-history size evidence was reused rather than rescanning old objects.
- The earlier fresh-task four-child routing smoke remains valid for the installed permission-aware configuration; the completed 31-child stress test is intentionally not repeated.

## Publication Verification

Pending the authorized release commit, `main` push, annotated `v29.1.0` tag, and GitHub Release. A post-publication record will name the release commit, final `main` commit, remote Release state, and local-tag cleanup result without moving the tag.

## Publication Path

The authenticated GitHub CLI account performs the user-authorized branch/main push, annotated tag push, and GitHub Release publication. Cleanup is limited to old local tags and current-tree versioned documents.

## Residual Risk

Static configuration validation cannot prove backend capacity or per-spawn effective permissions. Deleting old versioned files from the checkout saves only modest space because Git and GitHub history intentionally retain them.
