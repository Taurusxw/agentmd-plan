# Global AGENTS Coverage Matrix

Use this matrix to verify that the concise global outline delegates detailed behavior without losing semantic coverage.

Source global version: `27.8.0`
Source global SHA256: `53DB9EF5531A27938DF4A31F1AD73321FE21519AE1ABF9E3BFD32A28DF3095E1`
Coverage verified: `2026-07-18`

## Coverage Rule

Each global rule must be `covered`, `delegated`, or deliberately `omitted`. Coverage is semantic, not literal duplication. Global rules remain the always-on layer; references provide detailed, on-demand execution guidance.

## Section Map

| Global Section | Status | Detailed Coverage |
|---|---|---|
| 1. Core principles | covered | `execution-standards.md`, `code-change-governance.md`, `documentation-governance.md`, `verification-and-reporting.md`, `acceptance-closure.md`, `goal-mode-closure.md` |
| 2. Instruction and rule locations | covered | `rule-governance.md`, `project-agents-template.md`, `task-scaling-and-context.md` |
| 3. Task levels | covered | `task-scaling-and-context.md`, `architecture-drift.md`, `documentation-governance.md`, `verification-and-reporting.md` |
| 4. Mandatory Skill gate | covered | `low-token-guardrails.md`, `task-scaling-and-context.md`, `verification-and-reporting.md` |
| 5. Execution and edit baselines | covered | `execution-standards.md`, `code-change-governance.md`, `architecture-drift.md` |
| 6. Documentation, traceability, and versions | covered | `documentation-governance.md`, `rule-governance.md` |
| 7. Validation and acceptance closure | covered | `verification-and-reporting.md`, `acceptance-closure.md`, `goal-mode-closure.md` |
| 8. Completion check | covered | `verification-and-reporting.md`, `rule-review-checklist.md` |

## Five-Round Improvement Protocol

1. Coverage: map every global section and rule.
2. Task flow: test L0-L4, Skill routing, and context depth.
3. Change governance: test edits, documentation, progress, versions, and movement.
4. Validation: test verification depth, failure disclosure, and acceptance closure.
5. Maintainability: check size, routing, duplication, metadata, scripts, and portability.

## Acceptance Standard

- Source version and SHA256 match the candidate or installed global file.
- Every section maps to at least one direct reference.
- `SKILL.md` remains a router rather than a second global manual.
- Detailed references remain one level below `SKILL.md`.
- Deterministic checks cover size, metadata, routes, synchronized copies, and optional private state.
