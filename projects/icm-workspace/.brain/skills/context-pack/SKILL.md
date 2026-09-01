---
name: context-pack
description: Use when selecting task context. Enforces a five-file pack.
---

# Context Pack

1. Read `.brain/INDEX.md` and choose the owning area.
2. Prefer the nearest `CONTEXT.md`, target implementation, focused test, and one contract/rule.
3. Run `python .brain/scripts/icm.py context set <paths...>`.
4. If selection exceeds five files, split the task rather than bypassing the cap.
5. Clear the pack after completion with `context clear`.
