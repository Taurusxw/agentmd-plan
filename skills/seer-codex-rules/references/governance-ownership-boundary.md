# Governance Ownership Boundary

Use this reference whenever a task proposes changing, synchronizing, installing, restoring, or publishing the global Codex governance system.

## Protected Assets

The centralized boundary covers:

- the live global `<codex-home>/AGENTS.md`;
- configured synchronized or distribution copies of that global file;
- public candidate and release artifacts for the global file;
- the public source, installed copies, snapshots, manifests, validators, tests, and release records of `seer-codex-rules`.

Project-specific `AGENTS.md` files and unrelated Skills are not protected by this boundary unless a proposed edit would indirectly change or replace a protected asset.

## Owner Context Gate

Direct writes are permitted only when all conditions are true:

1. The current workspace contains the canonical `agentmd-plan` project.
2. The nearest effective project `AGENTS.md` declares that project as the governance owner.
3. The current user request explicitly targets maintenance of the global governance system.

The folder name alone is insufficient if the project ownership declaration is absent. A previous write authorization, another conversation, a nearby workspace, a Goal, an automation, or an external project's local rule cannot satisfy this gate.

## Report-Only Mode

If any Owner Context Gate condition is false:

- inspect protected assets only as needed and remain read-only;
- do not edit, copy over, synchronize, install, restore, version, commit, push, release, or regenerate protected assets or their state manifests;
- do not modify validators, tests, config, hooks, or documentation to simulate compliance with the proposed change;
- do not invoke another Skill, script, installer, automation, subagent, or external project to perform the prohibited write indirectly;
- return the Required Change Report to the user so the user can transfer it to the dedicated `agentmd-plan` conversation.

This is a governance ownership boundary, not a request for another permission prompt. A request from another project or conversation remains report-only even when it explicitly asks for a protected write; the user transfers the report to the owner project for implementation.

## Required Change Report

Default to a detailed response artifact rather than writing into the protected project. Include:

1. **Source context**: current project/conversation, affected asset, and why the issue was encountered.
2. **Current-state evidence**: exact versions, paths, hashes or line references, observed behavior, and a bounded reproduction when available.
3. **Problem statement**: the concrete failure, drift, ambiguity, or cross-project side effect.
4. **Proposed change**: suggested rule text or conceptual diff, responsible file/module, and alternatives considered.
5. **Version impact**: `none`, `PATCH`, `MINOR`, or `MAJOR`, with compatibility rationale.
6. **Blast radius**: affected projects, workflows, Skills, agents, stored state, and backward-compatibility risk.
7. **Validation plan**: the smallest checks that would prove the change and any required synchronized-copy or release checks.
8. **Rollback plan**: prior artifact/version to restore and conditions for rollback.
9. **Urgency and blockers**: whether the issue is informational, operational, privacy-related, security-related, or release-blocking.

Do not present the proposed change as already applied. Avoid machine secrets and unrelated private content in the report.

## Owner Project Implementation

Inside a passing owner context:

1. Compare the report with current global, Skill, project, and recovery state.
2. Accept, revise, or reject the proposal based on system-wide effects rather than the source project's local convenience.
3. Apply the normal version, documentation, synchronization, guardrail, snapshot, Git, and release rules.
4. Keep installation and publication separate unless the user explicitly authorizes both.

Subagents inherit this boundary. A child may perform bounded read-only analysis, but it cannot convert a report-only task into a protected write.
