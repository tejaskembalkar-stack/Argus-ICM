# Model Routing

- Date: 2026-09-01
- Decision: Use a local deterministic router to choose swarm role tiers, with OpenRouter as the preferred gateway when exposed to the runtime.
- Reason: Keeps orchestration local, model access provider-agnostic, and cost bounded.
- Alternatives considered: single-model monolith; direct provider-specific routing.
- Affected paths: `.brain/MODELS.md`, `.brain/scripts/swarm.py`, `.brain/scripts/icm.py`.

## Related

- [[../architecture/routing]]
