# Swarm Routing

## Tier mapping

- `icm-fast` — formatting, extraction, rename, copy edit.
- `icm-plan` — decomposition, architecture, trade-off analysis.
- `icm-worker` — implementation and targeted fixes.
- `icm-review` — independent verification and winner selection.
- `icm-auto` — fallback when a role-specific alias is unavailable.

## Escalation

Use `frontier` tier for security, authentication, schema, deployment, or cross-boundary work. Use `standard` for bounded features and bug fixes. Use `fast` only for mechanical work with narrow validation.
