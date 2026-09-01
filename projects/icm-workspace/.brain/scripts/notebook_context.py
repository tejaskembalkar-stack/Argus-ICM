#!/usr/bin/env python3
"""NotebookLM context bridge for the ICM vault.

Queries a chosen NotebookLM notebook via the authenticated CLI and can
materialize the answer as a small Obsidian note inside `.brain/knowledge/`.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / ".brain" / "knowledge"
DEFAULT_NOTEBOOK = "e85d82af-b045-4ab6-9dd8-c59481cc26e7"
DEFAULT_NOTEBOOK_TITLE = "AI Routing, Agent Skills, and Context Engineering Strategies"


def run(cmd: list[str], cwd: Path = ROOT, timeout: int = 240) -> subprocess.CompletedProcess[str]:
    resolved = cmd[:]
    exe = shutil.which(resolved[0]) or resolved[0]
    resolved[0] = exe
    use_shell = exe.lower().endswith((".cmd", ".bat"))
    popen_cmd: list[str] | str = subprocess.list2cmdline(resolved) if use_shell else resolved
    return subprocess.run(
        popen_cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        timeout=timeout,
        shell=use_shell,
        check=False,
    )


def slugify(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value or "note"


def render_note(title: str, notebook_title: str, question: str, answer: str, links: list[str] | None = None) -> str:
    wikilinks = "\n".join(f"- {item}" for item in (links or [])) or "- [[HOME]]"
    return (
        f"# {title}\n\n"
        f"## Source\n\n"
        f"- NotebookLM notebook: {notebook_title}\n"
        f"- Question: {question}\n\n"
        f"## Distilled answer\n\n{answer.strip()}\n\n"
        f"## Links\n\n{wikilinks}\n"
    )


def query_notebook(notebook_id: str, question: str) -> dict[str, Any]:
    proc = run([
        "uvx", "--from", "notebooklm-mcp-cli", "nlm", "notebook", "query", notebook_id, question, "--json"
    ])
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or f"query failed: {proc.returncode}")
    return json.loads(proc.stdout)


def status() -> dict[str, Any]:
    proc = run(["uvx", "--from", "notebooklm-mcp-cli", "nlm", "notebook", "list"])
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or f"list failed: {proc.returncode}")
    notebooks = json.loads(proc.stdout)
    current = next((n for n in notebooks if n.get("id") == DEFAULT_NOTEBOOK), None)
    return {
        "authenticated": True,
        "notebook_count": len(notebooks),
        "default_notebook": current or {"id": DEFAULT_NOTEBOOK, "title": DEFAULT_NOTEBOOK_TITLE},
    }


def distill(notebook_id: str, notebook_title: str, question: str, note_title: str, folder: str, links: list[str]) -> dict[str, Any]:
    result = query_notebook(notebook_id, question)
    note_dir = KNOWLEDGE / folder
    note_dir.mkdir(parents=True, exist_ok=True)
    path = note_dir / f"{slugify(note_title)}.md"
    content = render_note(
        title=note_title,
        notebook_title=notebook_title,
        question=question,
        answer=result.get("answer", "").strip(),
        links=links,
    )
    path.write_text(content, encoding="utf-8")
    return {"path": str(path), "question": question, "conversation_id": result.get("conversation_id")}


def main() -> int:
    parser = argparse.ArgumentParser(description="NotebookLM bridge for the ICM vault")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    q = sub.add_parser("query")
    q.add_argument("question")
    q.add_argument("--notebook-id", default=DEFAULT_NOTEBOOK)
    d = sub.add_parser("distill")
    d.add_argument("question")
    d.add_argument("note_title")
    d.add_argument("--folder", default="research/notebooklm-summaries")
    d.add_argument("--notebook-id", default=DEFAULT_NOTEBOOK)
    d.add_argument("--notebook-title", default=DEFAULT_NOTEBOOK_TITLE)
    d.add_argument("--link", action="append", default=[])
    args = parser.parse_args()

    if args.command == "status":
        print(json.dumps(status(), indent=2))
        return 0
    if args.command == "query":
        print(json.dumps(query_notebook(args.notebook_id, args.question), indent=2))
        return 0
    if args.command == "distill":
        print(json.dumps(distill(args.notebook_id, args.notebook_title, args.question, args.note_title, args.folder, args.link), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
