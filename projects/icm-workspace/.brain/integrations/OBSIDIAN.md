# Obsidian Integration

The local vault is `.brain/knowledge/`; open that folder as an Obsidian vault. The integration is plain Markdown and requires no plugin or network account.

## Structure

- `HOME.md` and `index.md` route the vault.
- `architecture/` stores stable system structure notes.
- `decisions/` stores durable decisions and affected paths.
- `fixes/` stores compact recurring operational fixes.
- `research/notebooklm-summaries/` stores distilled NotebookLM research notes.

Use links for stable relationships and keep notes small. Volatile status belongs only in `.brain/NOW.md`; task logs belong in ignored `work/`.

## Token discipline

Distill large NotebookLM answers into small notes with `python .brain/scripts/notebook_context.py distill ...` and link them into the vault instead of repeatedly loading long raw answers into agent context.
