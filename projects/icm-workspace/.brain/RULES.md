# Project Rules

## Before writing

- Read `AGENTS.md`, `.brain/NOW.md`, `.brain/INDEX.md`, and the nearest `CONTEXT.md`.
- Read only the additional references needed for this task; the active pack may contain at most five files total.
- Inspect existing code and tests before changing behavior.

## Code and verification

- Make the smallest coherent change; do not perform speculative refactors.
- Preserve public behavior unless the task explicitly changes it.
- Add or update focused tests for behavior changes.
- Run focused validation first, then broader checks when risk warrants it.
- Review the resulting diff or artifact before completion.

## Forbidden patterns

- Never read, print, commit, log, or send secrets to a model or external service.
- Never edit outside the selected project area without an explicit cross-area plan.
- Never load dependencies, generated assets, caches, binaries, lockfiles, or large logs without a task-specific reason.
- Never repeat the same failed approach more than twice.
- Never claim an integration is connected without a live status check.
