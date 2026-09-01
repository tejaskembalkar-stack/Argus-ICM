# Infinite Context Method (ICM)

A vendor-neutral, file-based second brain for coding agents. The system keeps the root prompt small, limits active context to five files, separates volatile state from durable knowledge, and validates its own structure.

## Start

Launch the agent from this directory, then have it read `AGENTS.md`.

```bash
python .brain/scripts/icm.py validate
python .brain/scripts/icm.py status
python .brain/scripts/icm.py route "refactor the authentication architecture"
python .brain/scripts/icm.py context set .brain/RULES.md backend/CONTEXT.md
python .brain/scripts/notebook_context.py status
python .brain/scripts/swarm.py status
```

`AGENTS.md` is canonical. There is intentionally no `CLAUDE.md`; add a one-line compatibility shim only if a tool requires it.

## Structure

- `.brain/` — routing, state, memory, integrations, workflows, swarm configs, and scripts
- `.brain/knowledge/` — Obsidian vault with distilled NotebookLM research notes
- `.brain/swarm/` — swarm roles, routing, review gate, worktree policy, and cost limits
- `frontend/`, `backend/`, `docs/` — bounded project areas with local context
- `work/` — ignored scratch space and swarm run artifacts
- `outputs/` — deliberate user-facing artifacts
- `.env.example` — names only; real values belong in ignored `.env`

See `.brain/ICM_STATUS.md` for the 20-component implementation map.
