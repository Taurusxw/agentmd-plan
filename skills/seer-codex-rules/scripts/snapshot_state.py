#!/usr/bin/env python3
"""Create the canonical Skill snapshot and machine-readable project state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path


DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
DEFAULT_GLOBAL_AGENTS = DEFAULT_CODEX_HOME / "AGENTS.md"
DEFAULT_SKILL = DEFAULT_CODEX_HOME / "skills" / "seer-codex-rules"
DEFAULT_PROJECT = Path(os.environ.get("SEER_CODEX_RULES_PROJECT", Path.cwd()))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def sha256(path: Path) -> str:
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


def skill_tree_sha256(skill_dir: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    files = skill_files(skill_dir)
    for path in files:
        relative = path.relative_to(skill_dir).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest().upper(), len(files)


def parse_global_metadata(text: str) -> tuple[str, str]:
    version = re.search(r"版本[：:]\s*([0-9]+(?:\.[0-9]+){2})", text)
    date = re.search(r"定版日期[：:]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    if not version or not date:
        raise SystemExit("Global AGENTS.md is missing version or date")
    return version.group(1), date.group(1)


def parse_inventory_source(path: Path) -> tuple[str, str]:
    text = read_text(path)
    version = re.search(r"Source global version:\s*`?([^`\s]+)`?", text)
    digest = re.search(r"Source global SHA256:\s*`?([A-Fa-f0-9]{64})`?", text)
    if not version or not digest:
        raise SystemExit("Coverage inventory is missing source version or SHA256")
    return version.group(1), digest.group(1).upper()


def write_snapshot(skill_dir: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in skill_files(skill_dir):
            relative = path.relative_to(skill_dir).as_posix()
            info = zipfile.ZipInfo(f"seer-codex-rules/{relative}")
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    temporary.replace(destination)


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot the live Codex rule system.")
    parser.add_argument("--global-agents", default=str(DEFAULT_GLOBAL_AGENTS))
    parser.add_argument("--skill", default=str(DEFAULT_SKILL))
    parser.add_argument("--project", default=str(DEFAULT_PROJECT))
    parser.add_argument("--write", action="store_true", help="Write snapshot and manifest")
    args = parser.parse_args()
    if not args.write:
        raise SystemExit("Refusing to write without --write")

    global_agents = Path(args.global_agents).resolve()
    skill_dir = Path(args.skill).resolve()
    project_dir = Path(args.project).resolve()
    artifacts_dir = project_dir / "artifacts"
    manifest_path = artifacts_dir / "current-state.json"
    snapshot_path = artifacts_dir / "seer-codex-rules-current.zip"

    global_text = read_text(global_agents)
    version, date = parse_global_metadata(global_text)
    global_hash = sha256(global_agents)
    canonical_artifact = artifacts_dir / f"AGENTS-{version}.md"
    if not canonical_artifact.is_file():
        raise SystemExit(f"Canonical artifact is missing: {canonical_artifact}")
    artifact_hash = sha256(canonical_artifact)
    if artifact_hash != global_hash:
        raise SystemExit("Canonical artifact does not match live global AGENTS.md")

    inventory_path = skill_dir / "references" / "global-agents-rule-inventory.md"
    source_version, source_hash = parse_inventory_source(inventory_path)
    if source_version != version or source_hash != global_hash:
        raise SystemExit("Coverage inventory is not anchored to live global AGENTS.md")

    write_snapshot(skill_dir, snapshot_path)
    tree_hash, file_count = skill_tree_sha256(skill_dir)
    payload = {
        "schema_version": 1,
        "global_agents": {
            "path": str(global_agents),
            "version": version,
            "date": date,
            "sha256": global_hash,
            "artifact_path": str(canonical_artifact),
            "artifact_sha256": artifact_hash,
        },
        "skill": {
            "path": str(skill_dir),
            "tree_sha256": tree_hash,
            "file_count": file_count,
            "snapshot_path": str(snapshot_path),
            "snapshot_sha256": sha256(snapshot_path),
        },
        "coverage": {
            "inventory_path": str(inventory_path),
            "source_version": source_version,
            "source_sha256": source_hash,
        },
    }
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    temporary = manifest_path.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(manifest_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
