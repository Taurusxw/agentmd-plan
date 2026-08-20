# Agentmd Plan

[简体中文](README.md) | [English](README.en.md)

Prepared release candidate: `v30.0.0` (not yet accepted or published)

The current checkout and public artifact target `30.0.0`. The source and separate distribution repositories in the two-repository release path, along with maintainer-environment installation, Git tagging, and the GitHub Release, are recorded separately only when completed; GitHub retains historical tags, Releases, and Git commit history, while the checkout follows a latest-only local-asset policy.

Agentmd Plan is a portable, verifiable, low-token governance system for Codex rules. The global `AGENTS.md` keeps only the outline that must remain active on every task, while the `seer-codex-rules` Skill loads detailed execution rules on demand.

## What It Solves

- Prevents the global `AGENTS.md` from growing without bound as rules evolve.
- Keeps small tasks lightweight while preserving validation and traceability for important development, migrations, and releases.
- Reduces rule drift through conditional governance routing, Skill routing, modular references, validation scripts, and final disclosure.
- Constrains repeated acceptance loops, excessive rounds, and overdevelopment of low-probability edge conditions.
- Lets in-scope local edits and non-destructive validation proceed by default while making repeated permission prompts, regression tests, and security review evidence-triggered.
- Freezes finite completion criteria for persistent Goals so auto-continuations cannot turn optional edges into endless required work.
- Restores architecture and module-boundary decisions before repeated patches turn a production hotspot into structural drift.
- Delegates only when independent packets have a concrete net benefit and the runtime permits it, sizes waves from available capacity and task budget, and controls coordination cost through compact contexts and exclusive write ownership.
- Keeps personal paths, private backups, and live state outside the public repository.
- Keeps screenshots, documents, links, and research analysis-only by default. It invokes `seer-capture` only when the user explicitly routes the named material to Knowledge or a named Book, and never inherits that authorization across conversations or adjacent tasks.
- Allows direct changes to the global `AGENTS.md` and `seer-codex-rules` only inside the dedicated `agentmd-plan` owner project; every other project is report-only.
- Makes every task follow the latest effective global rules actually loaded by the host; old context cannot downgrade them, and the highest version found elsewhere cannot trigger an autonomous switch.

## Release Contents

- `artifacts/AGENTS-30.0.0.md`: the prepared global-rule candidate; installation and publication remain separately accepted steps.
- `config/`: optional multi-agent configuration and role examples. Their capacity and model identifiers are not current governance defaults; choose them from actual runtime capability and task need.
- `skills/seer-codex-rules/`: the Skill for rule design, task scaling, code and documentation governance, round/phase/release handling, acceptance closure, and versioning.
- `skills/seer-codex-rules/scripts/`: checks for rule size, Skill routing, structural hotspots, synchronized state, and recovery snapshots.
- `docs/`: public project status, document index, and necessary development and release records.
- `VERSION`: the current project release version.

The current checkout retains only the latest release assets to reduce local duplication. GitHub keeps older tags and Releases, and Git commit history is not rewritten.

## How It Works

```text
global AGENTS.md
  -> loads matching Skills for the task
      -> loads seer-codex-rules for governance-sensitive work
          -> selects an L0-L4, guardrail tier, and independent packets
              -> delegates only after the net-benefit gate and sizes waves to live capacity/budget
                  -> loads only the reference needed by the task
                      -> change, validate, trace, and close
```

Tasks that match an existing Skill load that Skill normally. `seer-codex-rules` loads only for governance-sensitive work: rules or `AGENTS.md`, version/progress/documentation governance, release/migration/global sync, architecture drift, Goal/acceptance expansion, or multi-agent coordination. Ordinary L1/L2 and single-file work does not trigger it merely because a local edit was requested. Delegate only when the net-benefit gate passes, rather than to satisfy capacity.

## Installation

1. Back up the existing `<codex-home>/AGENTS.md`, `config.toml`, `agents/`, and Skill directory.
2. Copy `skills/seer-codex-rules/` to `<codex-home>/skills/seer-codex-rules/`.
3. Review `artifacts/AGENTS-30.0.0.md` to confirm that it fits your workflow.
4. Install that artifact as `<codex-home>/AGENTS.md`.
5. If adopting the optional examples, merge the `[agents]` table from `config/agents.toml.example` into `<codex-home>/config.toml`, then copy `config/agents/*.toml` to `<codex-home>/agents/`. `[features.multi_agent_v2]` is a non-public, non-portable runtime input, not a documented template or migration target; do not author it in new configuration.
6. Run the validation commands below to verify the version, Skill routing, model roles, and synchronized state.

`<codex-home>` is normally set by the `CODEX_HOME` environment variable. When unset, it is usually `<user-home>/.codex`.

## Core Governance

### Task Levels

- `L0`: read-only analysis; no file changes or development records.
- `L1`: tiny change; smallest complete edit and direct validation, with no round by default.
- `L2`: normal development; targeted tests and traceability within the project's existing system.
- `L3`: important change; impact review and a small validation matrix mapped to real risks.
- `L4`: phase, migration, or release; run the established phase/release checklist once against the final state.

### Execution Efficiency And Authorization

- Change, build, fix, or optimize requests authorize in-scope local reads, edits, formatting, and non-destructive validation without another question.
- Confirm only external writes or publication, destructive or irreversible actions, purchases, credential disclosure, or a material change in target or risk; confirm the same authorization envelope once.
- Move through direct, behavioral, affected, and full-release validation only as lower steps become insufficient.
- Ordinary tasks generate no hash, checksum, or manifest by default. Compute one only when acceptance explicitly requires byte identity and names an actual consumer; integrity metadata cannot replace semantic, source, behavioral, test, or visual evidence.
- Passing evidence expires only after a relevant code, test, configuration, dependency, generated-input, or environment change; do not repeat identical or overlapping checks.
- Full regression and security scans are event-triggered. Merely mentioning security or permissions does not activate them.
- Prefer tests that distinguish the buggy baseline from the fixed candidate; a suite that already passed is regression evidence, not repair proof.

### Centralized Governance Ownership

- The dedicated `agentmd-plan` project exclusively maintains the global `AGENTS.md`, synchronized copies, and the source and installed copies of `seer-codex-rules`.
- Other projects may inspect drift, defects, or improvement opportunities read-only, but must return a change report covering evidence, the proposed diff, version impact, cross-project risk, validation, and rollback.
- The user transfers that report into the owner-project conversation for evaluation. Sync scripts, installers, restore tasks, and subagents cannot bypass this boundary.

### Latest Effective Rules

- "Latest" means the live global rules the host actually supplies to the current task, not the highest semantic version discovered in local files, Git history, or a remote Release.
- Old conversations, cached summaries, historical artifacts, README files, snapshots, and project notes cannot downgrade the loaded rules.
- A rule changed during an active task is not assumed to hot-reload. It becomes effective in a new task or after an explicit host reload, while normal instruction priority and centralized ownership still apply.

### Acceptance And Edge Closure

- Stop adding gates after the original acceptance criteria pass.
- A new finding enters the current task automatically only when it blocks the original goal or creates material security, permission, privacy, or data risk.
- An ordinary edge condition needs evidence, direct relevance to the goal, and a proportionate fix with focused validation.
- L2 permits at most one extra edge-hardening pass; stop when two consecutive iterations improve only hypothetical robustness.

### Goal Mode Closure

- When creating or resuming a persistent Goal, store the outcome, 3-5 frozen criteria, non-goals, fixed validation budget, and closure rule in the Goal objective.
- Convert open-ended words such as fully, completely, best, or no omissions into observable criteria instead of unlimited `required work`.
- Admit new findings only when a criterion fails, the current change caused a regression, or a material safety risk appears; list other findings as at most three follow-ups.
- If one continuation makes no contract progress, allow one diagnostic pass only for a real blocker. Mark the Goal `complete` as soon as all criteria pass, without recursively hardening test or acceptance tooling.

### Architecture Drift Control

- Load the architecture-drift reference and script only when one production module is repeatedly patched or the current change adds responsibility, interface breadth, duplicated logic, or test coupling.
- Three consecutive tasks or five of the latest ten records touching the same file form a hotspot signal; more than 800 non-empty lines and 20 entry branches are supporting signals.
- Line count alone never requires a split. Freeze new responsibility at two signals; at three or more, upgrade to L3 and define the module boundary.
- `structure_check.py` reports evidence only. It never refactors automatically and cannot replace semantic review of serialized runtime code or intentional duplication.

### Multi-Agent And Model Routing

- Identify independent discovery, implementation, validation, and specialist-review packets. Delegate only when a packet is bounded, independently verifiable, write-disjoint, permitted by the runtime, and offers speed, isolation, capability-routing, or material-risk coverage that clearly outweighs coordination and token cost.
- Wave size is the minimum of ready packets, effective free slots, and the task/time/token budget. Governance has no fixed one/two/three-agent ceiling, and configured capacity is not a utilization target.
- Model and reasoning tiers in optional role examples are historical configuration references, not governance defaults. Select a compatible role from actual available capability, task complexity, and cost at dispatch time.
- Before each spawn, state the packet's required read/write/network/approval access and check the parent task's current effective permission mode. A role file's static `sandbox_mode` is only a default capability signal, not proof of that child's final access.
- Also record the concrete paths, tools, services, or side-effect sinks, the parent access actually observed and its observation source, and the compatibility decision for this spawn; a bare `checked=yes` is not auditable evidence.
- Send write packets only to implementation workers. If the parent mode is insufficient or an old task is inconsistent, keep permitted work in the root and request access once or recommend a fresh task with the correct mode instead of letting children loop on permission prompts.
- The root owns requirements, the critical path, write assignment, wave synthesis, integration, and final validation. A file or generated artifact has one concurrent writer.
- Freeze an acceptance signal and task-scoped ceiling for each non-trivial wave. Continue only when new evidence can change the decision or close a named gap, and record first-pass acceptance, rework, and rejection reasons.
- When the current orchestrator supports it, prefer compact fresh context; specific context parameters are host adaptations, not portable configuration contracts. Nesting is off by default and requires an explicitly authorized recursive packet that repeats the same gates.
- 31 spawned-agent threads (normally 32 total with the root) are historical configuration and stress evidence, not a governance capacity default. Each task follows runtime hard limits and effective free slots.

### Traceability Control

- Continue the existing record for uninterrupted work on the same objective.
- Round numbering resets by date and increments only for independent objectives on the same day.
- Capacity thresholds may change where a record is stored, but never justify skipping required traceability.
- Promote multi-day, multi-round, or release work to a phase/release instead of accumulating endless rounds.

## Validation

Run from the repository root:

```powershell
python skills/seer-codex-rules/scripts/measure_rules.py --strict artifacts/AGENTS-30.0.0.md
python -m py_compile skills/seer-codex-rules/scripts/agent_routing_check.py skills/seer-codex-rules/scripts/guardrail_check.py skills/seer-codex-rules/scripts/measure_rules.py skills/seer-codex-rules/scripts/snapshot_state.py skills/seer-codex-rules/scripts/structure_check.py
python -m unittest discover -s skills/seer-codex-rules/tests -p "test_*.py" -v
python skills/seer-codex-rules/scripts/agent_routing_check.py --config config/agents.toml.example --agents-dir config/agents --json
python skills/seer-codex-rules/scripts/guardrail_check.py --strict --project . --global-agents artifacts/AGENTS-30.0.0.md --downloads-agents artifacts/AGENTS-30.0.0.md --skill skills/seer-codex-rules --json
codex --strict-config doctor --summary
codex debug prompt-input probe
```

After installation, run `agent_routing_check.py --json` without path overrides to check the live static router configuration. It always reports `runtime_permissions_verified=false`; each spawn still needs a fresh check of the parent task's live permission mode. `snapshot_state.py --write` can create a private state manifest and Skill recovery snapshot. Do not commit live manifests or backups that contain personal paths.

## Upgrade And Rollback

- Project releases, Git tags, and GitHub Releases use `vMAJOR.MINOR.PATCH`.
- A global workflow-model or compatibility change increments `MAJOR`.
- A substantive long-term rule, Skill route, or governance capability increments `MINOR`.
- A typo, formatting, or link correction that does not change behavior increments `PATCH`.
- To roll back, restore the previous accepted global rules, Skill, `config.toml`, and custom agent files. Source-repository release and maintainer-environment installation are separate targets: confirm each independently and rerun the affected checks.

## Privacy And Security

The public repository excludes personal machine paths, historical private backups, live state, credentials, and binary recovery bundles. Prose rules do not replace sandboxing, approvals, permissions, tests, CI, or human safety review.

## Contributing And License

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting improvements. Report security issues privately through [SECURITY.md](SECURITY.md).

This project is licensed under the [MIT License](LICENSE).
