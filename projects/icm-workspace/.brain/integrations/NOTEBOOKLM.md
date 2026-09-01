# NotebookLM Integration

NotebookLM is the preferred research and context library for lookups and synthesis. Use the authenticated CLI first.

## Verified notebook

- Default notebook ID: `e85d82af-b045-4ab6-9dd8-c59481cc26e7`
- Title: `AI Routing, Agent Skills, and Context Engineering Strategies`

## Commands

```bash
python .brain/scripts/notebook_context.py status
python .brain/scripts/notebook_context.py query "How should we route models?"
python .brain/scripts/notebook_context.py distill "How should we route models?" "OpenRouter Routing" --link [[swarm]] --link [[routing]]
```

## Boundary

Use NotebookLM for source ingestion, retrieval, and synthesis. Distill durable takeaways into small Obsidian notes; do not treat raw NotebookLM answers as permanent knowledge until distilled into the vault.
