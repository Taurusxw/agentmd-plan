# Agentmd Plan v30.1.0 Acceptance

## Status

Accepted and released on 2026-08-24.

## Scope

- Publish the accumulated `seer-codex-rules` catalog-discovery and runtime-health improvements as `v30.1.0`.
- Install the complete Skill source into the maintainer environment and prove final byte equivalence.
- Keep only the latest local release record and local Git tag while preserving Git history and GitHub historical releases.

## Exclusions

- No global `AGENTS.md` behavior or artifact change; its version remains `30.0.0`.
- No Nature source, duplicate copy, installation, or validation work.
- No repetition of the historical 31-child stress test.
- No publication to the separate Skills distribution repository.
- `docs/HANDOFF.md` remains frozen.

## Acceptance Evidence

- Skill structure validation passed with the bundled `skill-creator` validator.
- Python compilation and the complete affected unit suite passed: 41 tests, including 16 catalog tests.
- Strict guardrail and project routing checks passed.
- The real Codex runtime catalog passed with 57/57 expected implicit names, 75/75 configured source paths, and 87/87 locally resolvable prompt files present; missing, ambiguous, description-mismatch, and unresolved counts were zero.
- The post-install model-visible Skill section was 21,569 characters and selector detection remained `skill-file`; one renderer-driven `.system` metadata refresh was reconciled, and the new health check added no Codex subprocess.
- Public-release scans found no high-confidence credential signature or machine-specific path in the publishable tree; tracked history had no large-object concern.
- The installed Skill tree was compared once against the final source as the actual synchronization consumer and was byte-equivalent.
- GitHub `main`, annotated tag `v30.1.0`, and the non-draft/non-prerelease GitHub Release were verified after publication.

## Version Decision

`30.0.0 -> 30.1.0` (`MINOR`): this release adds a reusable governance capability and runtime contract without changing the global workflow model or breaking existing Skill usage.

## Cleanup And Rollback

- Local `v30.0.0` release records were replaced by the `v30.1.0` release commit; the old local tag was removed only after publication succeeded. Prior commits, the remote tag, and the GitHub Release remain recoverable.
- The pre-install Skill copy was held only as a temporary local rollback target and removed after byte-equivalent installation verification.
- The ignored pre-29.1.0 private install backup was removed with the authorized old-local-version cleanup. Its exact private folder is no longer locally recoverable; the corresponding public source history remains on GitHub.
- Rollback remains available from GitHub `v30.0.0` or the prior source commit; no history rewrite was performed.

## Residual Risk

- Runtime health observes a freshly rendered prompt. It diagnoses but does not repair an old conversation that already persisted a stale plugin-cache path.
- A plugin whose entire Skill payload is omitted from the prompt requires plugin-registry observability beyond the current prompt-only contract.
- New Skill instructions are expected to appear in new tasks or after an explicit host reload; no in-task hot reload is assumed.
