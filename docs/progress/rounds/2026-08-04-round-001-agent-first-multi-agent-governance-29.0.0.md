# 2026-08-04 Round 001: Agent-First Multi-Agent Governance 29.0.0

## Objective

Replace the fixed single-agent-default and 1/2/3 concurrency model with a supported, non-Ultra, agent-first governance system that scales useful collaboration without confusing configured capacity with required utilization. Balance quantity, elapsed time, quality, and tokens through adaptive waves, multi-model roles, fresh contexts, exclusive write ownership, and measurable stop rules.

## Scope And Completion Contract

- Establish current primary-source and local-runtime evidence for proactive authorization, V1/V2 capacity semantics, model/fork routing, and hard-versus-soft limits.
- Make global and Skill rules explicitly require root-led delegation whenever an independent packet passes the benefit gate.
- Remove prose count ceilings; scale each wave to ready packets, effective slots, and the fixed task/time/token budget.
- Provide a current V2 template, backend-aware validator, role capability classes, tests, synchronized installations, and a fresh-session probe.
- Preserve all existing dirty/untracked work and the `28.2.0` freshness candidate; do not commit, push, tag, or publish a GitHub Release.

## Diagnosis

- The screenshot was not evidence that Codex lacked collaboration capability. The active runtime injected `ExplicitRequestOnly`, and the assistant treated it as an absolute ban even though an applicable Skill already requested delegation; later child creation succeeded in the same environment.
- Ultra is the current built-in proactive mode, but it is not the only supported path to child creation. An applicable user, `AGENTS.md`, or Skill instruction can explicitly request delegation at lower reasoning efforts.
- Deprecated `multiAgentMode` is ignored. A hidden prompt-hint field exists in source but is not a stable public contract and is not used here.
- Current Codex distinguishes V1 child-thread capacity from V2 total-session capacity. Model metadata can select V2 even when a feature list appears disabled, so a new-task effective prompt is the decisive local check.
- Parser acceptance and a model-visible slot count are not proof that an account or backend will execute the same number successfully.

## Primary Research Evidence

- OpenAI app-server protocol states that deprecated `multiAgentMode` is ignored and Ultra selects proactive behavior: <https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md>.
- OpenAI configuration schema defines `[agents].max_concurrent_threads_per_session`, marks V1 nesting depth ignored by V2, and exposes a positive-integer V2 total-capacity field without a published maximum: <https://github.com/openai/codex/blob/main/codex-rs/core/config.schema.json>.
- OpenAI Codex source resolves V2 capacity and backend selection, including conversion from legacy child capacity: <https://github.com/openai/codex/blob/main/codex-rs/core/src/config/mod.rs>.
- OpenAI subagent guidance documents custom agents, role/model routing, and explicit delegation: <https://learn.chatgpt.com/docs/agent-configuration/subagents.md>.
- Anthropic’s production research system uses an orchestrator-worker pattern, scales simple through 10+ subagents by query shape, and reports both major latency gains and roughly 15× chat token use for multi-agent systems: <https://www.anthropic.com/engineering/multi-agent-research-system>.
- Google ADK demonstrates a parallel discovery stage followed by a sequential synthesis stage, supporting wave/barrier topology: <https://adk.dev/agents/workflow-agents/parallel-agents/>.

## Decision

1. Publish a `29.0.0` candidate because replacing the global operating model and compatibility semantics is `MAJOR`; keep project `VERSION` and public release state at `28.1.0` until separately authorized.
2. Treat applicable global/Skill instructions as explicit non-Ultra delegation authorization. Do not use deprecated fields, hidden prompt text, unsupported binary patches, or claims of bypassing platform hard limits.
3. Use an adaptive root orchestrator. Wave size is `min(ready independent packets, effective free runtime slots, task/time/token budget)` with no fixed governance count ceiling.
4. Keep root scope/integration ownership, one concurrent writer per file area, compact results, synthesis barriers, and final targeted evaluation.
5. Prefer Terra/medium exploration and fallback, Terra/high bounded implementation, and Sol/high named material-risk review; escalate or reduce effort by uncertainty and rework cost rather than a universal floor.
6. Use `fork_turns="none"` for heterogeneous routing. Permit nested delegation only through an explicitly authorized recursive packet that repeats all gates.
7. Set the portable/current live V2 template to 32 total slots including the root. This is generous headroom, not a target or platform guarantee.

## Implemented Surfaces

- New `artifacts/AGENTS-29.0.0.md` and MAJOR rationale while preserving `AGENTS-28.2.0.md`.
- `seer-codex-rules` router plus multi-agent, task-scaling, low-token, coverage, and inventory references.
- Backend-aware `agent_routing_check.py`, guardrail anchors, and unit tests.
- V2 portable/live configuration and three role templates.
- Chinese/English README, progress overview, document index, current handoff, Skill snapshot, and installed copies.

## Validation

- Skill creator validation passed, and all five Python scripts compiled.
- The full shared validator suite passed `11/11`, including V1 `N+1`, V2 `N`, capacity 128 acceptance, conflicting-key rejection, adaptive authorization anchors, and existing structure checks.
- Strict measurement passed at 129 lines, 98 non-empty lines, and 13,116 bytes.
- Portable and live router checks passed with V2 total slots `32`, child slots `31`, Terra/medium explorer/default, Terra/high worker, and Sol/high reviewer.
- `codex --strict-config doctor --summary` loaded the configuration with zero failures; unrelated existing rollout/thread warnings remain outside this objective.
- A fresh `codex debug prompt-input probe` emitted “32 available concurrency slots … including you.” An explicit non-Ultra `explorer_fast` probe spawned and completed; the child could confirm successful delegation but could not introspect its exact resolved model/effort.
- A later fresh, ephemeral Sol/high CLI session loaded live `29.0.0`, attempted all 31 child slots before waiting, accepted 31/31 spawns with no collaboration-limit error, directly observed 22 children running while 9 had already completed, and finished 31/31. A separate Desktop task screenshot showed five simultaneously active children, independently proving the former three-child ceiling was not a Sol/high limit.
- Saturating the pool also produced model-metadata `429` responses, image-preparation failures, child-shutdown timeouts, and conflicting raw mathematical readings that required root adjudication. The result validates capacity and explicit non-Ultra delegation, not 31-way utilization as an efficiency or quality target.
- Strict guardrail passed with no warnings. Global artifact/live/Downloads SHA256 is `E82A3B28999BC93B6F702A06E2C345C062B908FFC85D50CAF70EF3167DEC1638`; project, Codex, and Skills Manager trees share `95425F4E39BDE7C60D3985C0949FA37E5F66F1D709E005A31A2E3FBA3DC6D8C2` across 26 files.

## Risks And Rollback

- Existing tasks do not hot-reload the new global rule, role files, or 32-slot capacity. The original Desktop task remained at root plus three children, while fresh tasks loaded the new capacity; use a new task or explicit host reload after configuration changes.
- High fan-out can increase token use and coordination failure. The benefit gate, cheap capability routing, fresh contexts, wave barriers, exclusive writes, and diminishing-return stop rule reduce but cannot eliminate that risk.
- Model identifiers, efforts, feature fields, and account capacity may change; runtime facts override portable templates.
- Roll back from Git commit history or an operator-owned local backup without resetting or discarding unrelated dirty work.

## Publication Continuation

- The original no-publication boundary remained effective through implementation and runtime validation. The user later explicitly authorized the `v29.0.0` commit, push, tag, GitHub Release, and latest-only cleanup.
- The current checkout retains only the latest versioned artifact/release documents and local tag; GitHub keeps prior tags/Releases, and commit history remains intact for auditability.
