# Documentation Governance Reference

Use this reference for progress records, documentation thresholds, round organization, and avoiding document sprawl.

## Task Level Documentation

| Level | Documentation Default |
|---|---|
| L0 read-only analysis | Do not write progress records. Report conclusion and evidence. |
| L1 tiny change | Do not create a round by default. Mention whether docs were unnecessary. |
| L2 normal development | Update existing project docs when affected. If `docs/progress/rounds/` exists, create or update the current round. |
| L3 important change | Record impact, decisions, validation, and risk. Update architecture, API, database, changelog, or progress docs as applicable. |
| L4 phase or release | Use `docs/progress/phases/` or `docs/progress/releases/` with plan, design, acceptance, review, and release risk. |

Do not create a full documentation tree just because a template exists. Create the minimum durable artifact required by the task and project maturity.

## Documentation Update Triggers

| Change Type | Default Documentation |
|---|---|
| Install, startup, command, environment variable, or local workflow change | `README.md`, `docs/DEVELOPMENT.md` |
| Rule, naming, directory, or convention change | `AGENTS.md`, `docs/RULES.md` |
| User-visible feature, fix, or refactor | `docs/CHANGELOG.md`, `docs/PROGRESS.md` |
| API, protocol, request, response, event, or contract change | `docs/API.md`, `docs/CHANGELOG.md` |
| Database, data model, storage, migration, or seed change | `docs/DATABASE.md`, `docs/ARCHITECTURE.md`, `docs/CHANGELOG.md` |
| Architecture, module boundary, dependency, or data-flow change | `docs/ARCHITECTURE.md`, `docs/KNOWLEDGE_GRAPH.md` |
| New, moved, renamed, archived, or deleted documentation | `docs/DOC_INDEX.md` |
| Phase or release work | `docs/progress/phases/` or `docs/progress/releases/` |

If the target document does not exist:

- L0/L1: do not create it; mention that the project has no such doc if relevant.
- L2: update only within an existing documentation system.
- L3/L4: create or propose the minimum necessary missing document if handoff would suffer without it.

## Standard Progress Structure

```text
docs/progress/
├─ README.md
├─ rounds/
├─ phases/
├─ releases/
└─ archive/
```

Round file:

```text
YYYY-MM-DD-round-001-short-task-name.md
```

Round number scope:

- Default scope is one calendar date in the target `rounds/` location.
- For date `YYYY-MM-DD`, compute the next number only from files matching `YYYY-MM-DD-round-NNN-*.md`.
- If no file exists for that date, start at `001`.
- Do not continue yesterday's last number. `2026-07-06-round-031-...` must be followed by `2026-07-07-round-001-...` unless the project explicitly declares a global monotonic counter.
- Monthly folders such as `rounds/2026-07/` do not change the rule; numbering still resets per date.

Phase directory:

```text
phase-001-short-phase-name/
├─ PLAN.md
├─ DESIGN_NOTES.md
├─ ACCEPTANCE.md
└─ REVIEW.md
```

Release directory:

```text
vx.y.z/
├─ RELEASE_NOTES.md
├─ ACCEPTANCE.md
└─ artifacts/
```

## Round Content Template

Use these sections when a round is required:

```markdown
# YYYY-MM-DD Round NNN: short task name

## Status
planned | in-progress | completed | blocked | archived

## Goal

## Background

## Scope

## Implementation Steps

## Key Decisions

## Change List

## Tests And Verification

## Documentation Updates

## Risks And Follow-Up

## Next Step
```

Keep the template concise. Do not fill it with low-value narration just to satisfy headings.

## Round Overflow Rules

- Capacity thresholds route the record; they never cancel it. If the task requires a round, "rounds is full" is not a valid reason to skip traceability.
- Same objective, same day, continuous work: update the existing round.
- Independent objective on the same day: create the next round number.
- New calendar date: start from `round-001` for that date unless a same-date round already exists.
- New phase, changed goal, unblocked work, acceptance feedback, or risk escalation: create a new round or phase.
- `rounds/` above 30 files: organize by month such as `rounds/2026-07/`.
- `rounds/` above 100 files: perform an archive or phase-summary pass before adding more.
- Same theme across 5-8 consecutive rounds: promote to `phases/phase-xxx-short-name/`.
- A single round above 250-300 lines: split details into a phase or archive summary.
- When root `rounds/` is crowded, write the current required record to one of these destinations instead of skipping it:
  - `docs/progress/rounds/YYYY-MM/YYYY-MM-DD-round-NNN-short-name.md`
  - `docs/progress/phases/phase-NNN-short-name/REVIEW.md` or another phase file when the work has become a phase
  - `docs/progress/archive/YYYY-MM-summary.md` when archiving old rounds and summarizing the current trace
- If a round cannot be written for a technical reason, state that as a failure or blocker and name the intended path; do not report it as an intentional omission.

Preserve raw historical rounds as evidence unless the user approves deletion or migration.

## Size Thresholds

| Document | Target | Response When Exceeded |
|---|---:|---|
| Global `AGENTS.md` | 120-220 non-empty lines; warning at 300 non-empty lines or 16 KiB | Stop adding detailed rules. Move project facts to project rules and complex workflows to Skills. |
| Project `AGENTS.md` | 150-250 lines | Keep commands, boundaries, and completion standards. Move module rules downward. |
| `docs/PROGRESS.md` | 150-200 lines | Keep overview, recent progress, next steps, and risks. Move details to rounds, phases, or releases. |
| `docs/DOC_INDEX.md` | 200 lines | Index core docs and directories only. Do not enumerate every historical artifact. |
| Architecture or knowledge graph docs | 500 lines | Keep overview and key relationships. Move module detail closer to code. |
| Single round | 250-300 lines | Split or summarize into a phase record. |

## Duplicate Document Controls

Avoid adding long-term documents with overlapping responsibilities, such as `notes.md`, `summary.md`, `plan.md`, `plans.md`, `guide.md`, `developer-notes.md`, `architecture-overview.md`, `knowledge-map.md`, `acceptance.md`, or `review-notes.md`, unless the project already uses that name deliberately.

Before creating a new document, check whether the content belongs in:

- `README.md` for user-facing setup or overview;
- `AGENTS.md` for agent operating rules;
- `docs/RULES.md` for project conventions;
- `docs/DEVELOPMENT.md` for local commands and workflows;
- `docs/ARCHITECTURE.md` for structure and data flow;
- `docs/CHANGELOG.md` for notable user or maintainer changes;
- `docs/PROGRESS.md` and `docs/progress/` for work tracking.

## Migration Approach

1. Inventory current documents and identify duplicated responsibilities.
2. Propose a target map before moving or deleting history.
3. Create summaries or indexes before archiving large historical sets.
4. Preserve paths and names that other docs reference until links are updated.
5. Validate that future Codex runs can find the right answer without reading unrelated history.

## Progress Summary Policy

`docs/PROGRESS.md` should answer only:

- What is the current state?
- What changed recently?
- What is next?
- What risks or blockers remain?
- Where are detailed records?

Do not paste full round logs into `docs/PROGRESS.md`. Link or summarize instead.

## Changelog Policy

`docs/CHANGELOG.md` should contain changes worth a user or maintainer knowing. It is not a commit log.

Include:

- user-visible features and fixes;
- breaking changes;
- migration notes;
- notable internal refactors that affect maintenance;
- documentation or rule changes with long-term consequence.

Exclude:

- every small typo;
- raw commit messages;
- temporary planning notes;
- repeated entries already captured in round records.
