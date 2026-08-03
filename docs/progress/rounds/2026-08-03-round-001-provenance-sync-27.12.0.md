# 2026-08-03 Round 001: Provenance Sync 27.12.0

## Status

completed

## Goal

Repair governance provenance drift between the installed `27.12.0` global rules, the live `seer-codex-rules` Skill, the public artifact, and the ignored private recovery state, then publish the explicitly authorized formal `v27.12.0` release.

## Evidence

- The live global file was `27.12.0` with SHA-256 `4D9BDD34E635D5321F9BFB8A21321041F175C8404B026A5142A7A64E97759266`.
- Public artifacts, README, progress, and private state still referenced `27.9.0`.
- The live and public Skill trees differed only in the global coverage matrix and rule inventory; the live coverage matrix itself still carried a `27.11.0` metadata anchor.
- The strict guardrail therefore reported stale global version/hash, canonical artifact, Skill tree, coverage, README, and progress provenance.

## Key Decisions

- Treat `27.12.0` as the formal release and recovery baseline after the user explicitly authorized the Release.
- Align `VERSION`, release records, tag, GitHub Release, artifact, live global rules, and synchronized copies on `27.12.0`.
- Keep `artifacts/current-state.json` and `seer-codex-rules-current.zip` private and ignored because they contain machine-specific paths and recovery state.
- Sync the public Skill source and live Skill coverage metadata so future snapshots are internally coherent.

## Change List

- Added the byte-identical `artifacts/AGENTS-27.12.0.md` release artifact and its patch rationale.
- Updated the public and live coverage anchors plus the public inventory for `seer-capture` research routing.
- Updated Chinese and English manuals, progress overview, document index, and progress index.
- Refreshed the ignored private state manifest and deterministic Skill snapshot from the live installation.

## Tests And Verification

- Verified exact SHA-256 parity across live global, Downloads copy, and the `27.12.0` release artifact.
- Verified public/live Skill tree parity after excluding caches.
- Ran Skill Python compilation, unit tests, measurement, agent routing, snapshot generation, strict guardrail, path/privacy scans, and `git diff --check`.

## Version And Release

- Global and project release: `27.9.0 -> 27.12.0`, `MINOR` because it adds a long-term research routing rule and synchronizes the governed recovery baseline.
- Formal release artifacts, tag, and GitHub Release use `v27.12.0`.

## Risks And Follow-Up

No known provenance drift remains. The GitHub connector installation token is read-only, so authenticated GitHub CLI credentials perform the authorized publication while the connector remains available for read operations.
