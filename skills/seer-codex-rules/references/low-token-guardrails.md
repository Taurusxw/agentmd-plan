# Low-Token Guardrails

Use this reference when the user wants maximum rule adherence without burning unnecessary context.

## Principle

Use layered controls, but load detail only when the task needs it.

| Layer | Token Cost | Purpose |
|---|---:|---|
| Global gate | tiny | Forces `seer-codex-rules` for rule/process/documentation/version tasks. |
| `SKILL.md` router | low | Chooses mode and relevant references. |
| Targeted reference | medium | Loads only the rule module needed for the task. |
| Script preflight | low | Checks paths, versions, gate text, Skill validity, and project provenance without reading all docs. |
| State manifest | tiny | Binds live global rules, canonical artifact, coverage inventory, and live Skill to exact hashes. |
| Current Skill snapshot | no prompt cost | Keeps the live Skill recoverable without replaying old rounds. |
| Final disclosure | low | Makes drift visible by stating Skill use, key references, and uncovered risk. |
| Project provenance | medium only when needed | Records substantial rule or Skill changes for recovery. |
| Adaptive delegation gate | low when used | Proactively routes useful packets while preventing full-context forks, duplicate work, idle capacity chasing, and verbose child returns. |

## Guardrail Tiers

| Tier | Use When | Required Actions |
|---|---|---|
| G0 unrelated read-only | Casual question or read-only work unrelated to development governance | No need to load this Skill unless another trigger matches. |
| G1 development compliance | Any file-changing development task covered by the global gate | Read `SKILL.md` once, then `task-scaling-and-context.md` and only the artifact-specific reference needed; reuse them at completion. |
| G2 rule work | Auditing or editing global/project rules, docs governance, progress, version policy, or this Skill | Read targeted references and run `guardrail_check.py` after edits; preflight only when existing drift could change the edit. |
| G3 global sync | Editing global `AGENTS.md` or synced copies | Confirm a recoverable prior artifact, update version, sync copies, compare hashes, and run one final `guardrail_check.py` plus `measure_rules.py`. |
| G4 release or migration | Large restructure, phase, archive, or policy model change | Use the fixed phase/release checklist once; do not inherit additional G1-G3 validation loops. |

Default to the lowest tier that covers the risk.

## Freshness Without Repeated Discovery

- Use the current effective live global rules already supplied to the task; do not rescan local artifacts, Git history, README files, or remote releases on every task.
- Old conversation context and cached summaries cannot downgrade the loaded rule set. A higher semantic version found elsewhere cannot replace it automatically.
- Load `governance-ownership-boundary.md` only when freshness, drift, synchronization, installation, restoration, or publication is actually involved.
- Mid-task rule edits require host reload or a new task before they are treated as effective; do not spend tokens pretending to hot-reload an instruction chain.

## Minimal Final Disclosure

For G1+ tasks, include one compact line:

```text
Skill gate: used seer-codex-rules; references: <names>; uncovered risk: <none/brief>.
```

Do not paste long checklists into routine final answers.

## Drift Detection

Use script output and final disclosure to catch drift:

- global gate missing or stale;
- `seer-codex-rules` invalid;
- project provenance missing;
- references named in `SKILL.md` missing;
- reference files present but not routed from `SKILL.md`;
- global version or date missing;
- synced copies hash mismatch.
- coverage inventory source version/hash differs from the live global file;
- live Skill tree differs from the current project snapshot or manifest;
- canonical version artifact differs from the live global file.

If drift is found, fix it before continuing when it affects the current task. Otherwise report it as residual risk.

## Token Budget Rules

- Do not read `global-agents-rule-inventory.md` unless checking full coverage.
- Do not read every reference for a normal task.
- Do not reread `SKILL.md` or a reference at completion when it remains in context and did not change; the end check reuses the selected rules.
- Prefer `guardrail_check.py` for preflight facts instead of manually reading many files.
- Use default guardrail mode for routine work; use `--strict` only for global sync, release, or a task that must fail on warnings.
- Refresh the state manifest only after a substantive Skill or approved global change, not during read-only analysis.
- Keep global `AGENTS.md` as a gate and summary, not the detailed rule body.
- Cache passing command evidence in the current task. Rerun only after a relevant invalidating change, and avoid commands whose coverage is already supplied by another passing check.
- Prefer final one-line disclosure unless the user asks for detailed audit output.
- Load `goal-mode-closure.md` only while a persistent Goal is being created, resumed, auto-continued, or closed. Keep its compact contract in the Goal objective instead of rereading project history on every continuation.
- Identify ready independent packets before material execution. When the multi-agent benefit gate passes, proactively delegate; do not wait for another user request or Ultra reasoning.
- Size each wave as the minimum of ready packets, effective free runtime slots, and the task/time/token budget. Do not impose a prose ceiling or treat configured capacity as a utilization target.
- Use `fork_turns="none"` and a compact task packet for role/model routing; use limited or full history only when the continuity benefit outweighs duplicated context.
- Route narrow work to the cheapest capable tier, require compact evidence rather than raw logs, synthesize once per wave, close completed children promptly, and never invent token savings when exact usage is unavailable.
