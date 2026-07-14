# v27.6.0 Acceptance

## Status

completed

## Release Contract

- `VERSION`, Git tag, GitHub Release, release directory, and global artifact use `27.6.0`.
- Chinese and English manuals describe the same installation, governance, validation, privacy, and rollback model.
- The public tree contains no live state, private backup, credential, or machine-specific path.
- The global outline and Skill coverage inventory use the same source version and SHA256.

## Required Verification

- Skill structure validation.
- Python syntax compilation for bundled scripts.
- Strict global-rule size and guardrail checks.
- README language-link and version consistency checks.
- Secret, private-path, risky-file, and Git whitespace scans.
- Local commit, remote branch, tag, and GitHub Release identity checks.

## Residual Risk

Text rules and routing reduce execution drift but cannot replace permissions, sandboxing, tests, CI, or human review for high-risk operations.
