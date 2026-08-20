# 2026-08-16 Round 001: Current Codex Subagent Governance

## Status

completed

## Goal

Update the post-release governance candidate from current primary-source evidence without replaying the completed `v29.0.0` release, 31-child stress run, or unchanged acceptance checks. Keep the published global `AGENTS.md` concise while improving the linked `seer-codex-rules`, portable agent configuration, and focused routing evidence.

## Frozen Completion Contract

- Use current official OpenAI Codex Subagents, configuration, and Skills documentation as the product contract; keep Responses API multi-agent Beta out of local Codex routing rules.
- Replace the schema-only V2 capacity override in the portable template with the documented `[agents]` child-thread key while preserving 31 spawned children and the usual 32 total threads including the root.
- Keep `features.multi_agent_v2` recognizable as an official-schema-supported but human-readable-table-omitted backend override; warn on it and never claim parser success proves backend capacity.
- Make each dispatch packet record required capability scope, the parent access actually observed and its observation source, and the compatibility decision rather than an unauditable Boolean alone.
- Add a task-scoped wave budget, marginal-evidence stop gate, root-accepted outcome accounting, first-pass acceptance, and rework/rejection reasons without creating a universal agent ceiling or heavy dashboard.
- Keep `docs/HANDOFF.md` frozen. Do not install live copies, commit, push, tag, publish, or rerun the prior stress test.

## Authorized Follow-Up Installation

After the source candidate was completed, the user separately authorized live installation and fresh-task validation. That follow-up extended scope only to a private rollback backup, live Skill/role/config synchronization, and a four-child read-only smoke test. Git/GitHub, version publication, HANDOFF changes, and the prior 31-child stress test remained excluded.

## Primary Evidence And Decisions

- Current Codex releases enable subagents and may delegate when direct user, applicable `AGENTS.md`, or Skill instructions request it; parallel read-heavy work is favored and write-heavy coordination requires caution: <https://developers.openai.com/codex/subagents/>.
- The human-readable config reference defines `agents.max_concurrent_threads_per_session` as spawned threads excluding the primary and lists `agents.max_threads` as a legacy alias, while the official JSON Schema separately includes `features.multi_agent_v2` and says an enabled value takes precedence: <https://developers.openai.com/codex/config-reference/> and <https://developers.openai.com/codex/config-schema.json>.
- Subagents inherit the parent turn's live sandbox and approval overrides, so static role TOML remains capability metadata rather than runtime proof: <https://developers.openai.com/codex/subagents/>.
- Skills use progressive disclosure and the initial Skill list has a bounded context budget, supporting a shorter trigger description and detailed one-level references: <https://developers.openai.com/codex/skills/>.
- Anthropic's production multi-agent report and Google ADK patterns support independent packets, explicit work bounds, synthesis barriers, and hard stop conditions while warning that coordination can consume substantially more tokens: <https://www.anthropic.com/engineering/multi-agent-research-system> and <https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/>.
- OpenAI, Google, and Microsoft agent-evaluation guidance supports outcome-first acceptance, sampled trace review, explicit rework taxonomy, and measured usage rather than self-reported completion or universal leaderboard targets.

## Implementation

- Migrated `config/agents.toml.example` to the documented `[agents]` capacity key with 31 spawned threads.
- Kept compatibility parsing for the schema-supported V2 backend override, marked its capacity semantics as local evidence rather than a portable contract, and emitted a warning.
- Strengthened the role-instruction anchor and packet contract with required capability scope, current parent access, its observation source, and a compatible dispatch decision.
- Added Wave Budget And Stop Gate guidance, root-accepted result semantics, first-pass/rework metrics, and a portability boundary around `fork_turns`.
- Shortened the Skill trigger description without removing its major trigger classes and updated Chinese/English manuals.
- Expanded focused router tests for network/approval access, empty and unknown access, unknown roles, documented defaults and alias handling, V2 Boolean/precedence/minimum handling, exact role anchors, migration warnings, and plain-text runtime non-claims.

## Tests And Verification

- `py_compile` passed for the router and guardrail scripts.
- All 18 focused routing tests and all 6 guardrail tests passed.
- The portable static router passed with 31 child slots and normally 32 total slots; it explicitly reported `runtime_permissions_verified=false` and `dispatch_ready=false`.
- The final Skill snapshot contains 26 files with tree SHA-256 `071DB11672910F5F2700C8651AAECB5AF97A741BB8FB558A52D7E29C7A53245B`; the source guardrail passed global gate, Skill routes/anchors, project shape, synchronized hashes, and current state.
- Strict measurement passed with no warnings: global artifact 98 non-empty lines / 13,116 bytes, Skill router 95 / 13,366, multi-agent reference 128 / 17,355, and `PROGRESS.md` 76 / 9,905.
- The earlier `quick_validate.py` dependency block is closed: the active default Python exposes PyYAML 6.0.2, and the upstream validator passed against both source and live Skill paths.
- A final independent read-only review found the initial V2-schema, documented-default/alias, and dispatch-evidence gaps closed. Its one interim minimum-capacity finding was repaired to match the schema minimum of 1 and covered by the focused test before final validation.
- Live static routing passed with `[agents]` 31 child slots / normally 32 total, all three role files valid, `runtime_permissions_verified=false`, and `dispatch_ready=false`. Live strict guardrail passed with the same 26-file Skill tree hash as source.
- A new task loaded the installed rules, reported 32 total runtime slots, and accepted exactly four concurrent `explorer_fast` read-only children; all completed first pass as Terra/medium without permission prompts. This is a smoke test, not proof that all 31 child slots can execute reliably.

## Version And Synchronization

- The published global `AGENTS.md`, artifact, `VERSION`, tag, and Release remain `29.0.0`; the live global file was unchanged and retains the published hash. The post-release Skill, three role files, and `[agents]` capacity were installed privately after separate authorization and are not claimed as part of the published tag.
- The always-on global outline already requires the multi-agent governance reference, so duplicating these detailed mechanics there would increase prompt cost without closing a coverage gap. This task therefore makes no global version bump.
- A later separately authorized release must decide the next project/Skill version and repeat only the release-specific checks invalidated by that publication state.

## Risks And Follow-Up

- V2 is present in the official JSON Schema but absent from the human-readable key table, whose documented child-thread semantics apply only to `[agents]`; compatibility recognition therefore does not promise identical backend behavior across clients.
- Static validation still cannot prove live sandbox, app/MCP permissions, network controls, account limits, or backend concurrency.
- Capability scope is recorded for audit and routing; actual enforcement remains with runtime sandbox, permission, app/MCP, approval, hook, or CI controls.

## Next Step

Stop at the validated and privately installed candidate. Any version decision, commit, push, tag, or publication remains separately authorized work.
