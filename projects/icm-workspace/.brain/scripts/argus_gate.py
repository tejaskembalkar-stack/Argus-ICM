#!/usr/bin/env python3
"""Run Argus/ECC security gates for this ICM workspace.

The gate is local-only and secret-safe: it shells out to the cloned Argus repo,
collects machine-readable output, and fails on deterministic security findings.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARGUS = Path("C:/Users/Spectrex/Documents/GitHub/Argus")


def run(cmd: list[str], cwd: Path, timeout: int = 180) -> dict[str, Any]:
    resolved = cmd[:]
    exe = shutil.which(resolved[0]) or resolved[0]
    resolved[0] = exe
    use_shell = exe.lower().endswith((".cmd", ".bat"))
    popen_cmd: list[str] | str = subprocess.list2cmdline(resolved) if use_shell else resolved
    proc = subprocess.run(
        popen_cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        timeout=timeout,
        shell=use_shell,
    )
    return {
        "cmd": cmd,
        "cwd": str(cwd),
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def parse_json_or_none(text: str) -> Any:
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return None
    return None


def summarize_agentshield(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"ok": False, "error": "agentshield output was not JSON"}
    summary = payload.get("summary", {}) or {}
    critical = int(summary.get("critical", 0) or 0)
    high = int(summary.get("high", 0) or 0)
    medium = int(summary.get("medium", 0) or 0)
    return {
        "ok": critical == 0 and high == 0,
        "grade": (payload.get("score", {}) or {}).get("grade"),
        "numeric_score": (payload.get("score", {}) or {}).get("numericScore"),
        "critical": critical,
        "high": high,
        "medium": medium,
        "total_findings": int(summary.get("totalFindings", 0) or 0),
        "files_scanned": int(summary.get("filesScanned", 0) or 0),
        "findings": payload.get("findings", []),
    }


def summarize_ioc(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"ok": False, "error": "ioc scan output was not JSON"}
    findings = payload.get("findings", []) or []
    return {
        "ok": len(findings) == 0,
        "scanned_files": payload.get("scannedFiles", 0),
        "total_findings": len(findings),
        "findings": findings,
    }


def summarize_harness(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"ok": False, "error": "harness audit output was not JSON"}
    checks = payload.get("checks", []) or []
    failed_security = [
        check for check in checks
        if check.get("category") == "Security Guardrails" and not check.get("pass")
    ]
    return {
        "ok": True,
        "overall_score": payload.get("overall_score"),
        "max_score": payload.get("max_score"),
        "security_score": ((payload.get("categories", {}) or {}).get("Security Guardrails", {}) or {}).get("score"),
        "failed_security_guardrails": failed_security,
        "top_actions": payload.get("top_actions", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Argus security gate for the ICM workspace")
    parser.add_argument("--root", default=str(ROOT), help="Project root to scan")
    parser.add_argument("--argus", default=str(DEFAULT_ARGUS), help="Local Argus checkout")
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    argus = Path(args.argus).resolve()
    if not root.exists():
        raise SystemExit(f"root not found: {root}")
    if not argus.exists():
        raise SystemExit(f"Argus checkout not found: {argus}")

    commands = {
        "agentshield": run(
            ["npx", "--yes", "ecc-agentshield", "scan", "--path", str(root), "--format", "json"],
            cwd=root,
            timeout=240,
        ),
        "argus_ioc": run(
            ["node", "scripts/ci/scan-supply-chain-iocs.js", "--root", str(root), "--json"],
            cwd=argus,
            timeout=180,
        ),
        "argus_harness_audit": run(
            ["node", "scripts/harness-audit.js", "--root", str(root), "--format", "json"],
            cwd=argus,
            timeout=180,
        ),
    }

    result = {
        "root": str(root),
        "argus": str(argus),
        "agentshield": summarize_agentshield(parse_json_or_none(commands["agentshield"]["stdout"])),
        "argus_ioc": summarize_ioc(parse_json_or_none(commands["argus_ioc"]["stdout"])),
        "argus_harness_audit": summarize_harness(parse_json_or_none(commands["argus_harness_audit"]["stdout"])),
        "command_status": {
            name: {"returncode": data["returncode"], "stderr": data["stderr"][-1000:]}
            for name, data in commands.items()
        },
    }
    result["ok"] = (
        result["agentshield"].get("ok")
        and result["argus_ioc"].get("ok")
        and all(data["returncode"] == 0 for data in commands.values())
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Argus gate: {'PASS' if result['ok'] else 'FAIL'}")
        print(json.dumps(result, indent=2))

    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
