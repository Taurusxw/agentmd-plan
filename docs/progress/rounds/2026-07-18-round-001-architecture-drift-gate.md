# Round 001: Architecture Drift Gate

Date: `2026-07-18`
Level: `L4 release`
Target: `v27.7.0`

## Objective

Prevent repeated local patches from silently expanding production hotspots while keeping ordinary development low-token and avoiding line-count-driven over-refactoring.

## Evidence

- A high-churn browser-extension project contained 186 round records; one central background entry file appeared in 105 records and still held 37 message branches after prior successful extractions.
- Two sibling site-template modules exposed 75 exact shared function names, requiring semantic review for a shared boundary or intentional runtime isolation.
- A comparison project showed that large cohesive modules can remain appropriate, so line count cannot be a split verdict.

## Changes

- Added a concise cumulative-drift gate to the global outline.
- Added `architecture-drift.md` with event triggers, combination thresholds, boundary criteria, emergency bypass, and low-token reporting.
- Added `structure_check.py` plus unit tests.
- Updated task scaling, code governance, bilingual manuals, coverage mappings, and release records.

## Verification

- Python compilation and two unit tests pass.
- A real-project run identifies the known background hotspot and sibling duplication.
- Final strict guardrail, synchronization, privacy, Git, and release checks are recorded in `docs/progress/releases/v27.7.0/ACCEPTANCE.md`.

## Five-Pass Review

1. Coverage: mapped both new global rules to task scaling, code governance, and the new architecture reference.
2. Task flow: confirmed ordinary L1/L2 work does not scan automatically and cumulative drift upgrades only on combined evidence.
3. Signal integrity: merged round and Git evidence into one `patch_hotspot` signal so the same fact is not double-counted.
4. Validation: proved combined hotspot signals trigger review while a cohesive large file alone does not.
5. Maintainability: kept the global outline at 93 non-empty lines, routed one-level references, verified project/live Skill tree parity, and retained semantic review as the final decision point.

## Risk

Static signals cannot determine semantic ownership. Human review remains mandatory before extraction, especially for generated or serialized runtime code.
