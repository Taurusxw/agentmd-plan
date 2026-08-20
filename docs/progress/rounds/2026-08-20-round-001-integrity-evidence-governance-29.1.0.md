# 2026-08-20 Round 001: Integrity Evidence Governance 29.1.0

## Status

completed

## Goal

Reduce redundant hash, checksum, manifest, and per-page/tree digest work across ordinary Codex tasks without removing the small set of integrity checks that have a real byte-identity consumer.

## Frozen Completion Contract

- Add one concise always-on global rule: ordinary tasks default to no integrity metadata, and hashes cannot replace semantic, source, behavioral, test, or visual evidence.
- Put detailed claim-to-evidence and PDF/page boundaries in `verification-and-reporting.md`, not in the global outline.
- Prevent subagent result packets and hash mismatches from creating checksum manifests or repeated debug loops by default.
- Add deterministic global/reference anchors and one focused regression test so the boundary cannot disappear silently.
- Create and validate a `29.1.0` source candidate, update coverage/state/progress once, and stop after the finite targeted checks pass.
- Do not change `docs/HANDOFF.md`; do not install live copies, use Git/GitHub, publish, or repeat the completed 31-child stress test.

## Authorized Follow-Up Installation

After the source candidate passed its frozen checks, the user separately authorized update and live installation. That follow-up extends scope only to an ignored local rollback backup, the live and Downloads global-rule copies, the installed `seer-codex-rules`, one final private recovery snapshot, and the existing status records. Agent configuration, Git/GitHub, publication, `docs/HANDOFF.md`, and the completed 31-child stress test remain excluded.

## Authorized Formal Release

The user subsequently authorized the Git commit, GitHub update, formal `v29.1.0` Release, and local latest-only cleanup. The release promotes the already validated and installed candidate, keeps remote historical tags/Releases and Git history, and does not replay the completed 31-child stress test.

## Evidence And Decisions

- Multiple independent community reports described GPT-5.6 Sol generating SHA-256 fingerprints, per-document or per-line hashes, and subagent mismatch loops without a task-specific consumer.
- Official OpenAI GPT-5.6 guidance recommends leaner prompts, stating each instruction once, and measuring success against outcome-focused evidence; it also notes that long sessions can amplify repeated prompt content: <https://developers.openai.com/api/docs/guides/latest-model>.
- The existing rule system already owns minimal validation, evidence reuse, and stop gates. The missing invariant is therefore narrow: integrity metadata proves byte identity, not task completion.
- Existing global-rule synchronization and recovery hashes remain legitimate because they have named drift/recovery consumers. They are limited to one final integrated comparison and are not generalized to ordinary artifacts.

## Change List

- Added `artifacts/AGENTS-29.1.0.md` with the default-no-hash and no-proxy-evidence rule.
- Added the detailed integrity metadata boundary to `verification-and-reporting.md` and a compact subagent result rule to `multi-agent-governance.md`.
- Limited snapshot refresh instructions to one run after the final integrated governance state.
- Added guardrail anchors, a focused regression test, and updated global coverage metadata.
- Updated Chinese/English overview and project progress; the formal release remains `29.0.0`, while the live global rule, Downloads copy, and installed Skill now use the private `29.1.0` candidate.

## Tests And Verification

- The owner-context strict preflight passed before edits against the existing `29.0.0` baseline.
- Skill creator `quick_validate.py` passed.
- The full shared validation suite passed once: 27/27 unit tests, including the new integrity-evidence regression test.
- Strict rule measurement passed: global candidate 99 non-empty lines / 13,496 bytes; Skill router 95 / 13,515; verification reference 75 / 7,425; multi-agent reference 129 / 17,843; progress 81 / 11,064.
- Independent Sol/high read-only review confirmed the global semantic delta was limited to version/date plus the new rule. Its two target-related anchor gaps and the live/source wording ambiguity were repaired; the invalidated focused guardrail tests then passed 7/7.
- The initial integrated snapshot was invalidated by that anchor repair, so only the affected snapshot/state evidence was refreshed once more after the repair. Final source state: global SHA-256 `2A84F623607689C1709B6F3F3C6E17154B7CF9326A4369238CB7101F43BECCC5`; 26-file Skill tree `1F1678EC66EC85AAE29D7C5135D6ED840F4D0EA618EDF577EF3908B4F5D09405`.
- Final strict `--require-state` guardrail passed with no warnings, missing phrases, route gaps, template residue, or state mismatch.
- After private installation, strict measurement passed and one final live `--strict --require-state` guardrail confirmed global version `29.1.0`, the 26-file installed Skill, the Downloads copy, project gate, and recovery state with no warnings.
- The follow-up installation created an ignored rollback copy, synchronized the two live global-rule files and installed Skill, and refreshed the private recovery state once. It did not perform Git/GitHub actions, publication, a HANDOFF refresh, Agent-config changes, or the 31-child stress test.

## Risks And Follow-Up

- The rule cannot infer every domain-specific integrity threat model. A future task must still name the byte-identity assertion and consumer when it elects to hash.
- The files are installed, but the current active task is not assumed to hot-reload them. The new behavior becomes effective when a new task or explicit host reload supplies `29.1.0` in its instruction chain.
- The reviewer noted that the existing state checker does not compare the manifest date or independently anchor the coverage-matrix header. Current metadata is consistent, and this pre-existing non-hash gap was intentionally left outside the frozen objective rather than adding another generic check.

## Next Step

The candidate is promoted through `docs/progress/releases/v29.1.0/`; publication evidence and any residual risk belong to that release record.
