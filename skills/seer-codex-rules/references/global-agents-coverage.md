# Global AGENTS Coverage Matrix

Use this matrix to verify that the concise global outline delegates detailed behavior without losing semantic coverage.

Source global version: `27.13.0`
Source global SHA256: `F5E8D50863462A6EE0B7F733177E0F1971F86D873108656DD0B9EAFA532014B7`
Coverage verified: `2026-08-03`

## Coverage Rule

Each global rule must be `covered`, `delegated`, or deliberately `omitted`. Coverage is semantic, not literal duplication. Global rules remain the always-on layer; references provide detailed, on-demand execution guidance.

## Section Map

| Global Section | Status | Detailed Coverage |
|---|---|---|
| 1. Core principles | covered | `task-scaling-and-context.md`, `execution-standards.md`, `code-change-governance.md`, `documentation-governance.md`, `verification-and-reporting.md`, `acceptance-closure.md`, `goal-mode-closure.md`, `multi-agent-governance.md`, companion `<codex-home>/skills/seer-capture/SKILL.md` |
| 2. Instruction and rule locations | covered | `rule-governance.md`, `project-agents-template.md`, `task-scaling-and-context.md` |
| 3. Task levels | covered | `task-scaling-and-context.md`, `architecture-drift.md`, `documentation-governance.md`, `verification-and-reporting.md` |
| 4. Mandatory Skill gate | covered | `low-token-guardrails.md`, `task-scaling-and-context.md`, `verification-and-reporting.md`, `multi-agent-governance.md` |
| 5. Execution and edit baselines | covered | `execution-standards.md`, `code-change-governance.md`, `architecture-drift.md` |
| 6. Documentation, traceability, and versions | covered | `documentation-governance.md`, `rule-governance.md` |
| 7. Validation and acceptance closure | covered | `verification-and-reporting.md`, `acceptance-closure.md`, `goal-mode-closure.md` |
| 8. Completion check | covered | `verification-and-reporting.md`, `rule-review-checklist.md` |

## Single-Pass Audit Dimensions

Cover these dimensions in one audit pass; they are not five sequential review rounds:

1. Coverage and task flow.
2. Change, documentation, and version governance.
3. Validation, authorization, and closure behavior.
4. Maintainability, routing, and duplication.
5. Deterministic metadata, scripts, and portability.

## Acceptance Standard

- Source version and SHA256 match the candidate or installed global file.
- Every section maps to at least one direct reference.
- `SKILL.md` remains a router rather than a second global manual.
- Detailed references remain one level below `SKILL.md`.
- Deterministic checks cover size, metadata, routes, synchronized copies, and optional private state.
