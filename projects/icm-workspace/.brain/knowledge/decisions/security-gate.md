# Security Gate

- Date: 2026-09-01
- Decision: Use local Argus/ECC wrappers as the pre-commit, pre-push, and pre-merge security gate.
- Reason: deterministic local scans are cheaper and more reliable than ad hoc prompt-only review.
- Alternatives considered: no gate; custom one-off secret scan only.
- Affected paths: `.brain/scripts/argus_gate.py`, `.brain/integrations/ARGUS.md`, `.brain/TOOLS.md`.

## Related

- [[../architecture/swarm]]
