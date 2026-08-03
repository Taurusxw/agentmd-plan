# v27.12.0 Acceptance

## Status

completed

## Release Contract

- `VERSION`, Git tag, GitHub Release, release directory, global artifact, live global file, and Downloads copy use `27.12.0`.
- The global artifact, live global file, and Downloads copy are byte-identical with SHA-256 `4D9BDD34E635D5321F9BFB8A21321041F175C8404B026A5142A7A64E97759266`.
- The public and live `seer-codex-rules` trees are identical, and coverage metadata is anchored to the same global version and hash.
- Chinese and English manuals describe the same release, installation, routing, and privacy model.
- Private manifests and recovery snapshots remain ignored and are not part of the public release.

## Verification Completed

- Skill creator validation, reference routing, Python compilation, and all seven unit tests passed.
- Portable Agent routing validation passed for Terra/high exploration, Terra/max implementation, and Sol/high review.
- Strict live and release-artifact guardrails passed without warnings or mismatches.
- Rule measurement, version consistency, synchronized hashes, public-path privacy scanning, Markdown path review, and Git whitespace checks passed.
- Local release commit, remote `main`, tag `v27.12.0`, GitHub Release, and remote `VERSION` were verified after publication.

## Publication Path

The GitHub connector installation token permits reads but returns `403 Resource not accessible by integration` for PR writes. The already authenticated GitHub CLI account has explicit `repo` and `workflow` scopes and was used for the user-authorized merge, tag, and Release publication.

## Residual Risk

No known release blocker remains. The connector write limitation is isolated from repository publication; future connector-native mutations require OpenAI to expose a GitHub App installation with the corresponding write permissions.
