# Swarm Roles

Keep swarms bounded. Default shape:

- `planner` — decomposes the task and identifies risks.
- `worker-1` — primary implementation path.
- `worker-2` — optional alternative implementation for frontier tasks.
- `reviewer` — independent judge that verifies gates and chooses a winner.

Do not exceed 1 planner, 2 workers, and 1 reviewer unless the user explicitly approves higher cost.
