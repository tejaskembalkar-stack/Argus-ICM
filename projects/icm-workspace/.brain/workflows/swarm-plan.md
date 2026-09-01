# Swarm Plan Workflow

1. Query NotebookLM for the smallest relevant research answer.
2. Build a bounded context pack of at most five files.
3. Run `python .brain/scripts/swarm.py plan "<task>" <files...> --notebook-id <id>`.
4. Review the generated roles, gates, and worker count before execution.
