# 2026-07-28 Round 001: Multi-Agent Model Routing

## Status

completed

## Goal

Implement an efficiency-governed Codex subagent model router that preserves a strong quality floor without turning ordinary work into a token-heavy agent swarm.

## Evidence

- The live Codex configuration used `gpt-5.6-sol/high` for the parent and had no `[agents]` table or custom Agent directory, so unpinned children inherited the parent configuration.
- Current Codex documentation supports global child defaults and custom Agent files that pin model, reasoning effort, sandbox, and instructions.
- Current research and mature frameworks favor centralized orchestration, independent sidecars, heterogeneous roles, bounded context transfer, and explicit termination over homogeneous Agent scaling.

## Key Decisions

- Keep single-agent execution as the default and require a concrete parallel-time, context-isolation, or specialist-review benefit before spawning.
- Use Terra/high as the minimum and fallback; route bounded implementation to Terra/max and material-risk review to Sol/high.
- Reserve reasoning above Sol/high for explicit user selection.
- Keep requirements, the critical path, integration, and final validation in the parent.
- Use one child normally, two only for independent work, and three as a hard configuration ceiling.
- Prevent nested delegation, duplicate work, full-context copying by default, and concurrent same-file writes.

## Change List

- Global `AGENTS.md` candidate `27.9.0` and synchronized installed copies.
- `multi-agent-governance.md`, Skill routing, low-token rules, coverage inventory, and reporting updates.
- Portable `[agents]` and three role templates plus their live installation.
- Deterministic `agent_routing_check.py` and unit tests.
- Chinese and English manuals, project index/progress, release notes, and acceptance record.

## Tests And Verification

- Skill creator validation passed for both project and live Skill trees.
- Seven unit tests passed, including portable routing templates, invalid fallback rejection, global gate anchors, Goal closure anchors, and architecture hotspot behavior.
- Python compilation passed for all five Skill scripts.
- Portable and live routing checks confirmed Terra/high fallback and exploration, Terra/max implementation, Sol/high review, read-only specialist roles, and concurrency ceiling 3.
- Strict guardrail with required private state passed; global, Downloads, artifact, coverage, live Skill, snapshot, and project state hashes are synchronized.
- Codex CLI `0.145.0` parsed the live configuration and reported `multi_agent` as stable and enabled.
- Markdown links, version parity, secrets, private paths, risky tracked files, historical objects above 5 MiB, whitespace, and stale lower-model references passed.

## Risks And Follow-Up

Custom role discovery and semantic task classification remain runtime/model behavior rather than mathematical guarantees. Explicit spawn overrides and the deterministic config check provide fallback and drift detection.
