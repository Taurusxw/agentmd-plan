# v27.7.0 Acceptance

## Status

completed

## Release Contract

- `VERSION`, Git tag, GitHub Release, release directory, and global artifact use `27.7.0`.
- Chinese and English manuals describe the same architecture-drift triggers, thresholds, limits, installation, and validation model.
- The public tree contains no live state, private backup, credential, or machine-specific path.
- The global outline and Skill coverage inventory use version `27.7.0` and SHA256 `40B38F5424B71887F3905AB864FF4DB895E3C540F383777CE8CF79E4B2EF53C7`.

## Required Verification

- Skill structure validation and reference routing.
- Python compilation and `structure_check.py` unit tests.
- Real-project structure scan reproducing the audited hotspot and duplication evidence.
- Strict global-rule size, coverage, and synchronization guardrails.
- Chinese/English version consistency, Markdown link, secret, private-path, risky-file, and Git whitespace scans.
- Local commit, remote branch, tag, and GitHub Release identity checks.

## Residual Risk

Static thresholds expose likely drift but cannot decide semantic module ownership or whether duplicated runtime code is intentionally isolated. The script never performs automatic extraction.
