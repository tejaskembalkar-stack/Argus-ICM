# ICM Agent Router

This repository root is the only working root. `AGENTS.md` is the canonical instruction file for every agent.

## Startup route

1. Read `.brain/NOW.md` for volatile task state.
2. Read `.brain/INDEX.md` to locate the smallest relevant context.
3. Select no more than five task-specific reference files; record them with `python .brain/scripts/icm.py context set ...`.
4. Read the nearest `CONTEXT.md` before changing a scoped area.
5. Read `.brain/RULES.md` before code changes and `.brain/TOOLS.md` before shell or external-tool use.

## Operating contract

- Work only inside this root unless the user explicitly authorizes another path.
- Inspect before editing and preserve unrelated changes.
- After two materially equivalent failures, stop, update `.brain/NOW.md`, and change the hypothesis.
- Update `.brain/NOW.md` after meaningful progress, failure, decision, or handoff.
- Store only verified reusable lessons in `.brain/memory/`; never store secrets or transcripts.
- Use `.brain/workflows/plan.md`, `execute.md`, and `review.md` as separate passes for risky work.
