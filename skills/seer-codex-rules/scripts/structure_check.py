#!/usr/bin/env python3
"""Report cumulative architecture-drift signals without prescribing a refactor."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


SOURCE_SUFFIXES = {".c", ".cc", ".cpp", ".cs", ".go", ".java", ".js", ".jsx", ".kt", ".mjs", ".php", ".py", ".rb", ".rs", ".ts", ".tsx", ".vue"}
EXCLUDED_DIRS = {".git", ".next", ".venv", "artifacts", "backups", "build", "coverage", "dist", "node_modules", "output", "tmp", "vendor", "venv"}
FUNCTION_PATTERNS = (
    re.compile(r"^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(", re.MULTILINE),
    re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^\n]*\)\s*=>", re.MULTILINE),
    re.compile(r"^\s*def\s+([A-Za-z_]\w*)\s*\(", re.MULTILINE),
)


def relative_text(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def source_files(root: Path, include_tests: bool) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIRS for part in relative_parts):
            continue
        lowered = relative_text(path, root).lower()
        if not include_tests and ("/test/" in f"/{lowered}/" or "/tests/" in f"/{lowered}/" or re.search(r"(?:^|/)[^/]*(?:test|spec)\.[^/]+$", lowered)):
            continue
        files.append(path)
    return sorted(files)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def file_metrics(path: Path, root: Path) -> dict[str, object]:
    content = read_text(path)
    functions: set[str] = set()
    for pattern in FUNCTION_PATTERNS:
        functions.update(pattern.findall(content))
    return {
        "path": relative_text(path, root),
        "non_empty_lines": sum(bool(line.strip()) for line in content.splitlines()),
        "handler_cases": len(re.findall(r"^\s*case\s+[^:]+:", content, re.MULTILINE)),
        "functions": sorted(functions),
    }


def recent_round_counts(root: Path, paths: list[str], limit: int) -> tuple[Counter[str], Counter[str]]:
    if limit <= 0:
        return Counter(), Counter()
    round_files = sorted(root.glob("docs/progress/rounds/**/*.md"), key=lambda item: item.as_posix())[-limit:]
    counts: Counter[str] = Counter()
    consecutive: Counter[str] = Counter()
    latest_hits: list[set[str]] = []
    for round_path in round_files:
        text = read_text(round_path).replace("\\", "/")
        hits = {path for path in paths if path in text}
        latest_hits.append(hits)
        counts.update(hits)
    for path in paths:
        for hits in reversed(latest_hits):
            if path not in hits:
                break
            consecutive[path] += 1
    return counts, consecutive


def recent_git_counts(root: Path, paths: list[str], limit: int) -> tuple[Counter[str], Counter[str]]:
    if limit <= 0:
        return Counter(), Counter()
    command = ["git", "-C", str(root), "log", f"-{limit}", "--name-only", "--pretty=format:--COMMIT--"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return Counter(), Counter()
    counts: Counter[str] = Counter()
    consecutive: Counter[str] = Counter()
    commits = result.stdout.split("--COMMIT--")
    known = set(paths)
    commit_hits: list[set[str]] = []
    for commit in commits:
        if not commit.strip():
            continue
        touched = {line.strip().replace("\\", "/") for line in commit.splitlines() if line.strip()}
        hits = touched & known
        commit_hits.append(hits)
        counts.update(hits)
    for path in paths:
        for hits in commit_hits:
            if path not in hits:
                break
            consecutive[path] += 1
    return counts, consecutive


def duplication_candidates(metrics: list[dict[str, object]]) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for index, left in enumerate(metrics):
        left_functions = set(left["functions"])
        if len(left_functions) < 10:
            continue
        left_parent = Path(str(left["path"])).parent
        for right in metrics[index + 1:]:
            if Path(str(right["path"])).parent != left_parent:
                continue
            right_functions = set(right["functions"])
            shared = left_functions & right_functions
            denominator = min(len(left_functions), len(right_functions)) or 1
            if len(shared) >= 10 and len(shared) / denominator >= 0.25:
                candidates.append({
                    "left": left["path"],
                    "right": right["path"],
                    "shared_functions": len(shared),
                    "overlap_of_smaller": round(len(shared) / denominator, 3),
                })
    return sorted(candidates, key=lambda item: (-int(item["shared_functions"]), str(item["left"]), str(item["right"])))


def analyze(root: Path, recent_rounds: int, recent_commits: int, include_tests: bool) -> dict[str, object]:
    metrics = [file_metrics(path, root) for path in source_files(root, include_tests)]
    paths = [str(item["path"]) for item in metrics]
    round_counts, consecutive = recent_round_counts(root, paths, recent_rounds)
    git_counts, git_consecutive = recent_git_counts(root, paths, recent_commits)
    duplicates = duplication_candidates(metrics)
    duplicate_paths = {str(item[key]) for item in duplicates for key in ("left", "right")}
    hotspots: list[dict[str, object]] = []
    for item in metrics:
        path = str(item["path"])
        signals: list[str] = []
        if round_counts[path] >= 5 or consecutive[path] >= 3 or git_counts[path] >= 5 or git_consecutive[path] >= 3:
            signals.append("patch_hotspot")
        if int(item["non_empty_lines"]) > 800:
            signals.append("size_signal")
        if int(item["handler_cases"]) > 20:
            signals.append("broad_interface")
        if path in duplicate_paths:
            signals.append("sibling_duplication")
        if signals:
            hotspots.append({
                "path": path,
                "non_empty_lines": item["non_empty_lines"],
                "handler_cases": item["handler_cases"],
                "recent_round_mentions": round_counts[path],
                "consecutive_round_mentions": consecutive[path],
                "recent_commit_mentions": git_counts[path],
                "consecutive_commit_mentions": git_consecutive[path],
                "signals": signals,
            })
    hotspots.sort(key=lambda item: (-len(item["signals"]), -int(item["recent_round_mentions"]), -int(item["recent_commit_mentions"]), -int(item["non_empty_lines"])))
    review_required = any(len(item["signals"]) >= 2 for item in hotspots) or bool(duplicates)
    return {
        "project": str(root),
        "source_files": len(metrics),
        "review_required": review_required,
        "hotspots": hotspots[:10],
        "duplication_candidates": duplicates[:10],
        "note": "Signals require semantic review; line count alone never mandates splitting.",
    }


def print_text(report: dict[str, object]) -> None:
    print(f"Architecture drift review: {'required' if report['review_required'] else 'not triggered'}")
    print(f"Source files scanned: {report['source_files']}")
    for item in report["hotspots"]:
        print(f"HOTSPOT {item['path']}: signals={','.join(item['signals'])}; lines={item['non_empty_lines']}; cases={item['handler_cases']}; rounds={item['recent_round_mentions']}; commits={item['recent_commit_mentions']}")
    for item in report["duplication_candidates"]:
        print(f"DUPLICATION {item['left']} <-> {item['right']}: shared_functions={item['shared_functions']}; overlap={item['overlap_of_smaller']}")
    print(report["note"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--recent-rounds", type=int, default=10)
    parser.add_argument("--recent-commits", type=int, default=10)
    parser.add_argument("--include-tests", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-review", action="store_true")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if not root.is_dir():
        parser.error(f"project directory not found: {root}")
    report = analyze(root, args.recent_rounds, args.recent_commits, args.include_tests)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else "", end="" if args.json else "")
    if not args.json:
        print_text(report)
    return 2 if args.fail_on_review and report["review_required"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
