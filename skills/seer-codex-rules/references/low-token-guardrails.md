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

## Guardrail Tiers

| Tier | Use When | Required Actions |
|---|---|---|
| G0 unrelated read-only | Casual question or read-only work unrelated to development governance | No need to load this Skill unless another trigger matches. |
| G1 development compliance | Any file-changing development task covered by the global gate | Read `SKILL.md`, `task-scaling-and-context.md`, and only the artifact-specific reference needed; use one compact final disclosure. |
| G2 rule work | Auditing or editing global/project rules, docs governance, progress, version policy, or this Skill | Run `guardrail_check.py`; read targeted references; update provenance if the edit is substantial. |
| G3 global sync | Editing global `AGENTS.md` or synced copies | Backup, update version if needed, sync copies, compare hashes, run `guardrail_check.py` and `measure_rules.py`. |
| G4 release or migration | Large restructure, phase, archive, or policy model change | Use phase/release records, coverage inventory, broad validation, and explicit residual risk. |

Default to the lowest tier that covers the risk.

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
- Prefer `guardrail_check.py` for preflight facts instead of manually reading many files.
- Use default guardrail mode for routine work; use `--strict` only for global sync, release, or a task that must fail on warnings.
- Refresh the state manifest only after a substantive Skill or approved global change, not during read-only analysis.
- Keep global `AGENTS.md` as a gate and summary, not the detailed rule body.
- Prefer final one-line disclosure unless the user asks for detailed audit output.
- Load `goal-mode-closure.md` only while a persistent Goal is being created, resumed, auto-continued, or closed. Keep its compact contract in the Goal objective instead of rereading project history on every continuation.
