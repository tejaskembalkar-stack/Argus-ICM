# Swarm Execute Workflow

1. Materialize the run with `python .brain/scripts/swarm.py execute "<task>" <files...> --notebook-id <id>`.
2. Use the generated briefs under `work/swarm/<run-id>/`.
3. Keep each worker inside the assigned context pack and branch/worktree.
4. Run validation and Argus gate before any acceptance decision.
