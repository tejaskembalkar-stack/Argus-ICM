# ICM Implementation Status

1. Root folder — this directory is the canonical launch root.
2. Brain folder — `.brain/` contains modular system knowledge only.
3. Root router — `AGENTS.md` is canonical; no vendor-specific router is required.
4. Model routing — `.brain/MODELS.md` plus `icm.py route` provides deterministic intent routing.
5. Five-file cap — `.brain/CONTEXT.md` plus `icm.py context set` enforces the cap.
6. Memory folder — `.brain/memory/` stores verified durable lessons.
7. Index — `.brain/INDEX.md` maps entry points and boundaries.
8. Tool contracts — `.brain/TOOLS.md` defines inputs, limits, and verification.
9. Project folders — `frontend/`, `backend/`, and `docs/` are hard edit boundaries.
10. Local context — every project area has a small `CONTEXT.md`.
11. Obsidian — `.brain/knowledge/` is a local Obsidian-compatible vault.
12. GitHub — `gh` integration guide and live status check exist; authentication is user-controlled.
13. Current state — `.brain/NOW.md` is the volatile loop-breaker.
14. Notion — on-demand API boundary is documented; credentials remain local and optional.
15. Rules — `.brain/RULES.md` defines coding, testing, and forbidden patterns.
16. Skills — `.brain/skills/` contains opt-in reusable procedures.
17. Workflows — Plan, Execute, and Review are separate passes.
18. Python scripts — `.brain/scripts/icm.py` handles deterministic validation and routing.
19. Environment — `.env.example` declares names; `.env` is ignored and never agent context.
20. Ignore rules — `.gitignore` excludes secrets, dependencies, generated files, caches, and logs.

Run `python .brain/scripts/icm.py validate` for machine-checked status. “Configured” does not mean an external account is connected.
