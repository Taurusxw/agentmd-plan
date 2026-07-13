#!/usr/bin/env python3
"""Measure Codex rule and documentation files.

The script is intentionally dependency-free so it can be run from any Codex
session before changing AGENTS.md, project docs, or progress folders.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


VERSION_RE = re.compile(r"(?:version|版本)\s*[：:]\s*([0-9]+(?:\.[0-9]+){2})", re.I)
DATE_RE = re.compile(r"(?:date|定版日期)\s*[：:]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", re.I)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def classify_file(path: Path) -> dict[str, int | str | None]:
    content = read_text(path)
    lines = content.splitlines()
    non_empty = [line for line in lines if line.strip()]
    headings = [line for line in lines if line.lstrip().startswith("#")]
    version = VERSION_RE.search(content)
    date = DATE_RE.search(content)

    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "lines": len(lines),
        "non_empty_lines": len(non_empty),
        "headings": len(headings),
        "version": version.group(1) if version else None,
        "date": date.group(1) if date else None,
        "threshold": threshold_name(path),
        "status": threshold_status(path, len(non_empty), path.stat().st_size),
    }


def threshold_name(path: Path) -> str:
    normalized = str(path).replace("\\", "/").lower()
    name = path.name.lower()

    if name == "agents.md" and "/.codex/" in normalized:
        return "global-agents"
    if re.fullmatch(r"agents-[0-9]+(?:\.[0-9]+){2}\.md", name) and "/artifacts/" in normalized:
        return "global-agents-candidate"
    if name == "agents.md":
        return "project-agents"
    if normalized.endswith("/docs/progress.md"):
        return "progress"
    if normalized.endswith("/docs/doc_index.md"):
        return "doc-index"
    if name.startswith("architecture") or name in {"architecture.md", "knowledge_graph.md"}:
        return "architecture"
    if "round" in name and name.endswith(".md"):
        return "round"
    return "generic"


def threshold_status(path: Path, non_empty_lines: int, byte_count: int) -> str:
    kind = threshold_name(path)

    if kind in {"global-agents", "global-agents-candidate"}:
        if non_empty_lines >= 300 or byte_count >= 16 * 1024:
            return "warning: extract detailed rules to Skills or project docs"
        if non_empty_lines > 220:
            return "notice: near global AGENTS.md target range"
        return "ok"
    if kind == "project-agents" and non_empty_lines > 250:
        return "warning: move module-specific rules downward"
    if kind == "progress" and non_empty_lines > 200:
        return "warning: move details to rounds, phases, or releases"
    if kind == "doc-index" and non_empty_lines > 200:
        return "warning: index only core docs and directories"
    if kind == "architecture" and non_empty_lines > 500:
        return "warning: move module details closer to code"
    if kind == "round" and non_empty_lines > 300:
        return "warning: split into phase or archive summary"
    return "ok"


def measure_progress_dirs(root: Path) -> dict[str, int | str] | None:
    rounds_dir = root / "docs" / "progress" / "rounds"
    if not rounds_dir.exists() or not rounds_dir.is_dir():
        return None

    round_files = [path for path in rounds_dir.rglob("*.md") if path.is_file()]
    direct_files = [path for path in rounds_dir.glob("*.md") if path.is_file()]
    status = "ok"
    if len(direct_files) > 100:
        status = "warning: archive or summarize before adding more rounds"
    elif len(direct_files) > 30:
        status = "notice: organize direct round files by month"

    return {
        "path": str(rounds_dir),
        "direct_round_files": len(direct_files),
        "total_round_files": len(round_files),
        "status": status,
    }


def collect_targets(paths: list[Path]) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    dirs: list[Path] = []
    for path in paths:
        resolved = path.expanduser().resolve()
        if resolved.is_file():
            files.append(resolved)
        elif resolved.is_dir():
            dirs.append(resolved)
            for pattern in ("AGENTS.md", "docs/PROGRESS.md", "docs/DOC_INDEX.md"):
                candidate = resolved / pattern
                if candidate.is_file():
                    files.append(candidate)
        else:
            raise SystemExit(f"Path not found: {path}")
    return files, dirs


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure Codex rule and documentation files.")
    parser.add_argument("paths", nargs="+", help="Files or project directories to measure")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--strict", action="store_true", help="Fail on warning thresholds")
    args = parser.parse_args()

    files, dirs = collect_targets([Path(item) for item in args.paths])
    file_results = [classify_file(path) for path in files]
    progress_results = [result for root in dirs if (result := measure_progress_dirs(root))]
    warnings = [
        item["status"]
        for item in [*file_results, *progress_results]
        if str(item["status"]).startswith("warning:")
    ]
    payload = {
        "files": file_results,
        "progress_dirs": progress_results,
        "strict": args.strict,
        "warnings": warnings,
        "ok": not args.strict or not warnings,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["ok"] else 1

    for item in file_results:
        print(f"{item['path']}")
        print(f"  lines={item['lines']} non_empty={item['non_empty_lines']} bytes={item['bytes']}")
        print(f"  version={item['version'] or '-'} date={item['date'] or '-'}")
        print(f"  threshold={item['threshold']} status={item['status']}")
    for item in progress_results:
        print(f"{item['path']}")
        print(
            "  direct_round_files="
            f"{item['direct_round_files']} total_round_files={item['total_round_files']}"
        )
        print(f"  status={item['status']}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
