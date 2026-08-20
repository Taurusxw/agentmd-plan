# Low-Token Guardrails

Use this reference for governance-sensitive work. Keep normal development focused on the project's own instructions and the smallest credible validation.

## Tiers

| Tier | Trigger | Action |
|---|---|---|
| G0 | routine L0-L2 work | No universal governance compliance check. |
| G1 | rules, `AGENTS.md`, version/progress/docs governance | Read the targeted reference and run only its affected check. |
| G2 | global sync/recovery, release, migration, architecture drift, Goal/acceptance expansion, multi-agent routing | Read the named detailed reference and use its finite validation path. |

The current host-loaded global rules are authoritative. Do not scan artifacts, history, snapshots, or remotes merely to find a newer version. A changed rule does not hot-reload into the current task.

## Minimal controls

- Read `SKILL.md` and one directly relevant reference, not the entire governance library.
- Use `guardrail_check.py` only for governance-sensitive rule work; use `measure_rules.py`, `structure_check.py`, or `agent_routing_check.py` only when their specific subject changed.
- Do not refresh a snapshot, manifest, or hash as routine evidence. A final byte comparison occurs once only for an actual global/live synchronization or recovery consumer.
- Keep final disclosure to the changed governance behavior, focused evidence, and an uncovered risk.
- For delegation, use `multi-agent-governance.md`: compact packets, live access comparison, disjoint ownership, named net benefit, and root integration.
