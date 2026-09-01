# Worktree Policy

Use isolated branches or worktrees for worker execution when real code edits begin.

Naming:

- `swarm/<task-slug>/worker-1`
- `swarm/<task-slug>/worker-2`
- `swarm/<task-slug>/review`

Do not merge directly from a worker branch without validation, Argus gate, and reviewer selection.
