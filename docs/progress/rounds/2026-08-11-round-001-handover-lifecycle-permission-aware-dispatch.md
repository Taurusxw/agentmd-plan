# 2026-08-11 Round 001: Handover Lifecycle And Permission-Aware Dispatch

## Status

completed

## Goal

Close two post-release governance gaps without replaying the completed `v29.0.0` release or 31-child stress evidence: keep a consumed project handover frozen until a new explicit transfer request, and make every subagent dispatch account for the parent's live permission mode instead of treating role TOML as runtime proof.

## Frozen Completion Contract

- Verify that `seer-project-handover` separates explicit generation from one-time receiving, and that its route, template, validator, and focused test do not imply continuous HANDOFF maintenance.
- Require each multi-agent packet to state required effective access and confirm the parent permission mode immediately before the spawn; the snapshot expires after that spawn.
- Reject write packets assigned to read-only roles, keep legal read-only and worker dispatches valid, and make static router output state `runtime_permissions_verified=false` and `dispatch_ready=false`.
- Preserve the existing Terra/Sol roles, V2 32-slot configuration, adaptive fan-out, completed stress evidence, and publication state.
- Do not edit `docs/HANDOFF.md`, commit, push, tag, publish a Release, or rerun the 31-child stress test.

## Preflight And Diagnosis

- Startup preflight found `main@b0f3edda150a`, a clean tree, `VERSION=29.0.0`, one HANDOFF candidate, and no collector warning. The published `v29.0.0` remains non-draft and non-prerelease.
- Portable and live routing baselines both returned static `ok=true` for V2 capacity and role TOML but exposed no runtime-permission verification field, allowing static success to be mistaken for write readiness.
- The installed `seer-project-handover` already has the intended lifecycle in `SKILL.md`, `handover-schema.md`, `HANDOFF_TEMPLATE.md`, `check_handover.py`, and `test_handover.py`. Its implicit invocation policy still requires a matching explicit transfer intent from the Skill description; receiving mode exits without collector, validator, or HANDOFF writes.
- `seer-project-handover` has one installed copy and no canonical source inside this repository. The current task therefore verified that copy read-only and did not create a duplicate Skill tree.

## Implementation

- Added an Effective Permission Gate to `multi-agent-governance.md`, including Required effective access, Parent permission checked, current-spawn-only validity, role compatibility, one-request fallback, and old-task/new-task guidance.
- Updated the Skill router, portable role instructions, Chinese/English manuals, and guardrail anchors to preserve the gate and distinguish static role defaults from live effective access.
- Added `assess_dispatch()` for deterministic packet/role/parent-snapshot compatibility and changed the router report to identify its static-only scope, `runtime_permissions_verified=false`, `dispatch_ready=false`, and an actionable warning.
- Added focused tests for read-only write misrouting, unchecked parent permissions, legitimate read-only dispatch, legitimate worker dispatch, and static-report non-claims while preserving all capacity/model tests.

## Version And Synchronization Decision

- The highest semantic impact is `MINOR`: this adds a reusable dispatch gate and validation signal without changing the global Agent-first operating model or compatibility semantics.
- The versioned global `AGENTS.md` and formal project `VERSION` remain `29.0.0` because neither global prose nor a new release is part of this task. A future authorized release may carry the accumulated Skill change as the next MINOR.
- Project source and portable role templates are the changed review surface. Live `seer-codex-rules` and Skills Manager copies remain unmodified under the task's project-only write boundary; their pre-change static output was recorded and must not be described as runtime permission proof.

## Tests And Verification

- `test_agent_routing_check.py`: 9/9 passed, covering the four required permission cases, an explicitly checked but insufficient parent mode, and preserved V1/V2 capacity and role templates.
- `test_guardrail_check.py`: 6/6 passed; new Effective Permission Gate, packet fields, and static non-proof anchors are required.
- Project-source router passed with V2 total slots `32`, the existing Terra/Sol role matrix, `static_configuration_ok=true`, `runtime_permissions_verified=false`, and `dispatch_ready=false`.
- `seer-codex-rules` and installed `seer-project-handover` both passed the Skill creator validator; the handover collector/validator focused self-test passed. The first handover validator attempt was environment-blocked by default GBK decoding and passed on the single UTF-8 retry.
- G2 guardrail passed after the required private source snapshot refresh: Skill tree SHA-256 `D836D274C4A15AD24FBC85EFA50C9566C04EEE019DF373881C4D8E9CFA3F252D`, 26 files, no missing routes, anchors, scripts, template residue, or state mismatch. Plain-text router output also prints both `runtime_permissions_verified: false` and `dispatch_ready: false`.
- A final read-only `reviewer_deep` pass found the missing plain-text readiness signal and insufficient-parent branch coverage; both were fixed and their invalidated checks rerun. No material handover-lifecycle defect remained.

## Risks And Follow-Up

- Static validation cannot probe the parent task's live permission profile; the per-spawn check remains an orchestrator responsibility and deliberately expires after one spawn.
- Existing tasks do not hot-reload changed Skill or role files. Until a separately authorized installation/reload, live installed copies retain the prior static checker even though the project source is corrected.
- No evidence attributes old-task permission mismatch to Windows ACLs or claims that editing `config.toml` alone repairs live runtime permissions.

## Next Step

The frozen contract is complete. A later task needs separate authorization only if it will install, commit, publish, or runtime-probe the candidate.
