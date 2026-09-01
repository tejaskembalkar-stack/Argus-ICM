# Model Routing

Route by task risk and ambiguity, not by file size alone. Prefer NotebookLM for research-backed synthesis, Obsidian for distilled durable notes, and OpenRouter as the model gateway when available.

| Tier | Typical intent | Model class | Limits |
|---|---|---|---|
| fast | rename, formatting, isolated copy edits, deterministic extraction | inexpensive/fast (for example Haiku) | 5 turns; narrow tools |
| standard | contained feature, test writing, ordinary bug fix | balanced reasoning (for example Sonnet) | 10 turns; focused validation |
| frontier | architecture, cross-boundary refactor, security, ambiguous root-cause analysis | frontier reasoning (for example Opus) | plan first; review separately |

Escalate one tier when the task touches secrets, authentication, data loss, deployment, schema migration, or more than one project area. De-escalate only after the task is decomposed into independently verifiable mechanical steps.

## Role aliases

- `icm-fast` — cheap/fast model for mechanical work.
- `icm-plan` — planning/architecture model.
- `icm-worker` — main implementation model.
- `icm-review` — independent reviewer/judge.
- `icm-auto` — fallback gateway route.

Prefer OpenRouter as the model gateway when credentials are available to the local runtime, but keep all orchestration and routing decisions inside local ICM scripts and workflow files.

The local router is advisory and deterministic. It never sends task text to a network service.
