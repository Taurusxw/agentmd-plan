# v27.13.0 Acceptance

## Status

completed

## Release Contract

- `VERSION`, Git tag, GitHub Release, release directory, global artifact, live global file, and Downloads copy use `27.13.0`.
- The global artifact, live global file, and Downloads copy are byte-identical with SHA-256 `F5E8D50863462A6EE0B7F733177E0F1971F86D873108656DD0B9EAFA532014B7`.
- The public, Codex, and Skills Manager `seer-codex-rules` trees are identical with 25 managed files.
- Chinese and English manuals describe the same release, installation, authorization, validation, and model-routing behavior.
- Private manifests and recovery snapshots remain ignored and are not part of the public release.

## Verification Completed

- Skill creator validation, Python compilation, all eight unit tests, and portable Agent routing validation passed.
- Strict live and release-artifact guardrails passed without warnings or mismatches.
- Rule measurement, version consistency, synchronized hashes, Markdown links, public-path privacy, secret, risky-file, large-history-object, and Git whitespace checks passed.
- Local release commit, remote `main`, tag `v27.13.0`, GitHub Release, remote `VERSION`, license, visibility, and default branch were verified after publication.

## Publication Path

The authenticated GitHub CLI account with `repo` and `workflow` scopes performs the user-authorized commit push, tag push, and GitHub Release publication.

## Residual Risk

No known release blocker remains. Text rules reduce repeated model behavior but cannot replace runtime sandbox, approval, hook, CI, or human controls for genuinely high-risk actions.
