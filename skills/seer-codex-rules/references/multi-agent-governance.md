# Multi-Agent Governance

Use this reference before spawning, routing, or coordinating subagents. Its purpose is to reduce wall-clock time or isolate noisy context without multiplying token cost, duplicated work, and integration risk.

The operational model is centralized: the parent owns requirements, the critical path, decisions, integration, and final validation. Children are bounded sidecars, not an autonomous swarm.

## Single-Agent Default

Keep work in the parent when any of these applies:

- the task is a quick fix, a single-file change, or a short read-only question;
- the next parent action is blocked on the delegated result;
- phases share substantial context or require repeated back-and-forth;
- work is sequential, tightly coupled, or likely to touch the same files;
- explaining the task packet costs as much as doing the task locally;
- the only reason to delegate is that the task is large, difficult, or described as thorough.

L0-L2 normally remain single-agent. L3-L4 may use children, but task level alone never authorizes spawning.

## Delegation Benefit Gate

Delegate only when all mandatory conditions pass:

1. The subtask is concrete, bounded, and independently verifiable.
2. The parent has useful non-overlapping work to do immediately.
3. Read/write ownership is disjoint, or the child is read-only.
4. The child can return a compact result without transferring its raw working context.
5. At least one material benefit exists: parallel time savings, noisy-context isolation, or specialist review of a named risk.

Do not spawn duplicate agents to answer the same question by default. Use a second opinion only for a material correctness, architecture, security, data, or release risk that justifies its cost.

## Critical Path Ownership

The parent must retain:

- requirement interpretation and scope decisions;
- the immediate blocking step;
- cross-module design and integration;
- conflict resolution and final edits across child boundaries;
- final validation, completion judgment, and user reporting.

Do not delegate the critical path and then wait idly. Continue non-overlapping local work while children run. Wait only when the next parent step genuinely depends on a child result.

## Model Routing Matrix

Use capability tiers by task, not one model for every child. Verify model availability from the current runtime; when an identifier is unavailable, select the closest fast, balanced, or deep model offered by that runtime.

| Role | Preferred Configuration | Scope | Default Access |
|---|---|---|---|
| `explorer_fast` | `gpt-5.6-terra`, high | Search, code mapping, logs, supporting docs, large-file summaries | read-only |
| `worker_balanced` | `gpt-5.6-terra`, max | Bounded implementation with a disjoint write set | inherit parent permissions |
| `reviewer_deep` | `gpt-5.6-sol`, high | Architecture, security, data, compatibility, correctness, final release risk | read-only |

Use `gpt-5.6-terra` with high reasoning as both the minimum child tier and the unclassified fallback. Use Terra/max for bounded implementation and Sol/high for material-risk review. Reasoning above Sol/high requires an explicit user decision. Do not route any child below Terra/high merely for nominal token savings because failed attempts and rework can cost more than the initial saving.

Model resolution follows current Codex behavior:

1. a model or effort pinned in a custom agent file;
2. an explicit value supplied at spawn time;
3. the corresponding `[agents]` default;
4. the parent setting.

If the runtime does not expose custom-role selection, pass `model` and `reasoning_effort` explicitly when spawning and include the role contract in the task packet. Do not assume an unpinned child will choose a cheaper model deterministically.

## Compact Context Packet

Prefer a fresh child context rather than forking full conversation history. Send only:

```text
Role: <explorer_fast | worker_balanced | reviewer_deep>
Objective: <one bounded deliverable>
Scope: <allowed paths, services, or questions>
Do not touch: <excluded paths and responsibilities>
Known facts: <minimum facts the child cannot cheaply rediscover>
Validation: <specific command or evidence expected>
Return: <compact result contract>
```

Use a full context fork only when the child needs decisions or constraints that cannot be summarized safely. Never copy project history, unrelated references, or raw logs merely for convenience.

## Result Contract

Require children to return:

- the conclusion or completed change;
- exact files, symbols, commands, or source links that support it;
- validation performed and failures encountered;
- one short residual-risk statement;
- no raw exploratory transcript, repeated prompt, or long unfiltered log.

Prefer at most eight concise bullets or an equivalent compact patch summary. The parent reviews evidence and integrates only what is relevant to the frozen objective.

## Concurrency And Write Safety

- Normal concurrency: one child.
- Use two concurrent children only for genuinely independent work with distinct outputs.
- Treat three children as a hard global ceiling for exceptional L3/L4 decomposition, not a target.
- Never have multiple agents modify the same file or overlapping generated artifacts concurrently.
- Assign explicit write sets before parallel implementation.
- Stop or redirect a child when its task becomes obsolete; do not let sunk token cost justify continued work.

## No Nested Delegation

Children must not spawn descendants by default. The parent remains the only orchestrator. If a platform technically permits nesting, use it only under an explicit higher-priority instruction and a separately justified benefit gate.

## Lifecycle And Closure

1. Classify the local critical path before spawning.
2. Spawn the smallest sufficient role with a compact packet.
3. Continue non-overlapping parent work.
4. Wait once when integration becomes blocked; do not poll repeatedly.
5. Review the returned evidence and reject scope drift.
6. Close Completed Agents immediately because completed but open children may still consume concurrency capacity.
7. Integrate, validate the combined result, and finish when the original completion contract passes.

## Token And Efficiency Accounting

Prefer deterministic proxies when exact child usage is unavailable:

- number of spawned and concurrently open children;
- whether full context was forked;
- child return length and raw-log volume;
- duplicated searches or edits;
- parent idle waits and repeated polling;
- rework caused by underpowered routing;
- elapsed time relative to a plausible single-agent path.

Use exact request, cached, reasoning, input, and output token metrics only when the platform exposes them. Never invent numerical savings. If delegation did not produce a concrete time, isolation, or risk-review benefit, keep the next comparable task single-agent.

## Configuration Validation

After installing or changing the router, run:

```powershell
python scripts/agent_routing_check.py --json
```

For a portable project template, pass `--config <path-to-agents.toml.example> --agents-dir <path-to-agent-files>`. This check validates the fallback, concurrency ceiling, role names, model tiers, reasoning effort, required read-only roles, and non-empty role instructions. It does not prove that a model followed the semantic routing policy.

## Final Disclosure

When children were used, report roles/models, delegated scope, integration status, and any child result intentionally rejected. When no child was needed, do not add multi-agent ceremony to the final answer.
