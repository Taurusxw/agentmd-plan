# Multi-Agent Governance

Use this reference before spawning, routing, or coordinating subagents. The goal is to shorten the critical path, isolate noisy context, or add specialist assurance while keeping work ownership, integration, and token cost explicit.

The operating model is an adaptive root orchestrator. The root owns scope and the final answer; children receive independently verifiable work packets and return compressed evidence. Agent capacity enables useful parallelism, but it is never a utilization target.

## Agent-First Decision

Before a material execution step, identify ready work packets across discovery, implementation, validation, and specialist review. Do not assume that L0-L2 must be solo or that L3-L4 must use agents; actual dependency structure decides.

Task size, difficulty, or the word “thorough” is not enough by itself. Conversely, do not keep a qualifying independent packet in the root merely because one agent could eventually finish everything.

## Explicit Delegation Authorization

The global `AGENTS.md` and this reference explicitly request proactive root-led delegation whenever the Delegation Benefit Gate passes. This is the applicable-rule authorization for runtimes that otherwise advertise `ExplicitRequestOnly`; the user does not need to repeat the request, and Ultra reasoning is not required.

A matching Skill that requires subagents, parallel review, or isolated implementation is a binding routing signal unless a higher-priority instruction, unavailable runtime capability, or a failed benefit gate prevents it. If a mandated delegation is skipped, state the concrete reason.

Do not rely on deprecated `multiAgentMode`, hidden prompt-hint overrides, or unsupported patches to force proactive behavior. Runtime permissions, model availability, account limits, and session capacity remain authoritative.

## Delegation Benefit Gate

Delegate when all mandatory conditions pass:

1. The packet is concrete, bounded, and independently verifiable.
2. It can run without serial access to the root’s immediate next step, or it materially isolates noisy context or supplies a named specialist review.
3. Its read/write ownership is disjoint from concurrent work, or it is read-only.
4. It can return a compact conclusion, patch, or evidence bundle instead of transferring raw working context.
5. At least one material benefit exists: shorter critical-path time, better context isolation, cheaper capability routing, or stronger assurance on a named risk.

When the gate passes, spawn the smallest capable role promptly. Do not duplicate the same question across agents unless independent evaluation of a material correctness, architecture, security, data, compatibility, or release risk justifies it.

## Critical Path Ownership

The root must retain:

- requirement interpretation, scope decisions, and the completion contract;
- the dependency graph, wave boundaries, and write-set assignment;
- the immediate blocking design decision and cross-module integration;
- conflict resolution, final edits across child boundaries, and rejection of scope drift;
- final validation, completion judgment, and user reporting.

The root continues useful non-overlapping work while a wave runs. Waiting is appropriate at a declared synthesis or integration barrier, not as the default behavior after every spawn.

## Adaptive Fan-Out And Waves

For each wave, compute the useful fan-out as:

```text
min(ready independent packets, effective free runtime slots, task/time/token budget)
```

There is no fixed governance ceiling of one, two, or three children. Runtime capacity is a hard boundary; it is not a target and does not justify inventing work. Large waves are appropriate only when many cheap, independently checkable packets are already ready, such as breadth-first research, test sharding, or disjoint repository mapping.

Prefer this pipeline when multiple stages exist:

1. **Discovery wave:** read-only explorers map independent domains, sources, logs, or failure surfaces.
2. **Synthesis barrier:** the root deduplicates evidence and freezes decisions and write ownership.
3. **Implementation wave:** one writer owns each disjoint file or module area; no overlapping generated artifacts.
4. **Evaluation wave:** targeted validators or a material-risk reviewer inspect the integrated state.

Stop expanding a wave when packets overlap, evidence becomes repetitive, the root’s critical path is ready, coordination cost exceeds remaining work, or the fixed task/token budget is under pressure. Interrupt obsolete work and Close Completed Agents promptly so stale threads do not occupy capacity.

## Runtime Capacity And Backend Semantics

Capacity keys have backend-specific meanings in current Codex builds:

- V1/public compatibility: `[agents].max_concurrent_threads_per_session = N` counts spawned child threads, so the visible total is normally `N + 1` including the root.
- V2: `[features.multi_agent_v2].max_concurrent_threads_per_session = N` counts total session threads including the root.
- When V2 is explicitly enabled, do not also set the legacy child-capacity key. Model metadata may select V2 even when the feature listing looks disabled, so verify the effective new-session prompt rather than inferring the backend from one flag.

The schema publishes a positive-integer minimum but no durable public maximum. A large value being accepted by the parser or appearing in generated instructions does not prove that the account, backend, or host will execute that many children successfully.

After a capacity or backend change, use a fresh task or explicit host reload and check the effective total with current diagnostics, for example:

```powershell
codex --strict-config doctor --summary
codex debug prompt-input probe
```

Treat unsupported keys, effective capacity, permissions, and service limits as runtime facts. Never describe a prose rule or high configured value as a bypass of a platform hard limit.

## Model Routing Matrix

Use capability tiers instead of cloning the root model for every packet. Verify current model and effort availability; when a listed identifier is unavailable, choose the closest fast, balanced, or deep model exposed by the runtime.

| Role | Preferred Configuration | Escalate When | Default Access |
|---|---|---|---|
| `explorer_fast` | `gpt-5.6-terra`, medium | Use low for deterministic lookup; high only for ambiguous cross-source analysis | read-only |
| `worker_balanced` | `gpt-5.6-terra`, high | Use medium for mechanical edits; max only for a genuinely complex bounded implementation | inherit parent permissions |
| `reviewer_deep` | `gpt-5.6-sol`, high | Use a stronger offered tier only for a named material risk that high cannot resolve | read-only |

Use Terra/medium as the unclassified fallback. Do not select Ultra merely to unlock delegation: applicable rules already provide explicit authorization. Do not lower capability only for nominal savings when likely rework would erase them; route by packet uncertainty, impact, and verification cost.

Model resolution normally follows a role file, an explicit spawn override, `[agents]` defaults, then parent settings. Runtime behavior can change, so validate actual task metadata when model identity matters.

## Fresh Context And Fork Semantics

Use `fork_turns="none"` for a named role, a different model, or a different reasoning effort. Send a compact packet:

```text
Role: <explorer_fast | worker_balanced | reviewer_deep>
Objective: <one bounded deliverable>
Scope: <allowed paths, services, or questions>
Do not touch: <excluded paths and responsibilities>
Known facts: <minimum facts the child cannot cheaply rediscover>
Validation: <specific command or evidence expected>
Return: <compact result contract>
Delegation: <none | explicitly authorized recursive subtree>
```

Use a small positive `fork_turns` only when a few recent decisions are costly to summarize. Use full-history inheritance only for justified continuity: it can duplicate large histories, and current V2 behavior may force the child to inherit the parent model and effort while rejecting overrides.

Never copy unrelated project history, large logs, images, or every loaded governance reference merely for convenience.

## Result Contract

Require children to return:

- the conclusion or completed change;
- exact files, symbols, commands, or source links that support it;
- validation performed and failures encountered;
- one short residual-risk statement;
- no raw exploratory transcript, repeated prompt, or unfiltered log.

Prefer at most eight concise bullets or an equivalent compact patch summary. The root accepts only evidence relevant to the frozen objective and synthesizes once per wave.

## Write And Integration Safety

- Assign one owner for every write set before an implementation wave.
- Never let agents modify the same file, migration, lockfile, or generated artifact concurrently.
- Use read-only explorers and reviewers whenever a write is unnecessary.
- Recheck the shared working tree before integration because children and the root observe the same filesystem.
- Preserve user-authored and unrelated changes; children must not “clean” a dirty tree.

## Conditional Nested Delegation

Prefer a flat root-orchestrated wave because it gives the root the best visibility and usually costs fewer tokens. Descendant spawning is permitted only when the parent task packet explicitly authorizes a recursive subtree, the child has a genuinely decomposable domain, and the child repeats the same benefit, ownership, capacity, and compact-result gates.

V2 may ignore legacy nesting-depth settings. Therefore role instructions must default to no further delegation while allowing the explicit packet exception; capacity and no-overlap rules apply to the entire tree, not separately to each branch.

## Token And Efficiency Accounting

Multi-agent work often reduces elapsed time or improves coverage while increasing total tokens. Balance all four outcomes—quantity, speed, quality, and token cost—rather than claiming that more agents are intrinsically cheaper.

Use these controls:

- route narrow discovery and mechanical work to the cheapest capable tier;
- use fresh compact contexts and avoid full-history clones;
- shard only ready independent work and synthesize once at a barrier;
- cap child output, reject duplicated searches, and close finished threads;
- reserve deep review and high/max effort for named uncertainty or risk;
- reuse accepted evidence instead of sending multiple agents over the same ground.

When the runtime exposes them, record elapsed time, requested/active slots, successful packets, rework, and input/cached/output tokens per accepted result. Otherwise use transparent proxies such as spawn count, full forks, return length, duplicated work, idle waits, and repair attempts. Never invent a numerical saving.

## Configuration Validation

After installing or changing the router, run:

```powershell
python scripts/agent_routing_check.py --json
```

For a portable project template, pass `--config <path-to-agents.toml.example> --agents-dir <path-to-agent-files>`. The check distinguishes V1 child capacity from V2 total capacity, rejects conflicting controls, permits high positive capacity without turning it into a dispatch target, and validates role capability classes, access, and conditional nesting instructions. It cannot prove backend capacity or semantic compliance; use a fresh-session runtime probe for those facts.

## Final Disclosure

When children were used, report role/model class, delegated scope, wave/integration status, and any result intentionally rejected. When a qualifying or Skill-mandated delegation was skipped, report why. Keep the disclosure compact and do not add multi-agent ceremony when no packet passed the gate.
