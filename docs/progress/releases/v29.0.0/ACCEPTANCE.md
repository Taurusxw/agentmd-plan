# v29.0.0 Acceptance

## Status

ready-for-publication

## Release Contract

- The prepared `VERSION`, release directory, global artifact, live global file, and Downloads copy use `29.0.0`; the tag and GitHub Release are created only after this staged release state is committed and pushed.
- The global artifact, live global file, and Downloads copy are byte-identical with SHA-256 `E82A3B28999BC93B6F702A06E2C345C062B908FFC85D50CAF70EF3167DEC1638`.
- The current checkout retains only the latest versioned artifact/release documents and local tag; GitHub retains prior tags/Releases, and Git commit history is not rewritten.
- The public, Codex, and Skills Manager `seer-codex-rules` trees are identical across 26 files with SHA-256 `95425F4E39BDE7C60D3985C0949FA37E5F66F1D709E005A31A2E3FBA3DC6D8C2`.
- Chinese and English manuals describe the same Agent-first, V2 capacity, role-routing, and latest-only release behavior.
- Private handoff, manifests, and recovery snapshots remain ignored and outside the public release.

## Verification Completed

- Skill creator validation, Python compilation, all 11 unit tests, portable/live router checks, strict public/Codex/Skills Manager guardrails, and strict rule measurement passed.
- A fresh prompt exposed 32 total slots; a fresh Sol/high stress session accepted 31/31 child requests, directly observed 22 running concurrently, and completed 31/31.
- Privacy, credential, tracked-risky-file, large-history-object, Markdown-link, and Git whitespace checks passed; no history object is at least 1 MiB.

## Publication Verification Pending

- After publication, verify remote `main`, exact release commit, the `v29.0.0` tag and GitHub Release, remote `VERSION`, MIT license, public visibility, `main` default branch, retained old remote tags/Releases, and absence of old local tags.
- Change this record to `completed` only after those external checks pass.

## Publication Path

The authenticated GitHub CLI account performs the user-authorized `main` push, annotated tag push, and GitHub Release publication. Cleanup is limited to old local tags and current-tree versioned documents.

## Residual Risk

Deleting old versioned Markdown from the current checkout saves only modest space because Git history retains its objects. GitHub URLs and external pins remain valid because remote tags and Releases are preserved.
