# Rule Governance Reference

Use this reference when designing, editing, auditing, compacting, or versioning Codex rule systems.

## Rule Destination Matrix

| Destination | Use For | Avoid Putting Here |
|---|---|---|
| Global `AGENTS.md` | Universal Codex habits, task levels, safety baselines, default documentation triggers, concise output expectations | Project commands, long workflows, tool manuals, detailed examples, temporary notes |
| Project `AGENTS.md` | Project goal, tech stack, directories, commands, test standards, project-specific documentation mode | Global behavior that should apply everywhere |
| Subdirectory `AGENTS.md` | Local module conventions, generated-code boundaries, package-specific commands | Rules unrelated to that subtree |
| Skill | Repeatable complex workflow, branching process, cross-project playbook, detailed governance logic, templates or scripts | One-off project facts or rules that must always be in context |
| Project docs | Architecture, API, database, progress, changelog, TODO, domain knowledge | Agent behavior rules that should affect execution directly |
| Hooks, tests, CI, permissions | Hard enforcement, destructive operation prevention, policy gates, format and security checks | Explanations that humans need to understand |

Choose the narrowest destination that still gives future Codex runs enough context to act correctly.

## Version Bump Rules

Use `MAJOR.MINOR.PATCH` for versioned rule files such as global `AGENTS.md`.

| Change | Bump | Examples |
|---|---|---|
| No file change | none | discussion, research, backup, plan only |
| Editorial fix | `PATCH` | typo, heading number, broken link, table formatting, wording clarification that does not change behavior |
| Substantive rule improvement | `MINOR` | new validation rule, new Skill routing, refined documentation threshold, added version policy, added task escalation criterion |
| Behavioral model change | `MAJOR` | replacing the task-level system, changing default authority order, incompatible documentation structure, new mandatory workflow that affects most tasks |

When several edits happen together, apply the highest required bump. Update the date only when the file content changes.

## Concrete Version Examples

- `25.1.1 -> 25.1.2`: fix a typo in the round naming pattern or clarify an ambiguous sentence without changing the rule.
- `25.1.1 -> 25.2.0`: add automatic version bump rules, add round overflow thresholds, or introduce a Skill-first extraction rule.
- `25.1.1 -> 26.0.0`: replace L0-L4 task levels with a different workflow model, make all tasks require phase records, or change global instruction precedence.

## Impact Questions

Ask these before deciding the bump:

1. Does this change how Codex behaves on future tasks, or only how the text reads?
2. Does it affect all projects, one project, one module, or one reusable workflow?
3. Does it add a new required step, validation, artifact, or escalation rule?
4. Does it make old project rules incompatible or obsolete?
5. Would a future agent need to read much more context to follow it?

## Rule Quality Standard

A good rule is:

- actionable enough that Codex can follow it without guessing;
- scoped to the narrowest responsible file;
- testable or reviewable when possible;
- short enough to remain discoverable;
- not duplicated in multiple long-term documents;
- backed by tools when it is safety-critical.

## Skill Extraction Triggers

Move material from global `AGENTS.md` into a Skill when one or more are true:

- the workflow has many branches or repeated decision points;
- the section is useful only for a class of tasks, not every Codex turn;
- the rule needs scripts, templates, checklists, or long examples;
- the global file is near or above its warning threshold;
- future changes are expected to be frequent;
- the user wants a reusable playbook across projects.
