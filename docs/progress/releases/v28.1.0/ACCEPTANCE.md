# v28.1.0 Acceptance

## Status

completed

## Release Contract

- `VERSION`, Git tag, GitHub Release, release directory, global artifact, live global file, and Downloads copy use `28.1.0`.
- The global artifact, live global file, and Downloads copy are byte-identical with SHA-256 `54633C3A5D2C9E38174BFAA45246B8B1460DF18F585B4BC9253E06ECA0B0D273`.
- The public, Codex, and Skills Manager `seer-codex-rules` trees are identical with 26 managed files.
- The Git update contains no `28.0.0` artifact, commit, tag, or GitHub Release.
- Chinese and English manuals describe the same explicit persistence and centralized ownership behavior.
- Private manifests and recovery snapshots remain ignored and are not part of the public release.

## Verification Completed

- Skill creator validation, Python compilation, all nine unit tests, and portable Agent routing validation passed.
- Strict live and release-artifact guardrails passed without warnings or mismatches.
- Rule measurement, synchronized hashes, Markdown links, privacy, credential, risky-file, large-history-object, and Git whitespace checks passed.
- Local release commit, remote `main`, tag `v28.1.0`, GitHub Release, remote `VERSION`, license, visibility, and default branch were verified after publication.

## Publication Path

The authenticated GitHub CLI account with `repo` and `workflow` scopes performs the user-authorized commit push, tag push, and GitHub Release publication.

## Residual Risk

No known release blocker remains. The owner gate constrains compliant Agents and is deterministically checked, but operating-system permissions cannot distinguish conversations running under the same user account.
