# Agentmd Plan

[简体中文](README.md) | [English](README.en.md)

Current version: `v27.7.0`

Agentmd Plan is a portable, verifiable, low-token governance system for Codex rules. The global `AGENTS.md` keeps only the outline that must remain active on every task, while the `seer-codex-rules` Skill loads detailed execution rules on demand.

## What It Solves

- Prevents the global `AGENTS.md` from growing without bound as rules evolve.
- Keeps small tasks lightweight while preserving validation and traceability for important development, migrations, and releases.
- Reduces rule drift through a global gate, Skill routing, modular references, validation scripts, and final disclosure.
- Constrains repeated acceptance loops, excessive rounds, and overdevelopment of low-probability edge conditions.
- Restores architecture and module-boundary decisions before repeated patches turn a production hotspot into structural drift.
- Keeps personal paths, private backups, and live state outside the public repository.

## Release Contents

- `artifacts/AGENTS-27.7.0.md`: the concise global rule outline.
- `skills/seer-codex-rules/`: the Skill for rule design, task scaling, code and documentation governance, round/phase/release handling, acceptance closure, and versioning.
- `skills/seer-codex-rules/scripts/`: checks for rule size, Skill routing, structural hotspots, synchronized state, and recovery snapshots.
- `docs/`: public project status, document index, and necessary development and release records.
- `VERSION`: the current project release version.

## How It Works

```text
global AGENTS.md
  -> requires seer-codex-rules/SKILL.md
      -> selects an L0-L4 and guardrail tier
          -> loads only the reference needed by the task
              -> change, validate, trace, and close
```

An ordinary file-changing task loads the Skill router, task-scaling guidance, and one artifact-specific reference. Full guardrails are reserved for rule synchronization, migrations, and releases, keeping compliance from consuming unnecessary context.

## Installation

1. Back up the existing `<codex-home>/AGENTS.md` and Skill directory.
2. Copy `skills/seer-codex-rules/` to `<codex-home>/skills/seer-codex-rules/`.
3. Review `artifacts/AGENTS-27.7.0.md` and confirm that it matches your operating preferences.
4. Install that artifact as `<codex-home>/AGENTS.md`.
5. Run the validation commands below to verify the version, Skill routing, and synchronized state.

`<codex-home>` is normally set by the `CODEX_HOME` environment variable. When unset, it is usually `<user-home>/.codex`.

## Core Governance

### Task Levels

- `L0`: read-only analysis; no file changes or development records.
- `L1`: tiny change; smallest complete edit and direct validation, with no round by default.
- `L2`: normal development; targeted tests and traceability within the project's existing system.
- `L3`: important change; impact review, recorded decisions, and broader validation.
- `L4`: phase, migration, or release; phase/release records suitable for handoff.

### Acceptance And Edge Closure

- Stop adding gates after the original acceptance criteria pass.
- A new finding enters the current task automatically only when it blocks the original goal or creates material security, permission, privacy, or data risk.
- An ordinary edge condition needs evidence, direct relevance to the goal, and a proportionate fix with focused validation.
- L2 permits at most one extra edge-hardening pass; stop when two consecutive iterations improve only hypothetical robustness.

### Architecture Drift Control

- Load the architecture-drift reference and script only when one production module is repeatedly patched or the current change adds responsibility, interface breadth, duplicated logic, or test coupling.
- Three consecutive tasks or five of the latest ten records touching the same file form a hotspot signal; more than 800 non-empty lines and 20 entry branches are supporting signals.
- Line count alone never requires a split. Freeze new responsibility at two signals; at three or more, upgrade to L3 and define the module boundary.
- `structure_check.py` reports evidence only. It never refactors automatically and cannot replace semantic review of serialized runtime code or intentional duplication.

### Traceability Control

- Continue the existing record for uninterrupted work on the same objective.
- Round numbering resets by date and increments only for independent objectives on the same day.
- Capacity thresholds may change where a record is stored, but never justify skipping required traceability.
- Promote multi-day, multi-round, or release work to a phase/release instead of accumulating endless rounds.

## Validation

Run from the repository root:

```powershell
python skills/seer-codex-rules/scripts/measure_rules.py --strict artifacts/AGENTS-27.7.0.md
python -m py_compile skills/seer-codex-rules/scripts/guardrail_check.py skills/seer-codex-rules/scripts/measure_rules.py skills/seer-codex-rules/scripts/snapshot_state.py skills/seer-codex-rules/scripts/structure_check.py
python -m unittest discover -s skills/seer-codex-rules/tests -p test_structure_check.py -v
python skills/seer-codex-rules/scripts/guardrail_check.py --strict --project . --global-agents artifacts/AGENTS-27.7.0.md --downloads-agents artifacts/AGENTS-27.7.0.md --skill skills/seer-codex-rules --json
```

After installation, `snapshot_state.py --write` can create a private state manifest and Skill recovery snapshot. Do not commit live manifests or backups that contain personal paths.

## Upgrade And Rollback

- Project releases, Git tags, and GitHub Releases use `vMAJOR.MINOR.PATCH`.
- A global workflow-model or compatibility change increments `MAJOR`.
- A substantive long-term rule, Skill route, or governance capability increments `MINOR`.
- A typo, formatting, or link correction that does not change behavior increments `PATCH`.
- To roll back, restore both the previous global rules and Skill, then rerun synchronization and coverage checks.

## Privacy And Security

The public repository excludes personal machine paths, historical private backups, live state, credentials, and binary recovery bundles. Prose rules do not replace sandboxing, approvals, permissions, tests, CI, or human safety review.

## Contributing And License

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting improvements. Report security issues privately through [SECURITY.md](SECURITY.md).

This project is licensed under the [MIT License](LICENSE).
