# Multi-Agent Governance

Use this reference before spawning, routing, or integrating subagents. Parallel work is useful only when it produces a concrete net benefit without losing ownership or verification.

## Net-Benefit Gate

Delegate only when every condition holds:

1. The packet is bounded, independently verifiable, and can return compact evidence.
2. Its read/write set is disjoint from concurrent work, or it is read-only.
3. It does not block the root's immediate decision, or it isolates noisy context or adds a named specialist review.
4. It has a named benefit: shorter critical path, better isolation, suitable capability routing, or stronger assurance on a material risk.
5. Expected coordination and review cost is lower than the benefit.

Task size, idle slots, or a request to be thorough do not pass this gate. Stop or avoid a wave when work overlaps, evidence repeats, root integration is ready, service limits intervene, or acceptance is already covered.

## Root Ownership

The root retains requirement interpretation, scope and completion contract, dependency and wave decisions, write-set assignment, cross-boundary integration, conflict resolution, final validation, and user reporting. Continue useful non-overlapping work while children run; wait only at a real synthesis barrier.

## Effective Access Gate

Immediately before each spawn, record and compare:

```text
Required effective access: <read-only | write | network | approval-bearing>
Required capability scope: <paths, tools, services, domains, recipients, or sinks>
Parent permission checked: <yes/no; immediately before this spawn>
Current parent effective access: <live sandbox, write, network, and approval facts>
Parent access observation source: <current task profile or runtime metadata>
Dispatch decision: <compatible | root-only | approval/new-task required; comparison>
```

Read-only roles do not receive write packets. A write, network, or approval-bearing packet is compatible only when the current parent access covers it. Static role files, configuration, ACLs, and earlier spawns are not runtime proof. If the check is missing or insufficient, keep permitted work in the root or request the one needed authorization; do not loop.

## Waves and packets

Use the smallest wave justified by ready packets, live capacity, and the task budget; capacity is a limit, never a target. A useful sequence is discovery, root synthesis and ownership freeze, disjoint implementation, then targeted integrated review.

Send only the facts a child cannot cheaply rediscover:

```text
Role: <read-only explorer | implementation worker | reviewer>
Objective: <one bounded deliverable>
Write ownership: <disjoint paths or none>
Do not touch: <excluded paths>
Known facts: <minimum necessary context>
Required effective access: <...>
Required capability scope: <...>
Parent permission checked: <...>
Current parent effective access: <...>
Parent access observation source: <...>
Dispatch decision: <...>
Validation: <specific evidence>
Return: <at most eight bullets; change/evidence/tests/risk>
Delegation: <none unless explicitly authorized>
```

Use fresh compact context by default. Include prior turns only when continuity changes the result. Children return the completed change or conclusion, exact paths/commands/links, focused validation, and one residual risk—not raw transcripts, repeated prompts, or default hashes.

## Integration and recursion

Assign one writer per file, migration, lockfile, or generated artifact. Recheck the shared tree before integration and preserve unrelated changes. A child result is evidence to be accepted or rejected by the root, not automatic completion.

Prefer a flat root wave. Recursive work is allowed only when the parent packet expressly authorizes it and the child repeats the net-benefit, disjoint ownership, live-access, compact-packet, and integration gates.

## Configuration boundary

`agent_routing_check.py` validates static configuration shape and packet compatibility fields; its JSON report remains static evidence and must report `runtime_permissions_verified=false` and `dispatch_ready=false`.

Treat `features.multi_agent_v2` only as a non-public, non-portable compatibility input. Do not add it to portable templates or infer runtime capacity, root-inclusion semantics, model availability, or permission from it. Model and capacity selection are runtime decisions based on the packet, available capabilities, and current limits.

## Integrity and disclosure

Default to zero hashes, checksums, manifests, and byte comparisons. When an actual global/live synchronization or recovery consumer requires byte identity, name that consumer and make one final comparison in the owning stage. It never substitutes for semantic review or focused validation.

For material waves, record only attempted/accepted packets and a primary rejection or rework reason when useful. In the final report state delegated scope, integration status, and rejected material results; omit multi-agent ceremony when no packet passed the gate.
