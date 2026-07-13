# Project AGENTS Template Reference

Use this reference when creating, reviewing, or compacting a project-level `AGENTS.md`.

## Purpose

A project `AGENTS.md` should make future Codex runs effective inside one repository. It should not copy the global file.

## Recommended Sections

```markdown
# Project AGENTS.md

This project also follows the global Codex rules at `<global-path>`.

## Project Goal

## Tech Stack

## Directory Map

## Common Commands

## Task Level Defaults

## Documentation Mode

## Code Conventions

## Test And Completion Standard

## Git And Collaboration Boundaries

## Risk Boundaries
```

Delete sections that do not matter for the project. Keep it useful, not ceremonial.

## Section Guidance

| Section | Include |
|---|---|
| Project Goal | What the repository is for and what success means |
| Tech Stack | Runtime, frameworks, package managers, databases, external services |
| Directory Map | Only directories Codex commonly needs |
| Common Commands | Install, run, test, lint, typecheck, build, migrations |
| Task Level Defaults | Any project-specific escalation rules |
| Documentation Mode | Which docs exist and when to update them |
| Code Conventions | Naming, module boundaries, generated files, formatting |
| Test And Completion Standard | Required checks before final response |
| Git And Collaboration Boundaries | Branch, commit, staging, generated artifacts, user-change protection |
| Risk Boundaries | Data, secrets, deploy, payments, migrations, destructive operations |

## Size And Scope

Target 150-250 lines or fewer.

Move out:

- long architecture explanations to `docs/ARCHITECTURE.md`;
- API details to `docs/API.md`;
- database details to `docs/DATABASE.md`;
- recurring complex workflows to a Skill;
- local module rules to subdirectory `AGENTS.md`.

## Anti-Patterns

Avoid:

- copying the full global `AGENTS.md`;
- listing every file in the repository;
- keeping old task notes;
- including one-off debugging commands as permanent rules;
- embedding long setup tutorials better suited for `README.md` or `docs/DEVELOPMENT.md`;
- using project rules as a changelog.

## Review Checklist

- Does the file answer what future Codex needs before editing?
- Can common commands be found in under one minute?
- Are risky operations clearly marked?
- Are docs and test standards project-specific?
- Are module-specific rules closer to the module?
- Is there no duplicate long-term document doing the same job?
