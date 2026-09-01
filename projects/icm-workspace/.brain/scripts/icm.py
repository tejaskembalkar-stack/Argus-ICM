#!/usr/bin/env python3
"""Local, dependency-free ICM validator and context/model router."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ACTIVE = ROOT / ".brain" / "context" / "active.json"
MAX_CONTEXT_FILES = 5

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    ".brain/INDEX.md",
    ".brain/NOW.md",
    ".brain/RULES.md",
    ".brain/TOOLS.md",
    ".brain/MODELS.md",
    ".brain/CONTEXT.md",
    ".brain/ICM_STATUS.md",
    ".brain/memory/README.md",
    ".brain/knowledge/HOME.md",
    ".brain/knowledge/index.md",
    ".brain/integrations/GITHUB.md",
    ".brain/integrations/NOTION.md",
    ".brain/integrations/OBSIDIAN.md",
    ".brain/integrations/NOTEBOOKLM.md",
    ".brain/integrations/OPENROUTER.md",
    ".brain/integrations/ARGUS.md",
    ".brain/workflows/plan.md",
    ".brain/workflows/execute.md",
    ".brain/workflows/review.md",
    ".brain/workflows/swarm-plan.md",
    ".brain/workflows/swarm-execute.md",
    ".brain/workflows/swarm-review.md",
    ".brain/skills/context-pack/SKILL.md",
    ".brain/scripts/icm.py",
    ".brain/scripts/notebook_context.py",
    ".brain/scripts/swarm.py",
    ".brain/scripts/argus_gate.py",
    ".brain/swarm/ROLES.md",
    ".brain/swarm/ROUTING.md",
    ".brain/swarm/REVIEW_GATE.md",
    ".brain/swarm/COST_LIMITS.md",
    ".brain/swarm/WORKTREE_POLICY.md",
    "frontend/CONTEXT.md",
    "backend/CONTEXT.md",
    "docs/CONTEXT.md",
    "work/CONTEXT.md",
    "outputs/CONTEXT.md",
    ".env.example",
    ".gitignore",
]

FORBIDDEN_CONTEXT_NAMES = {".env", ".env.local", ".env.production", ".env.development"}
FAST_TERMS = {
    "format", "formatting", "rename", "typo", "copy edit", "reorder", "sort",
    "extract", "convert", "whitespace", "comment", "mechanical",
}
FRONTIER_TERMS = {
    "architecture", "architectural", "security", "authentication", "authorization",
    "migration", "production", "deploy", "cross-boundary", "cross boundary",
    "root cause", "race condition", "data loss", "refactor system", "threat model",
}


def relative_file(raw: str) -> Path:
    candidate = (ROOT / raw).resolve() if not Path(raw).is_absolute() else Path(raw).resolve()
    try:
        rel = candidate.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"outside repository root: {raw}") from exc
    if not candidate.is_file():
        raise ValueError(f"not an existing file: {raw}")
    if candidate.name in FORBIDDEN_CONTEXT_NAMES or candidate.name.startswith(".env."):
        if candidate.name != ".env.example":
            raise ValueError(f"secret-bearing environment file is forbidden: {raw}")
    blocked_parts = {"node_modules", ".git", "dist", "build", "coverage", "__pycache__"}
    if blocked_parts.intersection(rel.parts):
        raise ValueError(f"generated or internal path is forbidden: {raw}")
    return rel


def load_active() -> list[str]:
    if not ACTIVE.exists():
        return []
    data = json.loads(ACTIVE.read_text(encoding="utf-8"))
    files = data.get("files", [])
    if not isinstance(files, list):
        raise ValueError("active context manifest has invalid schema")
    return [str(item) for item in files]


def context_command(args: argparse.Namespace) -> int:
    if args.context_action == "set":
        if len(args.files) > MAX_CONTEXT_FILES:
            print(f"error: context pack has {len(args.files)} files; maximum is {MAX_CONTEXT_FILES}", file=sys.stderr)
            return 2
        try:
            files = [relative_file(item).as_posix() for item in args.files]
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        if len(set(files)) != len(files):
            print("error: context pack contains duplicate paths", file=sys.stderr)
            return 2
        ACTIVE.parent.mkdir(parents=True, exist_ok=True)
        ACTIVE.write_text(json.dumps({"files": files}, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"count": len(files), "maximum": MAX_CONTEXT_FILES, "files": files}, indent=2))
        return 0
    if args.context_action == "show":
        files = load_active()
        print(json.dumps({"count": len(files), "maximum": MAX_CONTEXT_FILES, "files": files}, indent=2))
        return 0
    if args.context_action == "clear":
        ACTIVE.unlink(missing_ok=True)
        print("context pack cleared")
        return 0
    raise AssertionError("unknown context action")


def route_command(task: str) -> int:
    normalized = " ".join(task.lower().split())
    frontier_hits = sorted(term for term in FRONTIER_TERMS if term in normalized)
    fast_hits = sorted(term for term in FAST_TERMS if term in normalized)
    if frontier_hits:
        tier, model_class, turns, workflow = "frontier", "frontier reasoning", 15, "plan -> execute -> review"
        reasons = frontier_hits
    elif fast_hits:
        tier, model_class, turns, workflow = "fast", "inexpensive/fast", 5, "execute -> review"
        reasons = fast_hits
    else:
        tier, model_class, turns, workflow = "standard", "balanced reasoning", 10, "execute -> review"
        reasons = ["no high-risk or purely mechanical intent marker"]
    print(json.dumps({
        "tier": tier,
        "model_class": model_class,
        "max_turns": turns,
        "workflow": workflow,
        "reasons": reasons,
        "advisory": "The host runtime must select an available model in this class.",
    }, indent=2))
    return 0


def run_status(command: list[str], cwd: Path = ROOT) -> tuple[bool, str]:
    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    text = (result.stdout or result.stderr).strip().splitlines()
    return result.returncode == 0, text[0] if text else "no output"


def status_command() -> int:
    gh_installed = shutil.which("gh") is not None
    git_installed = shutil.which("git") is not None
    gh_auth = run_status(["gh", "auth", "status"])[0] if gh_installed else False
    git_repo = run_status(["git", "rev-parse", "--is-inside-work-tree"])[0] if git_installed else False
    remote = False
    if git_repo:
        ok, output = run_status(["git", "remote"])
        remote = ok and bool(output and output != "no output")
    print(json.dumps({
        "root": str(ROOT),
        "github": {"gh_installed": gh_installed, "authenticated": gh_auth, "git_repository": git_repo, "remote_configured": remote},
        "notion": {"token_configured": bool(os.environ.get("NOTION_TOKEN")), "root_id_configured": bool(os.environ.get("NOTION_ROOT_PAGE_ID"))},
        "obsidian": {"vault_present": (ROOT / ".brain" / "knowledge" / ".obsidian").is_dir()},
        "active_context_files": len(load_active()),
    }, indent=2))
    return 0


def validate_command() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing file: {rel}")
        elif path.stat().st_size == 0:
            errors.append(f"empty file: {rel}")
    if (ROOT / "CLAUDE.md").exists():
        warnings.append("CLAUDE.md exists; AGENTS.md remains canonical")
    try:
        active = load_active()
        if len(active) > MAX_CONTEXT_FILES:
            errors.append(f"active context contains {len(active)} files")
        for rel in active:
            relative_file(rel)
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(f"invalid active context: {exc}")
    agents = ROOT / "AGENTS.md"
    if agents.exists() and "no more than five" not in agents.read_text(encoding="utf-8").lower():
        errors.append("AGENTS.md does not state the five-file cap")
    result = {"ok": not errors, "root": str(ROOT), "checked_files": len(REQUIRED_FILES), "errors": errors, "warnings": warnings}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Infinite Context Method local utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="validate the ICM scaffold")
    sub.add_parser("status", help="show local integration readiness without secrets")
    route = sub.add_parser("route", help="recommend a model tier for a task")
    route.add_argument("task")
    context = sub.add_parser("context", help="manage the active five-file context pack")
    context_sub = context.add_subparsers(dest="context_action", required=True)
    set_parser = context_sub.add_parser("set")
    set_parser.add_argument("files", nargs="*")
    context_sub.add_parser("show")
    context_sub.add_parser("clear")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "validate":
        return validate_command()
    if args.command == "status":
        return status_command()
    if args.command == "route":
        return route_command(args.task)
    if args.command == "context":
        return context_command(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
