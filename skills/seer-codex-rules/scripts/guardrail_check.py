#!/usr/bin/env python3
"""Low-token guardrail checks for the AGENTS.md and seer-codex-rules system."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path


DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
DEFAULT_GLOBAL_AGENTS = DEFAULT_CODEX_HOME / "AGENTS.md"
DEFAULT_DOWNLOADS_AGENTS = Path.home() / "Downloads" / "AGENTS.md"
DEFAULT_SKILL = DEFAULT_CODEX_HOME / "skills" / "seer-codex-rules"
DEFAULT_PROJECT = Path(os.environ.get("SEER_CODEX_RULES_PROJECT", Path.cwd()))

REQUIRED_GATE_PHRASES = [
    "seer-codex-rules",
    "必须读取并遵守",
    "最终回答必须说明",
    "未覆盖风险",
    "完成契约",
]

REQUIRED_REFERENCES = {
    "rule-governance.md",
    "low-token-guardrails.md",
    "acceptance-closure.md",
    "goal-mode-closure.md",
    "global-agents-coverage.md",
    "global-agents-rule-inventory.md",
    "task-scaling-and-context.md",
    "execution-standards.md",
    "code-change-governance.md",
    "architecture-drift.md",
    "documentation-governance.md",
    "verification-and-reporting.md",
    "project-agents-template.md",
    "rule-review-checklist.md",
}

REQUIRED_SCRIPTS = {
    "measure_rules.py",
    "guardrail_check.py",
    "snapshot_state.py",
    "structure_check.py",
}

REQUIRED_REFERENCE_PHRASES = {
    "goal-mode-closure.md": {
        "Completion Contract",
        "Frozen Criteria",
        "Required-Work Admission",
        "No-Progress Circuit Breaker",
        "`complete`",
        "All Frozen Criteria pass: mark `complete`",
        "they are not `required work`",
        "Do not create or launch another Goal automatically",
        "does not lower a platform-required blocked threshold",
    },
}

TEMPLATE_MARKERS = (
    "Structuring This Skill",
    "[TODO",
    "TODO:",
    "PLACEHOLDER:",
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def skill_files(skill_dir: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in skill_dir.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix.lower() != ".pyc"
        ),
        key=lambda path: path.relative_to(skill_dir).as_posix(),
    )


def skill_tree_sha256(skill_dir: Path) -> tuple[str | None, int]:
    if not skill_dir.is_dir():
        return None, 0
    digest = hashlib.sha256()
    files = skill_files(skill_dir)
    for path in files:
        relative = path.relative_to(skill_dir).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest().upper(), len(files)


def parse_global_metadata(text: str) -> tuple[str | None, str | None]:
    version = re.search(r"版本[：:]\s*([0-9]+(?:\.[0-9]+){2})", text)
    date = re.search(r"定版日期[：:]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    return (
        version.group(1) if version else None,
        date.group(1) if date else None,
    )


def global_size_warning(path: Path, text: str) -> str | None:
    non_empty = sum(1 for line in text.splitlines() if line.strip())
    byte_count = path.stat().st_size
    if non_empty >= 300 or byte_count >= 16 * 1024:
        return (
            "global AGENTS.md exceeds warning threshold: "
            f"non_empty={non_empty}, bytes={byte_count}"
        )
    if non_empty > 220:
        return f"global AGENTS.md is above target range: non_empty={non_empty}"
    return None


def check_global_gate(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"ok": False, "path": str(path), "missing": ["file"]}
    text = read_text(path)
    missing = [phrase for phrase in REQUIRED_GATE_PHRASES if phrase not in text]
    version, date = parse_global_metadata(text)
    warning = global_size_warning(path, text)
    return {
        "ok": not missing and bool(version) and bool(date),
        "path": str(path),
        "version": version,
        "date": date,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "non_empty_lines": sum(1 for line in text.splitlines() if line.strip()),
        "warning": warning,
        "missing_gate_phrases": missing,
    }


def check_skill(skill_dir: Path) -> dict[str, object]:
    skill_md = skill_dir / "SKILL.md"
    refs_dir = skill_dir / "references"
    scripts_dir = skill_dir / "scripts"
    if not skill_md.is_file():
        return {"ok": False, "path": str(skill_dir), "missing": ["SKILL.md"]}

    skill_text = read_text(skill_md)
    routed_refs = set(
        re.findall(r"references/([A-Za-z0-9._-]+\.md)", skill_text)
    )
    existing_refs = (
        {path.name for path in refs_dir.glob("*.md")} if refs_dir.is_dir() else set()
    )
    missing_required_refs = sorted(REQUIRED_REFERENCES - existing_refs)
    required_not_routed = sorted(REQUIRED_REFERENCES - routed_refs)
    broken_routes = sorted(routed_refs - existing_refs)
    unrouted_refs = sorted(existing_refs - routed_refs)
    existing_scripts = (
        {path.name for path in scripts_dir.glob("*.py")}
        if scripts_dir.is_dir()
        else set()
    )
    missing_scripts = sorted(REQUIRED_SCRIPTS - existing_scripts)
    has_frontmatter = skill_text.startswith("---") and "name: seer-codex-rules" in skill_text

    missing_reference_phrases: dict[str, list[str]] = {}
    for name, phrases in REQUIRED_REFERENCE_PHRASES.items():
        reference_path = refs_dir / name
        if not reference_path.is_file():
            continue
        reference_text = read_text(reference_path)
        missing_phrases = sorted(phrase for phrase in phrases if phrase not in reference_text)
        if missing_phrases:
            missing_reference_phrases[name] = missing_phrases

    residues: list[str] = []
    for path in skill_files(skill_dir):
        if path.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        text = read_text(path)
        for marker in TEMPLATE_MARKERS:
            if marker in text:
                residues.append(f"{path.relative_to(skill_dir).as_posix()}: {marker}")

    tree_hash, file_count = skill_tree_sha256(skill_dir)
    ok = all(
        (
            has_frontmatter,
            not missing_required_refs,
            not required_not_routed,
            not broken_routes,
            not unrouted_refs,
            not missing_scripts,
            not missing_reference_phrases,
            not residues,
        )
    )
    return {
        "ok": ok,
        "path": str(skill_dir),
        "frontmatter": has_frontmatter,
        "tree_sha256": tree_hash,
        "file_count": file_count,
        "missing_required_references": missing_required_refs,
        "required_references_not_routed": required_not_routed,
        "broken_reference_routes": broken_routes,
        "unrouted_references": unrouted_refs,
        "missing_scripts": missing_scripts,
        "missing_reference_phrases": missing_reference_phrases,
        "template_residue": residues,
    }


def check_project(project_dir: Path) -> dict[str, object]:
    required = [
        "README.md",
        "AGENTS.md",
        "docs/DOC_INDEX.md",
        "docs/PROGRESS.md",
        "docs/progress/README.md",
        "docs/progress/rounds",
        "artifacts",
        "LICENSE",
        "CONTRIBUTING.md",
        "SECURITY.md",
    ]
    missing = [item for item in required if not (project_dir / item).exists()]
    rounds_dir = project_dir / "docs" / "progress" / "rounds"
    direct_rounds = len(list(rounds_dir.glob("*.md"))) if rounds_dir.is_dir() else 0
    total_rounds = len(list(rounds_dir.rglob("*.md"))) if rounds_dir.is_dir() else 0
    warning = None
    if direct_rounds > 100:
        warning = "direct rounds exceed 100; archive or summarize"
    elif direct_rounds > 30:
        warning = "direct rounds exceed 30; organize by month"
    return {
        "ok": not missing,
        "path": str(project_dir),
        "missing": missing,
        "direct_round_files": direct_rounds,
        "total_round_files": total_rounds,
        "warning": warning,
    }


def check_hashes(paths: list[Path]) -> dict[str, object]:
    hashes = {str(path): sha256(path) for path in paths}
    present = [value for value in hashes.values() if value]
    return {
        "ok": bool(present) and len(set(present)) == 1 and len(present) == len(hashes),
        "hashes": hashes,
    }


def parse_inventory_source(path: Path) -> tuple[str | None, str | None]:
    if not path.is_file():
        return None, None
    text = read_text(path)
    version = re.search(r"Source global version:\s*`?([^`\s]+)`?", text)
    digest = re.search(r"Source global SHA256:\s*`?([A-Fa-f0-9]{64})`?", text)
    return (
        version.group(1) if version else None,
        digest.group(1).upper() if digest else None,
    )


def check_state(
    project_dir: Path,
    global_agents: Path,
    skill_dir: Path,
    required: bool,
) -> dict[str, object]:
    manifest_path = project_dir / "artifacts" / "current-state.json"
    if not manifest_path.is_file():
        return {
            "ok": not required,
            "path": str(manifest_path),
            "status": "required-missing" if required else "not-configured",
        }
    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError as exc:
        return {"ok": False, "path": str(manifest_path), "error": str(exc)}

    global_text = read_text(global_agents) if global_agents.is_file() else ""
    global_version, _ = parse_global_metadata(global_text)
    global_hash = sha256(global_agents)
    skill_hash, skill_count = skill_tree_sha256(skill_dir)

    global_state = manifest.get("global_agents", {})
    skill_state = manifest.get("skill", {})
    coverage_state = manifest.get("coverage", {})
    mismatches: list[str] = []

    if global_state.get("version") != global_version:
        mismatches.append("global version differs from manifest")
    if global_state.get("sha256") != global_hash:
        mismatches.append("global hash differs from manifest")

    artifact_path = Path(global_state.get("artifact_path", ""))
    artifact_hash = sha256(artifact_path)
    if not artifact_path.is_file():
        mismatches.append("canonical global artifact is missing")
    elif artifact_hash != global_hash:
        mismatches.append("canonical global artifact differs from live global")
    if global_state.get("artifact_sha256") != artifact_hash:
        mismatches.append("canonical global artifact hash differs from manifest")

    if skill_state.get("tree_sha256") != skill_hash:
        mismatches.append("live Skill tree differs from manifest")
    if skill_state.get("file_count") != skill_count:
        mismatches.append("live Skill file count differs from manifest")

    snapshot_path = Path(skill_state.get("snapshot_path", ""))
    snapshot_hash = sha256(snapshot_path)
    if not snapshot_path.is_file():
        mismatches.append("current Skill snapshot is missing")
    if skill_state.get("snapshot_sha256") != snapshot_hash:
        mismatches.append("current Skill snapshot hash differs from manifest")

    inventory_path = skill_dir / "references" / "global-agents-rule-inventory.md"
    inventory_version, inventory_hash = parse_inventory_source(inventory_path)
    if inventory_version != global_version or inventory_hash != global_hash:
        mismatches.append("coverage inventory is not anchored to the live global file")
    if coverage_state.get("source_version") != inventory_version:
        mismatches.append("coverage version differs from manifest")
    if coverage_state.get("source_sha256") != inventory_hash:
        mismatches.append("coverage hash differs from manifest")

    for relative in ("README.md", "docs/PROGRESS.md"):
        path = project_dir / relative
        if not path.is_file() or (global_version and global_version not in read_text(path)):
            mismatches.append(f"{relative} does not mention current global version")

    return {
        "ok": not mismatches,
        "path": str(manifest_path),
        "mismatches": mismatches,
        "global_version": global_version,
        "global_sha256": global_hash,
        "skill_tree_sha256": skill_hash,
        "skill_file_count": skill_count,
        "coverage_source_version": inventory_version,
        "coverage_source_sha256": inventory_hash,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check low-token guardrails.")
    parser.add_argument("--global-agents", default=str(DEFAULT_GLOBAL_AGENTS))
    parser.add_argument("--downloads-agents", default=str(DEFAULT_DOWNLOADS_AGENTS))
    parser.add_argument("--skill", default=str(DEFAULT_SKILL))
    parser.add_argument("--project", default=str(DEFAULT_PROJECT))
    parser.add_argument(
        "--require-state",
        action="store_true",
        help="Require a private current-state manifest and Skill snapshot",
    )
    parser.add_argument("--strict", action="store_true", help="Fail when warnings exist")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    global_agents = Path(args.global_agents)
    downloads_agents = Path(args.downloads_agents)
    skill_dir = Path(args.skill)
    project_dir = Path(args.project)

    payload = {
        "global_gate": check_global_gate(global_agents),
        "skill": check_skill(skill_dir),
        "project": check_project(project_dir),
        "synced_hashes": check_hashes([global_agents, downloads_agents]),
        "state": check_state(project_dir, global_agents, skill_dir, args.require_state),
    }
    warnings = [
        str(payload[key]["warning"])
        for key in ("global_gate", "project")
        if payload[key].get("warning")
    ]
    base_ok = all(
        payload[key]["ok"]
        for key in ("global_gate", "skill", "project", "synced_hashes", "state")
    )
    payload["strict"] = args.strict
    payload["warnings"] = warnings
    payload["base_ok"] = base_ok
    payload["ok"] = base_ok and (not args.strict or not warnings)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"overall: {'ok' if payload['ok'] else 'fail'}")
        if warnings:
            print("warnings:")
            for warning in warnings:
                print(f"- {warning}")
        for key in ("global_gate", "skill", "project", "synced_hashes", "state"):
            status = "ok" if payload[key]["ok"] else "fail"
            print(f"{key}: {status}")
            details = {k: v for k, v in payload[key].items() if k != "ok"}
            print(json.dumps(details, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
