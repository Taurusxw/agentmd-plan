# v30.0.0 Acceptance

## Status

accepted and published — candidate validation, maintainer installation, both repository paths, annotated tag, GitHub Release, and publication verification passed.

## Release Contract

- [x] `VERSION`, release directory, candidate artifact, and integrated source use `30.0.0` consistently.
- [x] Chinese and English manuals describe the same governance-sensitive conditional routing (with ordinary matching Skills unaffected), net-benefit delegation, zero-hash boundary, two-target release boundary, and latest-only local policy.
- [x] Candidate validation is recorded from the final integrated source state; the read-only baseline is not substituted for it.
- [x] `seer-codex-rules` and the five approved Seer Skills pass their focused validators from source worktrees before installation.
- [x] The source and separate distribution repositories in the two-repository release path are separately authorized and evidenced; the distribution repository was pushed without a Release and the source repository has a formal Release.
- [x] Git commit, annotated `v30.0.0` tag, GitHub Release, and publication URL are recorded only after those external actions complete.
- [x] Local latest-only source cleanup removes only the obsolete `29.1.0` artifact/release assets; Git/GitHub history remains intact.
- [x] `docs/HANDOFF.md` remains unchanged.
- [x] No `nature-*` source, version, test, installed copy, or `.agents` duplicate-copy change is attributed to this release; the entire Nature scope remains frozen and unvalidated.

## Planned Candidate Validation

| Evidence | Purpose | Status |
|---|---|---|
| Version/reference and Markdown-path review | Candidate document consistency | passed |
| Governance and five-Seer focused validators | Source-level behavior and routing | passed |
| Release-owner selected source checks | Final integrated candidate behavior | passed |
| Separate installation evidence | Maintainer-environment target | passed |
| External release evidence | Tag and GitHub publication | passed |

## Candidate Evaluation

- Governance static evidence: valid Skill; final shared suite 25/25; strict global size 35 non-empty lines / 4,567 bytes; static routing valid with `runtime_permissions_verified=false`; non-live strict guardrail passed without requesting hashes or recovery state.
- Seer source evidence: 5/5 focused validators passed; `seer-mathbook` routing tests passed 4/4.
- Candidate routing evidence: scenarios 1–15 passed in a temporary non-live `CODEX_HOME`; seven governance loads, zero subagent dispatches, zero hash commands, and no live writes.
- Baseline/candidate for scenarios 1–15: total input `2,700,004 -> 2,287,102`; median `169,355 -> 133,725`.
- Ordinary cohort scenarios 1, 2, 3, 6, 11, and 12: total input `695,035 -> 324,423` (53.3% lower); median `153,779.5 -> 60,810` (60.5% lower). Ordinary L1/L2 and consumed-HANDOFF work no longer loaded governance.
- Nature scenarios 16–20 were intentionally not rerun or scored after the scope freeze.
- Recovery compatibility: the legacy persistent-inventory-hash requirement was removed; the affected shared suite passed 25/25, then one final recovery/sync stage created the private state and passed strict live, artifact, Downloads, Skill-tree, and state checks without mismatches.

## Baseline Observation (Not Acceptance)

20/20 routing prompts ran read-only with `gpt-5.6-sol` (total input `4,031,088`; median `168,567`). Nine scenarios loaded `seer-codex-rules`; no actual subagent dispatches or hash commands occurred. Nature scenarios 16–20 are read-only observations only, are not acceptance evidence, and are not presented as fixed.

## Publication Fields

- Distribution repository commit: `38cd851` on `skills-manager-backup/main`; pushed without a Release.
- Release commit: `4b4a2d7a63e4e29be48d31ba9270996d161df964`.
- Annotated tag: `v30.0.0`; remote tag published, local latest-only tag set contains only `v30.0.0`.
- GitHub Release URL/state: <https://github.com/Taurusxw/agentmd-plan/releases/tag/v30.0.0>; public, non-draft, non-prerelease, and latest at verification time.
- Maintainer-environment installation state: 30.0.0 global live/Downloads and installed governance Skill; five approved Seer Skills updated through canonical source links; private rollback backup retained.

## Residual Risk

The active task does not assume that live rule changes hot-reload. `30.0.0` becomes effective for new tasks or after an explicit host reload.
