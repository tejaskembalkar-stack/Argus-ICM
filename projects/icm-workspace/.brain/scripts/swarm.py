#!/usr/bin/env python3
"""Deterministic swarm planner/executor scaffold for ICM.

This script does not call remote models directly. It produces a bounded swarm
plan, stores it in SQLite, and materializes execution briefs so Hermes or other
agents can run the plan safely.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / ".brain" / "swarm" / "swarm.sqlite"
RUNS = ROOT / "work" / "swarm"
FRONTIER_TERMS = {
    "architecture", "security", "authentication", "authorization", "migration",
    "cross-boundary", "cross boundary", "production", "refactor", "data loss",
}
FAST_TERMS = {"format", "rename", "copy edit", "extract", "sort", "mechanical"}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_db(root: Path = ROOT) -> Path:
    db = root / ".brain" / "swarm" / "swarm.sqlite"
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    try:
        conn.executescript(
            """
            create table if not exists plans (
                id text primary key,
                created_at text not null,
                task text not null,
                tier text not null,
                plan_json text not null
            );
            create table if not exists executions (
                id text primary key,
                plan_id text not null,
                created_at text not null,
                run_dir text not null,
                status text not null,
                execution_json text not null
            );
            """
        )
        conn.commit()
    finally:
        conn.close()
    return db


def tier_for_task(task: str) -> tuple[str, str]:
    normalized = " ".join(task.lower().split())
    if any(term in normalized for term in FRONTIER_TERMS):
        return "frontier", "plan -> execute -> review"
    if any(term in normalized for term in FAST_TERMS):
        return "fast", "execute -> review"
    return "standard", "execute -> review"


def role_models(tier: str) -> list[dict[str, str]]:
    if tier == "frontier":
        return [
            {"role": "planner", "model_alias": "icm-plan", "purpose": "decompose task and risks"},
            {"role": "worker-1", "model_alias": "icm-worker", "purpose": "primary implementation"},
            {"role": "worker-2", "model_alias": "icm-worker", "purpose": "alternative implementation"},
            {"role": "reviewer", "model_alias": "icm-review", "purpose": "independent review and winner selection"},
        ]
    if tier == "fast":
        return [
            {"role": "worker-1", "model_alias": "icm-fast", "purpose": "single bounded mechanical pass"},
            {"role": "reviewer", "model_alias": "icm-review", "purpose": "light verification"},
        ]
    return [
        {"role": "planner", "model_alias": "icm-plan", "purpose": "light task decomposition"},
        {"role": "worker-1", "model_alias": "icm-worker", "purpose": "primary implementation"},
        {"role": "reviewer", "model_alias": "icm-review", "purpose": "review and verification"},
    ]


def build_plan(task: str, files: list[str], notebook_id: str | None = None) -> dict[str, Any]:
    tier, workflow = tier_for_task(task)
    roles = role_models(tier)
    return {
        "id": f"plan-{uuid.uuid4().hex[:12]}",
        "created_at": utc_now(),
        "task": task,
        "tier": tier,
        "workflow": workflow,
        "worker_count": len([r for r in roles if r["role"].startswith("worker-")]),
        "roles": roles,
        "context_files": files[:5],
        "gates": [
            "python .brain/scripts/icm.py validate",
            "python .brain/scripts/argus_gate.py --json",
        ],
        "notebook": {"id": notebook_id, "required": bool(notebook_id)},
        "merge_policy": "Only accept changes that pass validation, Argus gate, and human or reviewer approval.",
    }


def save_plan(root: Path, plan: dict[str, Any]) -> None:
    db = ensure_db(root)
    conn = sqlite3.connect(db)
    try:
        conn.execute(
            "insert or ignore into plans(id, created_at, task, tier, plan_json) values (?, ?, ?, ?, ?)",
            (plan["id"], plan["created_at"], plan["task"], plan["tier"], json.dumps(plan)),
        )
        conn.commit()
    finally:
        conn.close()


def worker_brief(plan: dict[str, Any], role: dict[str, str]) -> str:
    context_lines = "\n".join(f"- `{item}`" for item in plan["context_files"]) or "- none selected"
    notebook_line = f"NotebookLM notebook: `{plan['notebook']['id']}`" if plan["notebook"]["required"] else "NotebookLM: optional"
    return (
        f"# {role['role']}\n\n"
        f"- Model alias: `{role['model_alias']}`\n"
        f"- Purpose: {role['purpose']}\n"
        f"- Task: {plan['task']}\n"
        f"- Tier: {plan['tier']}\n"
        f"- Workflow: {plan['workflow']}\n"
        f"- {notebook_line}\n\n"
        f"## Context pack\n\n{context_lines}\n\n"
        f"## Gates\n\n"
        f"- `python .brain/scripts/icm.py validate`\n"
        f"- `python .brain/scripts/argus_gate.py --json`\n"
    )


def execute_plan(root: Path, plan: dict[str, Any]) -> dict[str, Any]:
    ensure_db(root)
    save_plan(root, plan)
    run_id = f"run-{uuid.uuid4().hex[:12]}"
    run_dir = root / "work" / "swarm" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    for role in plan["roles"]:
        filename = "reviewer.md" if role["role"] == "reviewer" else f"{role['role']}.md"
        (run_dir / filename).write_text(worker_brief(plan, role), encoding="utf-8")
    execution = {
        "id": run_id,
        "plan_id": plan["id"],
        "created_at": utc_now(),
        "run_dir": str(run_dir),
        "status": "materialized",
        "files": sorted(p.name for p in run_dir.iterdir()),
    }
    conn = sqlite3.connect(root / ".brain" / "swarm" / "swarm.sqlite")
    try:
        conn.execute(
            "insert into executions(id, plan_id, created_at, run_dir, status, execution_json) values (?, ?, ?, ?, ?, ?)",
            (execution["id"], execution["plan_id"], execution["created_at"], execution["run_dir"], execution["status"], json.dumps(execution)),
        )
        conn.commit()
    finally:
        conn.close()
    return execution


def status(root: Path = ROOT) -> dict[str, Any]:
    db = ensure_db(root)
    conn = sqlite3.connect(db)
    try:
        plan_count = conn.execute("select count(*) from plans").fetchone()[0]
        execution_count = conn.execute("select count(*) from executions").fetchone()[0]
        latest = conn.execute("select execution_json from executions order by created_at desc limit 1").fetchone()
    finally:
        conn.close()
    return {
        "db": str(db),
        "plan_count": plan_count,
        "execution_count": execution_count,
        "latest_execution": json.loads(latest[0]) if latest else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="ICM swarm planning and execution scaffold")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init-db")
    p = sub.add_parser("plan")
    p.add_argument("task")
    p.add_argument("files", nargs="*")
    p.add_argument("--notebook-id")
    e = sub.add_parser("execute")
    e.add_argument("task")
    e.add_argument("files", nargs="*")
    e.add_argument("--notebook-id")
    sub.add_parser("status")
    args = parser.parse_args()

    if args.command == "init-db":
        print(json.dumps({"db": str(ensure_db())}, indent=2))
        return 0
    if args.command == "plan":
        plan = build_plan(args.task, args.files, args.notebook_id)
        save_plan(ROOT, plan)
        print(json.dumps(plan, indent=2))
        return 0
    if args.command == "execute":
        plan = build_plan(args.task, args.files, args.notebook_id)
        save_plan(ROOT, plan)
        print(json.dumps({"plan": plan, "execution": execute_plan(ROOT, plan)}, indent=2))
        return 0
    if args.command == "status":
        print(json.dumps(status(), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
