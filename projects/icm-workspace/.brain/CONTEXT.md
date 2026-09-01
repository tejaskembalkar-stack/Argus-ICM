# Active Context Policy

A context pack is the set of task-specific reference files injected beyond the root router. It may contain at most five files.

## Selection order

1. `.brain/NOW.md`
2. nearest area `CONTEXT.md`
3. relevant rule, contract, or index entry
4. target implementation file
5. focused test or interface file

Prefer exact line ranges or summaries when a complete file is unnecessary. Never add directories, secrets, `.env`, generated output, dependencies, binaries, or raw logs.

Manage the manifest with:

```bash
python .brain/scripts/icm.py context set .brain/NOW.md backend/CONTEXT.md
python .brain/scripts/icm.py context show
python .brain/scripts/icm.py context clear
```

The manifest records paths only at `.brain/context/active.json`; it never copies file contents.
