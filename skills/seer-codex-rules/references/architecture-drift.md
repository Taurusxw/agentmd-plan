# Architecture Drift Reference

Use this reference when repeated patches may be expanding a production hotspot faster than its boundaries are being maintained. This is an event-triggered review, not a mandatory repository scan for every task.

## Trigger Conditions

Load this reference when any current condition is true:

- the same production file or module was changed in three consecutive tasks;
- it appears in at least five of the latest ten round records or recent commits;
- a file above 800 non-empty lines is about to gain another independent responsibility;
- an entry dispatcher, router, command surface, or message handler already has more than 20 branches and the patch adds another domain;
- non-trivial logic is duplicated across sibling modules;
- focused tests must mock or initialize unrelated subsystems to exercise one behavior.

Do not load this reference merely because a file is large. Generated files, data tables, cohesive controllers, parsers, and self-contained runtime payloads may be legitimately long.

## Evidence Signals

| Signal | Evidence | Meaning |
|---|---|---|
| Patch hotspot | 3 consecutive tasks or 5 of the latest 10 records/commits | Local fixes may be accumulating without a boundary decision |
| Size plus responsibility | More than 800 non-empty lines and a new independent responsibility | Navigation and ownership risk are increasing |
| Broad entry interface | More than 20 handler or case branches and a new domain | One entry point may own too many concepts |
| Sibling duplication | Repeated non-trivial functions or policy across sibling modules | A shared deep module or explicit variation boundary may be missing |
| Test coupling | One behavior requires unrelated subsystem setup | Knowledge is leaking across boundaries |

Line count, function count, and branch count are signals only. They never prove that a split is correct.

## Decision Rule

Count independent signals after excluding generated code and known intentional serialization boundaries:

- `0-1 signals`: continue the smallest complete patch. Record no architecture ceremony.
- `2 signals`: the fix may proceed, but do not add a new independent responsibility to the hotspot. State the boundary decision in the current round or final report.
- `3+ signals`: upgrade to at least L3. Define a stable boundary, promote repeated work to a phase when appropriate, and either extract the boundary now or record a scoped follow-up with owner, evidence, and stop condition.

An urgent correctness or security fix may bypass extraction once. The hotspot evidence remains active for the next non-emergency change; urgency does not reset the count.

## Boundary Review

Before extracting, identify:

1. the domain concept or technical concern that owns the behavior;
2. the smallest stable interface callers need;
3. state and dependencies that can stay private;
4. behavior tests that can protect the move;
5. whether duplication is intentional because code must be serialized or executed in isolated runtimes.

A useful extraction reduces caller knowledge, unrelated test setup, or repeated policy. Reject an extraction that only creates pass-through wrappers, moves lines without ownership, or introduces a shared utility with a wider interface than the original code.

## Low-Token Procedure

1. Run `scripts/structure_check.py <project-root>` only after a trigger fires.
2. Inspect only the top reported hotspot and directly related callers/tests.
3. Combine script evidence with the current change's responsibility and interface impact.
4. Make one decision: `patch`, `patch-with-boundary-freeze`, or `L3-boundary-work`.
5. Report one compact line: `Architecture drift: <decision>; signals: <evidence>; action: <scope>.`

The script is advisory. It can detect repeated paths, large files, broad switch surfaces, and shared function names, but it cannot determine semantic ownership or whether duplication is intentionally isolated.

## Round And Phase Interaction

Different round titles do not make repeated work independent when the same production hotspot is carrying the changes. Use file/module evidence in addition to topic names. If the hotspot spans five to eight related records, multiple days, or repeated acceptance passes, promote it to a phase and keep `PROGRESS.md` as a concise pointer.
