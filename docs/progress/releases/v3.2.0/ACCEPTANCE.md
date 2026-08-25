# Agentmd Plan v3.2.0 Acceptance

## Status

ready-for-publication

## Frozen Scope

1. The global rule artifact and project metadata use `3.2.0` consistently.
2. The global outline and routed Skill references cover outcome-first delivery, correction invalidation, evidence-based complexity, post-acceptance stopping, and compact reporting.
3. Only the latest versioned artifact, release record, and local tag remain in the checkout; historical Git/GitHub evidence is preserved.
4. Source validation, live installation, one final synchronized-state comparison, Git push, tag, and GitHub Release pass.

## Non-Goals

- Rewriting Git history or deleting historical GitHub tags/Releases.
- Publishing the independent Skills distribution repository.
- Re-running Nature work, historical multi-agent stress tests, or superseded acceptance suites.

## Required Evidence

- Rule measurement and semantic diff.
- Skill structure validation and affected unit tests.
- Strict source guardrail and current version/reference audit.
- Live global, Downloads, installed Skill, private current-state snapshot, and one final comparison.
- Clean source commit, annotated `v3.2.0` tag, pushed `main`, and published GitHub Release.

## Result

Local source and live acceptance passed. The global rule, Downloads copy, installed Skill, and private recovery state are synchronized at `3.2.0`; strict guardrails, the final source/live Skill comparison, and runtime catalog health all pass. Git push, tag, and GitHub Release remain the publication step.

`codex --strict-config doctor --summary` remains nonzero only for the pre-existing `TERM=dumb` terminal condition and stale thread-database rows that reference missing rollouts. Configuration, authentication, network, runtime, and Git checks are healthy, and the independent `codex debug prompt-input probe` passed; these environment residues are not caused by this release.
