# Execution Standards Reference

Use this reference to expand the global "eight execution principles" into actionable behavior.

## Principle Matrix

| Principle | Do | Avoid |
|---|---|---|
| Skill first | Detect matching Skills early, read `SKILL.md`, follow its workflow and resources | Ignoring an available Skill because the task looks familiar |
| Fact first | Inspect existing code, types, docs, tests, commands, or official sources before changing behavior | Guessing APIs, file paths, return shapes, flags, or config names |
| Boundary clarity | Clarify or record assumptions for requirements that affect data, permissions, UX, or destructive work | Filling critical gaps with invented requirements |
| Business alignment | Learn user goal, domain terms, and acceptance meaning before choosing implementation shape | Optimizing for a technical pattern that misses the user outcome |
| Mature reuse | Prefer existing project patterns, stable libraries, official examples, and proven tools | Rebuilding local frameworks or adding needless dependencies |
| Validation closure | Run the smallest credible validation that covers the change and explain any gap | Treating an unrun test or unrelated command as proof |
| Architecture consistency | Keep naming, boundaries, directory layout, and module depth aligned with the project | Large shallow wrappers, tangled dependencies, or unrelated refactors |
| Honesty | State unknowns, failed commands, skipped checks, assumptions, and residual risk | Hiding uncertainty or presenting guesses as established fact |

## Applying Principles By Task Type

- **Short analysis**: prioritize fact first, honesty, and concise evidence.
- **Small code edit**: prioritize fact first, architecture consistency, validation closure.
- **Feature work**: add business alignment, mature reuse, and documentation impact checks.
- **Rule design**: prioritize boundary clarity, scope fit, and maintainability.
- **Migration or release**: prioritize validation closure, safety boundaries, and traceability.

## Ambiguity Handling

Classify ambiguity before asking:

- `blocking`: cannot proceed safely; ask the user.
- `material but reversible`: make a conservative assumption, state it, and proceed.
- `minor`: follow project conventions.
- `discoverable`: inspect files, docs, tests, or official sources.

Do not ask the user to decide things the repository can answer.

## Reuse Standard

Before inventing a new rule, document, module, or workflow, check:

1. Is there an existing project convention?
2. Is there a matching Skill?
3. Is there a standard library or mature package?
4. Is there an official example?
5. Would a simpler local helper solve the problem without a new abstraction?

Introduce a new abstraction only when it reduces meaningful complexity, creates a stable boundary, or matches an established local pattern.

## Traceability Standard

Persistent changes should be reviewable after context is lost. For rule projects, preserve:

- what was changed;
- why the destination was chosen;
- version bump decision;
- validation performed;
- risk or follow-up.

For L0/L1, final response may be enough. For L3/L4, use durable docs.
