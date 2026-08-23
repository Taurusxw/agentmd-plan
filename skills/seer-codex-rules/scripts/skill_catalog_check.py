#!/usr/bin/env python3
"""Measure the global Codex Skill catalog and verify runtime visibility.

The checker is dependency-free. It models the user Skill discovery roots,
including top-level directory links and the bundled ``.system`` subtree, then
applies ``[[skills.config]]`` enablement overrides from ``config.toml``. An
optional runtime check verifies model-visible local Skill files, compares that
model with ``codex debug prompt-input``, and probes whether the installed CLI
selects Skills by folder or ``SKILL.md``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import tomllib
from collections import Counter
from pathlib import Path
from typing import Iterable


DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
DEFAULT_ROOTS = (DEFAULT_CODEX_HOME / "skills", Path.home() / ".agents" / "skills")
DEFAULT_CONFIG = DEFAULT_CODEX_HOME / "config.toml"
DEFAULT_DESCRIPTION_WARNING = 1024
DEFAULT_SKILL_LINE_WARNING = 500
PROMPT_OMISSION_PATTERN = re.compile(
    r"\b(?:omitted|excluded|truncated|showing\s+\d+\s+of\s+\d+|due\s+to\s+(?:token|context))\b",
    re.IGNORECASE,
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def _plain_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
        return parsed if isinstance(parsed, str) else str(parsed)
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str], list[str]]:
    """Parse the top-level scalar fields needed from YAML frontmatter.

    Skill frontmatter only needs ``name`` and ``description`` here. Supporting
    folded and literal block scalars keeps the measurement accurate without
    introducing a YAML runtime dependency.
    """

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, lines, ["missing YAML frontmatter"]
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return {}, lines, ["unterminated YAML frontmatter"]

    header = lines[1:end]
    fields: dict[str, str] = {}
    value_errors: list[str] = []
    index = 0
    while index < len(header):
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", header[index])
        if not match:
            index += 1
            continue
        key, raw_value = match.group(1), (match.group(2) or "")
        if raw_value in {"|", "|-", "|+", ">", ">-", ">+"}:
            block: list[str] = []
            index += 1
            while index < len(header):
                line = header[index]
                if line and not line[0].isspace():
                    break
                block.append(line.strip())
                index += 1
            if raw_value.startswith(">"):
                fields[key] = " ".join(part for part in block if part).strip()
            else:
                fields[key] = "\n".join(block).strip()
            continue
        if key in {"name", "description"} and raw_value.lstrip().startswith(("[", "{")):
            value_errors.append(f"{key} must be a YAML string scalar")
        fields[key] = _plain_scalar(raw_value)
        index += 1

    errors = value_errors + [
        f"missing frontmatter field: {key}"
        for key in ("name", "description")
        if not fields.get(key)
    ]
    return fields, lines[end + 1 :], errors


def parse_openai_yaml(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {
            "present": False,
            "implicit_policy": "default",
            "allow_implicit_invocation": True,
            "dependencies": False,
        }

    text = read_text(path)
    policy_match = re.search(
        r"(?:^|[,{\s])allow_implicit_invocation\s*:\s*(true|false)\b",
        text,
        re.IGNORECASE,
    )
    if policy_match:
        allowed = policy_match.group(1).lower() == "true"
        policy = "explicit-true" if allowed else "explicit-only"
    else:
        allowed = True
        policy = "default"

    dependencies = False
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^dependencies:\s*(.*)$", line)
        if not match:
            continue
        inline = match.group(1).strip()
        if inline:
            dependencies = inline not in {"[]", "{}", "null", "~"}
            break
        for nested in lines[index + 1 :]:
            if nested and not nested[0].isspace() and not nested.lstrip().startswith("#"):
                break
            stripped = nested.strip()
            if stripped and not stripped.startswith("#"):
                dependencies = True
                break
        break

    return {
        "present": True,
        "implicit_policy": policy,
        "allow_implicit_invocation": allowed,
        "dependencies": dependencies,
    }


def _candidate_dirs(root: Path) -> Iterable[Path]:
    if (root / "SKILL.md").is_file():
        yield root
        return
    if not root.is_dir():
        return
    for child in sorted(root.iterdir(), key=lambda item: item.name.casefold()):
        if child.name == ".system" and child.is_dir():
            for system_child in sorted(child.iterdir(), key=lambda item: item.name.casefold()):
                if (system_child / "SKILL.md").is_file():
                    yield system_child
        elif (child / "SKILL.md").is_file():
            # This intentionally follows a top-level directory link but never
            # recursively walks arbitrary linked trees.
            yield child


def discover_skill_dirs(roots: Iterable[Path]) -> tuple[list[Path], list[str]]:
    found: dict[str, Path] = {}
    warnings: list[str] = []
    for raw_root in roots:
        root = raw_root.expanduser().absolute()
        if not root.is_dir():
            warnings.append(f"discovery root not found: {root}")
            continue
        for path in _candidate_dirs(root):
            key = os.path.normcase(os.path.normpath(str(path.absolute())))
            found.setdefault(key, path.absolute())
    return sorted(found.values(), key=lambda item: str(item).casefold()), warnings


def inspect_skill(path: Path) -> dict[str, object]:
    skill_md = path / "SKILL.md"
    text = read_text(skill_md)
    frontmatter, body, errors = parse_frontmatter(text)
    openai = parse_openai_yaml(path / "agents" / "openai.yaml")
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    return {
        "path": str(path),
        "resolved_path": str(path.resolve()),
        "folder": path.name,
        "name": name,
        "description": description,
        "description_chars": len(description),
        "selection_metadata_chars": len(name) + len(description),
        "skill_bytes": skill_md.stat().st_size,
        "skill_lines": len(text.splitlines()),
        "body_lines": len(body),
        "folder_name_matches": bool(name) and path.name == name,
        "openai_yaml": openai,
        "errors": errors,
        "enabled": True,
        "config_override": None,
    }


def _path_keys(path: Path, base: Path | None = None) -> set[str]:
    expanded = Path(os.path.expandvars(str(path))).expanduser()
    if not expanded.is_absolute() and base is not None:
        expanded = base / expanded
    absolute = expanded.absolute()
    keys = {_literal_path_key(absolute)}
    try:
        keys.add(_literal_path_key(absolute.resolve()))
    except OSError:
        pass
    return keys


def _literal_path_key(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path.expanduser().absolute())))


def _path_identity(path: Path) -> tuple[str, str | None]:
    literal = _literal_path_key(path)
    try:
        resolved = _literal_path_key(path.resolve())
    except OSError:
        resolved = None
    return literal, resolved


def load_skill_overrides(config_path: Path | None) -> tuple[list[dict[str, object]], list[str], str]:
    if config_path is None:
        return [], [], "not-requested"
    config_path = config_path.expanduser().absolute()
    if not config_path.is_file():
        return [], [], "missing"
    try:
        with config_path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        return [], [f"cannot parse config: {error}"], "invalid"

    skills = data.get("skills", {})
    raw_items = skills.get("config", []) if isinstance(skills, dict) else []
    if not isinstance(raw_items, list):
        return [], ["skills.config must be an array of tables"], "invalid"

    overrides: list[dict[str, object]] = []
    errors: list[str] = []
    for index, item in enumerate(raw_items):
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("enabled"), bool):
            errors.append(f"invalid skills.config entry at index {index}")
            continue
        configured_path = Path(item["path"])
        overrides.append(
            {
                "index": index,
                "path": str(configured_path),
                "enabled": item["enabled"],
                "keys": _path_keys(configured_path, config_path.parent),
                "matches": [],
            }
        )
    return overrides, errors, "loaded"


def apply_overrides(
    entries: list[dict[str, object]],
    overrides: list[dict[str, object]],
    config_path_mode: str,
) -> None:
    for entry in entries:
        folder = Path(str(entry["path"]))
        candidate_paths = {
            "skill-file": (folder / "SKILL.md",),
            "folder": (folder,),
            "either": (folder, folder / "SKILL.md"),
        }[config_path_mode]
        entry_keys = set().union(*(_path_keys(path) for path in candidate_paths))
        matched = [override for override in overrides if entry_keys & set(override["keys"])]
        if not matched:
            continue
        chosen = matched[-1]
        entry["enabled"] = bool(chosen["enabled"])
        entry["config_override"] = {"index": chosen["index"], "path": chosen["path"], "enabled": chosen["enabled"]}
        for override in matched:
            override["matches"].append(str(entry["path"]))


def summarize(entries: list[dict[str, object]], description_warning: int, skill_line_warning: int) -> dict[str, object]:
    names = [str(entry["name"]) for entry in entries if entry["name"]]
    counts = Counter(names)
    duplicates = {
        name: [str(entry["path"]) for entry in entries if entry["name"] == name]
        for name, count in sorted(counts.items())
        if count > 1
    }
    return {
        "entries": len(entries),
        "named_entries": len(names),
        "unique_name_count": len(counts),
        "unique_names": sorted(counts),
        "duplicate_name_count": len(duplicates),
        "duplicate_entry_excess": sum(count - 1 for count in counts.values() if count > 1),
        "duplicate_names": duplicates,
        "description_chars": sum(int(entry["description_chars"]) for entry in entries),
        "total_metadata_chars": sum(int(entry["selection_metadata_chars"]) for entry in entries),
        "selection_metadata_chars": sum(
            int(entry["selection_metadata_chars"])
            for entry in entries
            if entry["openai_yaml"]["allow_implicit_invocation"]
        ),
        "skill_bytes": sum(int(entry["skill_bytes"]) for entry in entries),
        "openai_yaml_entries": sum(bool(entry["openai_yaml"]["present"]) for entry in entries),
        "explicit_only_entries": sorted(
            str(entry["name"] or entry["folder"])
            for entry in entries
            if entry["openai_yaml"]["implicit_policy"] == "explicit-only"
        ),
        "dependency_entries": sorted(
            str(entry["name"] or entry["folder"])
            for entry in entries
            if entry["openai_yaml"]["dependencies"]
        ),
        "description_warnings": sorted(
            {str(entry["name"] or entry["folder"]): int(entry["description_chars"]) for entry in entries if int(entry["description_chars"]) > description_warning}.items()
        ),
        "skill_line_warnings": sorted(
            {str(entry["name"] or entry["folder"]): int(entry["skill_lines"]) for entry in entries if int(entry["skill_lines"]) > skill_line_warning}.items()
        ),
        "folder_name_mismatches": sorted(str(entry["path"]) for entry in entries if entry["name"] and not entry["folder_name_matches"]),
        "entry_errors": [
            {"path": str(entry["path"]), "errors": list(entry["errors"])}
            for entry in entries
            if entry["errors"]
        ],
    }


def analyze_catalog(
    roots: Iterable[Path],
    config_path: Path | None,
    description_warning: int = DEFAULT_DESCRIPTION_WARNING,
    skill_line_warning: int = DEFAULT_SKILL_LINE_WARNING,
    config_path_mode: str = "skill-file",
) -> dict[str, object]:
    skill_dirs, root_warnings = discover_skill_dirs(roots)
    entries = [inspect_skill(path) for path in skill_dirs]
    overrides, config_errors, config_status = load_skill_overrides(config_path)
    apply_overrides(entries, overrides, config_path_mode)
    effective_entries = [entry for entry in entries if entry["enabled"]]
    raw = summarize(entries, description_warning, skill_line_warning)
    effective = summarize(effective_entries, description_warning, skill_line_warning)

    raw_names = set(raw["unique_names"])
    effective_names = set(effective["unique_names"])
    removed_names = sorted(raw_names - effective_names)
    structural_deduplication = all(
        (
            int(raw["duplicate_entry_excess"]) > 0,
            int(effective["duplicate_entry_excess"]) == 0,
            int(raw["entries"]) > int(effective["entries"]),
            int(raw["selection_metadata_chars"]) > int(effective["selection_metadata_chars"]),
            not removed_names,
        )
    )
    effect = {
        "disabled_entries": len(entries) - len(effective_entries),
        "entry_reduction": int(raw["entries"]) - int(effective["entries"]),
        "duplicate_excess_reduction": int(raw["duplicate_entry_excess"]) - int(effective["duplicate_entry_excess"]),
        "metadata_chars_reduction": int(raw["selection_metadata_chars"]) - int(effective["selection_metadata_chars"]),
        "capability_names_preserved": not removed_names,
        "removed_capability_names": removed_names,
        "structural_deduplication": structural_deduplication,
        "positive_deduplication": False,
        "positive_evidence": "live-prompt-check-not-run",
    }
    stale_overrides = [
        {"index": override["index"], "path": override["path"], "enabled": override["enabled"]}
        for override in overrides
        if not override["matches"]
    ]
    ok = not config_errors and not raw["entry_errors"] and not removed_names
    return {
        "ok": ok,
        "roots": [str(Path(root).expanduser().absolute()) for root in roots],
        "config": {
            "path": str(config_path.expanduser().absolute()) if config_path is not None else None,
            "status": config_status,
            "match_mode": config_path_mode,
            "entries": len(overrides),
            "matched_disabled_paths": sorted(
                str(override["path"])
                for override in overrides
                if not override["enabled"] and override["matches"]
            ),
            "stale_entries": stale_overrides,
            "errors": config_errors,
        },
        "root_warnings": root_warnings,
        "raw": raw,
        "effective": effective,
        "configuration_effect": effect,
        "entries": entries,
    }


def _strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _strings(nested)


def _prompt_skill_roots(section: str) -> dict[str, str]:
    match = re.search(r"### Skill roots\s*\n([\s\S]*?)(?=\n### |\Z)", section)
    if match is None:
        return {}
    roots: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.startswith("- "):
            continue
        alias, separator, value = line[2:].partition(" = ")
        alias = alias.strip().strip("`")
        value = value.strip().strip("`")
        if separator and alias and value:
            roots[alias] = value
    return roots


def _resolve_prompt_file(file_value: str, roots: dict[str, str]) -> str | None:
    portable = file_value.replace("\\", "/")
    alias, separator, remainder = portable.partition("/")
    if separator and alias in roots:
        candidate = Path(os.path.expandvars(roots[alias])).expanduser()
        candidate = candidate.joinpath(*(part for part in remainder.split("/") if part))
    else:
        candidate = Path(os.path.expandvars(file_value)).expanduser()
        if not candidate.is_absolute():
            return None
    return str(candidate.absolute())


def prompt_catalog_from_json(text: str) -> dict[str, object]:
    payload = json.loads(text)
    skills_text = next((item for item in _strings(payload) if "<skills_instructions>" in item), None)
    if skills_text is None:
        raise ValueError("model-visible skills instructions not found")
    section_match = re.search(r"<skills_instructions>[\s\S]*?</skills_instructions>", skills_text)
    if section_match is None:
        raise ValueError("skills instruction section is incomplete")
    section = section_match.group(0)
    catalog_match = re.search(r"### Available skills[\s\S]*?</skills_instructions>", section)
    if catalog_match is None:
        raise ValueError("available Skill catalog not found")
    catalog = catalog_match.group(0)
    skill_roots = _prompt_skill_roots(section)
    entry_lines = [line for line in catalog.splitlines() if line.startswith("- ") and "(file:" in line]
    entries: list[dict[str, str]] = []
    for line in entry_lines:
        head, separator, file_value = line[2:].rpartition(" (file: ")
        if not separator or not file_value.endswith(")"):
            continue
        name, description_separator, description = head.partition(": ")
        if not description_separator:
            continue
        entries.append(
            {
                "name": name,
                "description": description,
                "file": file_value[:-1],
                "resolved_file": _resolve_prompt_file(file_value[:-1], skill_roots),
                "line": line,
            }
        )
    names = [entry["name"] for entry in entries]
    name_counts = Counter(names)
    omission_warnings = [
        line.strip()
        for line in catalog.splitlines()
        if not line.startswith("- ") and PROMPT_OMISSION_PATTERN.search(line)
    ]
    return {
        "section_chars": len(section),
        "catalog_chars": len(catalog),
        "file_entries": len(entries),
        "entry_line_chars": sum(len(line) for line in entry_lines),
        "unique_name_count": len(name_counts),
        "duplicate_name_excess": sum(count - 1 for count in name_counts.values() if count > 1),
        "names": names,
        "entries": entries,
        "skill_roots": skill_roots,
        "omission_warnings": omission_warnings,
    }


def prompt_metrics_from_json(text: str) -> dict[str, int]:
    catalog = prompt_catalog_from_json(text)
    return {
        key: int(catalog[key])
        for key in ("section_chars", "catalog_chars", "file_entries", "entry_line_chars")
    }


def prompt_file_health(prompt_entries: list[dict[str, object]]) -> dict[str, object]:
    missing_files: list[str] = []
    unresolved_files: list[str] = []
    resolved_entries = 0
    existing_entries = 0
    for entry in prompt_entries:
        resolved_file = entry.get("resolved_file")
        if not resolved_file:
            unresolved_files.append(str(entry.get("file", "")))
            continue
        resolved_entries += 1
        path = Path(str(resolved_file))
        if path.is_file():
            existing_entries += 1
        else:
            missing_files.append(str(path))

    positive = not missing_files
    return {
        "status": "passed" if positive else "failed",
        "positive": positive,
        "prompt_entries": len(prompt_entries),
        "resolved_entries": resolved_entries,
        "existing_entries": existing_entries,
        "missing_files": sorted(set(missing_files)),
        "unresolved_files": sorted(set(unresolved_files)),
    }


def _codex_command_prefix(codex_command: str) -> list[str] | None:
    requested = Path(codex_command).expanduser()
    executable = str(requested.absolute()) if requested.is_file() else shutil.which(codex_command)
    if executable is None:
        return None
    if Path(executable).suffix.casefold() == ".ps1":
        powershell = shutil.which("pwsh") or shutil.which("powershell")
        if powershell is None:
            return None
        return [powershell, "-NoProfile", "-File", executable]
    return [executable]


def _render_prompt_catalog(
    command_prefix: list[str],
    probe_dir: Path,
    extra_config: str | None = None,
) -> dict[str, object]:
    command = [*command_prefix, "-C", str(probe_dir)]
    if extra_config is not None:
        command.extend(("-c", extra_config))
    command.extend(("debug", "prompt-input", "skill-catalog-probe"))
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"Codex prompt renderer exited {result.returncode}")
    return prompt_catalog_from_json(result.stdout)


def compare_prompt_metrics(
    configured: dict[str, int],
    enabled_control: dict[str, int],
    expected_entry_reduction: int,
) -> dict[str, object]:
    reductions = {
        "file_entries": enabled_control["file_entries"] - configured["file_entries"],
        "section_chars": enabled_control["section_chars"] - configured["section_chars"],
        "catalog_chars": enabled_control["catalog_chars"] - configured["catalog_chars"],
        "entry_line_chars": enabled_control["entry_line_chars"] - configured["entry_line_chars"],
    }
    positive = all(
        (
            expected_entry_reduction > 0,
            reductions["file_entries"] == expected_entry_reduction,
            reductions["section_chars"] > 0,
            reductions["catalog_chars"] > 0,
            reductions["entry_line_chars"] > 0,
        )
    )
    return {
        "status": "passed" if positive else "failed",
        "positive": positive,
        "configured": configured,
        "enabled_control": enabled_control,
        "reductions": reductions,
    }


def live_prompt_check(
    disabled_paths: list[str],
    expected_entry_reduction: int,
    probe_dir: Path,
    codex_command: str,
) -> dict[str, object]:
    if not disabled_paths:
        return {"status": "not-applicable", "positive": False, "reason": "no matched disabled Skill paths"}
    command_prefix = _codex_command_prefix(codex_command)
    if command_prefix is None:
        return {"status": "unavailable", "positive": False, "reason": f"Codex command not found: {codex_command}"}

    probe_dir = probe_dir.expanduser().absolute()
    if not probe_dir.is_dir():
        return {"status": "unavailable", "positive": False, "reason": f"probe directory not found: {probe_dir}"}
    enabled_items = ",".join(
        "{path=" + json.dumps(path, ensure_ascii=False) + ",enabled=true}"
        for path in disabled_paths
    )
    control_override = f"skills.config=[{enabled_items}]"

    try:
        configured_catalog = _render_prompt_catalog(command_prefix, probe_dir)
        control_catalog = _render_prompt_catalog(command_prefix, probe_dir, control_override)
        configured = {
            key: int(configured_catalog[key])
            for key in ("section_chars", "catalog_chars", "file_entries", "entry_line_chars")
        }
        enabled_control = {
            key: int(control_catalog[key])
            for key in ("section_chars", "catalog_chars", "file_entries", "entry_line_chars")
        }
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        return {"status": "error", "positive": False, "reason": str(error)}
    return compare_prompt_metrics(configured, enabled_control, expected_entry_reduction)


def _description_state(source: str, visible: str) -> str:
    if not visible:
        return "empty"
    if visible == source:
        return "exact"
    if source.startswith(visible):
        return "shortened"
    return "mismatch"


def _runtime_path_visibility(
    expected_entries: list[dict[str, object]],
    prompt_entries: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    source_entries = [entry for entry in expected_entries if entry.get("path")]
    prompt_paths: list[dict[str, object]] = []
    unresolved_prompt_files: list[str] = []
    for index, prompt_entry in enumerate(prompt_entries):
        resolved_file = prompt_entry.get("resolved_file")
        if not resolved_file:
            unresolved_prompt_files.append(str(prompt_entry.get("file", "")))
            continue
        literal, resolved = _path_identity(Path(str(resolved_file)))
        prompt_paths.append(
            {
                "index": index,
                "entry": prompt_entry,
                "literal": literal,
                "resolved": resolved,
            }
        )

    available = bool(expected_entries) and len(source_entries) == len(expected_entries) and bool(prompt_paths)
    if not available:
        return (
            {
                "status": "unavailable",
                "available": False,
                "expected_implicit_entries": len(expected_entries),
                "visible_expected_entries": 0,
                "reason": "source or prompt path provenance is unavailable",
                "prompt_resolved_entries": len(prompt_paths),
                "prompt_unresolved_files": sorted(set(unresolved_prompt_files)),
            },
            [],
        )

    missing_paths: list[str] = []
    ambiguous_matches: list[dict[str, object]] = []
    matched_prompt_indexes: set[int] = set()
    matched_by_literal = 0
    matched_by_resolved = 0
    records: list[dict[str, object]] = []
    descriptions_by_name: dict[str, set[str]] = {}

    for source_entry in source_entries:
        source_file = Path(str(source_entry["path"])) / "SKILL.md"
        source_literal, source_resolved = _path_identity(source_file)
        matches = [item for item in prompt_paths if item["literal"] == source_literal]
        match_mode = "literal"
        if not matches and source_resolved is not None:
            matches = [item for item in prompt_paths if item["resolved"] == source_resolved]
            match_mode = "resolved"
        if not matches:
            missing_paths.append(str(source_file))
            continue
        if len(matches) > 1:
            ambiguous_matches.append(
                {
                    "source_path": str(source_file),
                    "prompt_files": sorted(
                        str(item["entry"].get("file", "")) for item in matches
                    ),
                }
            )
        selected = max(
            matches,
            key=lambda item: len(" ".join(str(item["entry"].get("description", "")).split())),
        )
        matched_prompt_indexes.update(int(item["index"]) for item in matches)
        if match_mode == "literal":
            matched_by_literal += 1
        else:
            matched_by_resolved += 1

        source = " ".join(str(source_entry["description"]).split())
        visible = " ".join(str(selected["entry"].get("description", "")).split())
        status = _description_state(source, visible)
        lost_chars = max(len(source) - len(visible), 0) if status != "mismatch" else len(source)
        retained = len(visible) / len(source) if source else 1.0
        name = str(source_entry["name"])
        descriptions_by_name.setdefault(name, set()).add(source)
        records.append(
            {
                "name": name,
                "path": str(source_entry["path"]),
                "prompt_file": str(selected["entry"].get("file", "")),
                "match_mode": match_mode,
                "status": status,
                "source_chars": len(source),
                "visible_chars": len(visible),
                "lost_chars": lost_chars,
                "retention_ratio": round(retained, 4),
                "lost_preview": (
                    source[len(visible) : len(visible) + 120]
                    if status == "shortened"
                    else source[:120] if status in {"empty", "mismatch"} else ""
                ),
                "visible_preview": visible[:120] if status == "mismatch" else "",
                "_source": source,
                "_visible": visible,
            }
        )

    positive = not missing_paths and not ambiguous_matches
    public_records = [
        {key: value for key, value in record.items() if not key.startswith("_")}
        for record in records
    ]
    return (
        {
            "status": "passed" if positive else "failed",
            "available": True,
            "expected_implicit_entries": len(expected_entries),
            "visible_expected_entries": len(records),
            "unexpected_missing_paths": sorted(missing_paths),
            "ambiguous_prompt_matches": ambiguous_matches,
            "matched_prompt_entries": len(matched_prompt_indexes),
            "matched_by_literal": matched_by_literal,
            "matched_by_resolved": matched_by_resolved,
            "prompt_resolved_entries": len(prompt_paths),
            "prompt_unresolved_files": sorted(set(unresolved_prompt_files)),
            "divergent_duplicate_names": sorted(
                name for name, descriptions in descriptions_by_name.items() if len(descriptions) > 1
            ),
            "entries": public_records,
        },
        records,
    )


def compare_runtime_visibility(
    entries: list[dict[str, object]],
    catalog: dict[str, object],
) -> dict[str, object]:
    expected_entries = [
        entry
        for entry in entries
        if entry["enabled"]
        and entry["name"]
        and entry["openai_yaml"]["allow_implicit_invocation"]
    ]
    expected_names = {str(entry["name"]) for entry in expected_entries}
    explicit_only_names = {
        str(entry["name"])
        for entry in entries
        if entry["enabled"]
        and entry["name"]
        and not entry["openai_yaml"]["allow_implicit_invocation"]
    }
    visible_names = set(str(name) for name in catalog["names"])
    missing_names = sorted(expected_names - visible_names)
    omission_warnings = list(catalog["omission_warnings"])
    path_visibility, path_records = _runtime_path_visibility(
        expected_entries,
        list(catalog["entries"]),
    )

    exact_names: list[str] = []
    shortened_names: list[str] = []
    empty_names: list[str] = []
    mismatch_names: list[str] = []
    ambiguous_names: list[str] = []
    source_description_chars = 0
    visible_description_chars = 0
    loss_ranking: list[dict[str, object]] = []
    if path_visibility["available"]:
        records_by_name: dict[str, list[dict[str, object]]] = {}
        for record in path_records:
            records_by_name.setdefault(str(record["name"]), []).append(record)
        for name in sorted(expected_names & visible_names):
            named_records = records_by_name.get(name, [])
            if not named_records:
                ambiguous_names.append(name)
                continue
            worst = min(
                named_records,
                key=lambda record: (
                    float(record["retention_ratio"]),
                    -int(record["lost_chars"]),
                    str(record["path"]),
                ),
            )
            statuses = {str(record["status"]) for record in named_records}
            source_description_chars += int(worst["source_chars"])
            visible_description_chars += int(worst["visible_chars"])
            if "mismatch" in statuses:
                mismatch_names.append(name)
            elif "empty" in statuses:
                empty_names.append(name)
            elif "shortened" in statuses:
                shortened_names.append(name)
            else:
                exact_names.append(name)
            if str(worst["status"]) != "exact":
                loss_ranking.append(
                    {key: value for key, value in worst.items() if not key.startswith("_")}
                )
        loss_ranking.sort(
            key=lambda record: (
                float(record["retention_ratio"]),
                -int(record["lost_chars"]),
                str(record["name"]).casefold(),
            )
        )
    else:
        source_descriptions: dict[str, set[str]] = {}
        for entry in expected_entries:
            name = str(entry["name"])
            normalized = " ".join(str(entry["description"]).split())
            source_descriptions.setdefault(name, set()).add(normalized)
        visible_descriptions: dict[str, list[str]] = {}
        for prompt_entry in catalog["entries"]:
            name = str(prompt_entry["name"])
            if name in expected_names:
                visible_descriptions.setdefault(name, []).append(
                    " ".join(str(prompt_entry["description"]).split())
                )
        for name in sorted(expected_names & visible_names):
            variants = source_descriptions.get(name, set())
            shown = visible_descriptions.get(name, [])
            if len(variants) != 1:
                ambiguous_names.append(name)
                continue
            source = next(iter(variants))
            visible = max(shown, key=len, default="")
            source_description_chars += len(source)
            visible_description_chars += len(visible)
            status = _description_state(source, visible)
            if status == "empty":
                empty_names.append(name)
            elif status == "exact":
                exact_names.append(name)
            elif status == "shortened":
                shortened_names.append(name)
            else:
                mismatch_names.append(name)

    retention_ratio = (
        visible_description_chars / source_description_chars
        if source_description_chars
        else 1.0
    )
    positive = not any((missing_names, omission_warnings, empty_names, mismatch_names))
    if path_visibility["available"] and path_visibility["status"] != "passed":
        positive = False
    return {
        "status": "passed" if positive else "failed",
        "positive": positive,
        "expected_implicit_names": len(expected_names),
        "visible_expected_names": len(expected_names & visible_names),
        "unexpected_missing_names": missing_names,
        "explicit_only_names": sorted(explicit_only_names),
        "explicit_only_not_listed": sorted(explicit_only_names - visible_names),
        "prompt_unique_names": int(catalog["unique_name_count"]),
        "prompt_file_entries": int(catalog["file_entries"]),
        "prompt_duplicate_name_excess": int(catalog["duplicate_name_excess"]),
        "section_chars": int(catalog["section_chars"]),
        "catalog_chars": int(catalog["catalog_chars"]),
        "omission_warnings": omission_warnings,
        "path_visibility": path_visibility,
        "description_visibility": {
            "exact_names": exact_names,
            "shortened_names": shortened_names,
            "empty_names": empty_names,
            "mismatch_names": mismatch_names,
            "ambiguous_names": ambiguous_names,
            "source_chars": source_description_chars,
            "visible_chars": visible_description_chars,
            "retention_ratio": round(retention_ratio, 4),
            "loss_ranking": loss_ranking,
        },
    }


def classify_selector_mode(
    target_name: str,
    baseline: dict[str, object],
    skill_file_disabled: dict[str, object],
    folder_disabled: dict[str, object],
) -> dict[str, object]:
    baseline_count = list(baseline["names"]).count(target_name)
    file_count = list(skill_file_disabled["names"]).count(target_name)
    folder_count = list(folder_disabled["names"]).count(target_name)
    file_matches = baseline_count == 1 and file_count == 0
    folder_matches = baseline_count == 1 and folder_count == 0
    if file_matches and folder_matches:
        mode = "either"
    elif file_matches:
        mode = "skill-file"
    elif folder_matches:
        mode = "folder"
    else:
        mode = "neither"
    positive = mode != "neither"
    return {
        "status": "passed" if positive else "failed",
        "positive": positive,
        "target_name": target_name,
        "detected_mode": mode,
        "target_counts": {
            "baseline": baseline_count,
            "skill_file_disabled": file_count,
            "folder_disabled": folder_count,
        },
        "file_entry_counts": {
            "baseline": int(baseline["file_entries"]),
            "skill_file_disabled": int(skill_file_disabled["file_entries"]),
            "folder_disabled": int(folder_disabled["file_entries"]),
        },
    }


def refresh_runtime_entries(
    entries: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    refreshed: list[dict[str, object]] = []
    changed_entries: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    compared_fields = ("name", "description")
    for entry in entries:
        path = Path(str(entry["path"]))
        try:
            current = inspect_skill(path)
        except OSError as error:
            refreshed.append(entry)
            errors.append({"path": str(path), "error": str(error)})
            continue
        current["enabled"] = entry["enabled"]
        current["config_override"] = entry["config_override"]
        changed_fields = [field for field in compared_fields if current[field] != entry[field]]
        if current["openai_yaml"] != entry["openai_yaml"]:
            changed_fields.append("openai_yaml")
        if changed_fields:
            changed_entries.append(
                {
                    "path": str(path),
                    "name": str(current["name"] or entry["name"]),
                    "fields": changed_fields,
                }
            )
        refreshed.append(current)
    positive = not errors
    return refreshed, {
        "status": "passed" if positive else "failed",
        "positive": positive,
        "refreshed_entries": len(refreshed),
        "changed_entries": changed_entries,
        "errors": errors,
    }


def runtime_catalog_check(
    entries: list[dict[str, object]],
    probe_dir: Path,
    codex_command: str,
) -> dict[str, object]:
    command_prefix = _codex_command_prefix(codex_command)
    if command_prefix is None:
        return {"status": "unavailable", "positive": False, "reason": f"Codex command not found: {codex_command}"}
    probe_dir = probe_dir.expanduser().absolute()
    if not probe_dir.is_dir():
        return {"status": "unavailable", "positive": False, "reason": f"probe directory not found: {probe_dir}"}

    try:
        version_result = subprocess.run(
            [*command_prefix, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        version = version_result.stdout.strip() if version_result.returncode == 0 else "unknown"
        baseline = _render_prompt_catalog(command_prefix, probe_dir)
        prompt_files = prompt_file_health(list(baseline["entries"]))
        runtime_entries, source_refresh = refresh_runtime_entries(entries)
        visibility = compare_runtime_visibility(runtime_entries, baseline)

        name_counts = Counter(
            str(entry["name"])
            for entry in runtime_entries
            if entry["enabled"]
            and entry["name"]
            and entry["openai_yaml"]["allow_implicit_invocation"]
        )
        visible_counts = Counter(str(name) for name in baseline["names"])
        candidates = [
            entry
            for entry in runtime_entries
            if entry["enabled"]
            and entry["name"]
            and entry["openai_yaml"]["allow_implicit_invocation"]
            and name_counts[str(entry["name"])] == 1
            and visible_counts[str(entry["name"])] == 1
        ]
        candidates.sort(
            key=lambda entry: (
                str(entry["name"]) != "seer-codex-rules",
                str(entry["name"]).casefold(),
            )
        )
        if not candidates:
            selector = {
                "status": "unavailable",
                "positive": False,
                "reason": "no unique, implicitly visible Skill is available for a selector probe",
            }
        else:
            target = candidates[0]
            folder = Path(str(target["path"]))
            skill_file_config = (
                "skills.config=[{path="
                + json.dumps(str(folder / "SKILL.md"), ensure_ascii=False)
                + ",enabled=false}]"
            )
            folder_config = (
                "skills.config=[{path="
                + json.dumps(str(folder), ensure_ascii=False)
                + ",enabled=false}]"
            )
            skill_file_disabled = _render_prompt_catalog(command_prefix, probe_dir, skill_file_config)
            folder_disabled = _render_prompt_catalog(command_prefix, probe_dir, folder_config)
            selector = classify_selector_mode(
                str(target["name"]),
                baseline,
                skill_file_disabled,
                folder_disabled,
            )
            selector["target_path"] = str(folder)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        return {"status": "error", "positive": False, "reason": str(error)}

    positive = bool(
        source_refresh["positive"]
        and prompt_files["positive"]
        and visibility["positive"]
        and selector["positive"]
    )
    return {
        "status": "passed" if positive else "failed",
        "positive": positive,
        "codex_version": version,
        "source_refresh": source_refresh,
        "prompt_files": prompt_files,
        "visibility": visibility,
        "selector": selector,
    }


def print_text(report: dict[str, object]) -> None:
    raw = report["raw"]
    effective = report["effective"]
    effect = report["configuration_effect"]
    print(f"catalog: {'ok' if report['ok'] else 'fail'}")
    print(
        "raw: "
        f"entries={raw['entries']} unique_names={raw['unique_name_count']} "
        f"duplicate_excess={raw['duplicate_entry_excess']} metadata_chars={raw['selection_metadata_chars']}"
    )
    print(
        "effective: "
        f"entries={effective['entries']} unique_names={effective['unique_name_count']} "
        f"duplicate_excess={effective['duplicate_entry_excess']} metadata_chars={effective['selection_metadata_chars']}"
    )
    print(
        "configuration effect: "
        f"structural_deduplication={str(effect['structural_deduplication']).lower()} "
        f"positive_deduplication={str(effect['positive_deduplication']).lower()} "
        f"entry_reduction={effect['entry_reduction']} "
        f"duplicate_reduction={effect['duplicate_excess_reduction']} "
        f"metadata_reduction={effect['metadata_chars_reduction']} "
        f"capabilities_preserved={str(effect['capability_names_preserved']).lower()}"
    )
    live = report.get("live_prompt_effect", {"status": "not-run"})
    print(f"live prompt effect: {live['status']}")
    runtime = report.get("runtime_catalog", {"status": "not-run"})
    print(f"runtime catalog: {runtime['status']}")
    if runtime.get("source_refresh"):
        refresh = runtime["source_refresh"]
        print(
            "runtime source refresh: "
            f"entries={refresh['refreshed_entries']} "
            f"changed={len(refresh['changed_entries'])} "
            f"errors={len(refresh['errors'])}"
        )
    if runtime.get("prompt_files"):
        prompt_files = runtime["prompt_files"]
        print(
            "runtime prompt files: "
            f"existing={prompt_files['existing_entries']}/{prompt_files['resolved_entries']} "
            f"missing={len(prompt_files['missing_files'])} "
            f"unresolved={len(prompt_files['unresolved_files'])}"
        )
    if runtime.get("visibility"):
        visibility = runtime["visibility"]
        print(
            "runtime visibility: "
            f"visible={visibility['visible_expected_names']}/{visibility['expected_implicit_names']} "
            f"unexpected_missing={len(visibility['unexpected_missing_names'])} "
            f"prompt_entries={visibility['prompt_file_entries']} "
            f"section_chars={visibility['section_chars']}"
        )
        paths = visibility["path_visibility"]
        if paths["available"]:
            print(
                "runtime paths: "
                f"visible={paths['visible_expected_entries']}/{paths['expected_implicit_entries']} "
                f"missing={len(paths['unexpected_missing_paths'])} "
                f"ambiguous={len(paths['ambiguous_prompt_matches'])} "
                f"literal={paths['matched_by_literal']} resolved={paths['matched_by_resolved']}"
            )
        else:
            print(f"runtime paths: unavailable ({paths['reason']})")
        descriptions = visibility["description_visibility"]
        print(
            "runtime descriptions: "
            f"exact={len(descriptions['exact_names'])} "
            f"shortened={len(descriptions['shortened_names'])} "
            f"empty={len(descriptions['empty_names'])} "
            f"mismatch={len(descriptions['mismatch_names'])} "
            f"retained={descriptions['retention_ratio']:.1%}"
        )
        if descriptions["loss_ranking"]:
            worst = ", ".join(
                f"{entry['name']}={entry['retention_ratio']:.1%}"
                for entry in descriptions["loss_ranking"][:5]
            )
            print(f"runtime description loss: {worst}")
    if runtime.get("selector"):
        selector = runtime["selector"]
        print(
            "runtime selector: "
            f"mode={selector.get('detected_mode', 'unknown')} "
            f"target={selector.get('target_name', 'none')}"
        )
    if effective["duplicate_names"]:
        for name, paths in effective["duplicate_names"].items():
            print(f"DUPLICATE {name}: {len(paths)} entries")
    if report["config"]["errors"]:
        for error in report["config"]["errors"]:
            print(f"CONFIG ERROR: {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", type=Path, help="Skill discovery root; repeat for multiple roots")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Codex config.toml path")
    parser.add_argument("--no-config", action="store_true", help="Measure discovery without applying config overrides")
    parser.add_argument("--description-warning", type=int, default=DEFAULT_DESCRIPTION_WARNING)
    parser.add_argument("--skill-line-warning", type=int, default=DEFAULT_SKILL_LINE_WARNING)
    parser.add_argument(
        "--config-path-mode",
        choices=("skill-file", "folder", "either"),
        default="skill-file",
        help="How skills.config paths identify entries; current local CLI behavior uses skill-file",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--live-prompt-check",
        action="store_true",
        help="A/B the current catalog against matched disabled paths re-enabled in a local Codex prompt render",
    )
    parser.add_argument(
        "--runtime-check",
        action="store_true",
        help="Check model-visible capability coverage and probe folder versus SKILL.md selector behavior",
    )
    parser.add_argument(
        "--require-runtime-health",
        action="store_true",
        help=(
            "Fail unless model-visible local Skill files exist, every implicit filesystem Skill is visible, "
            "and selector behavior is detected"
        ),
    )
    parser.add_argument("--probe-dir", type=Path, default=Path(tempfile.gettempdir()))
    parser.add_argument("--codex-command", default="codex")
    parser.add_argument("--strict", action="store_true", help="Fail on catalog errors or remaining effective duplicates")
    parser.add_argument(
        "--require-positive-deduplication",
        action="store_true",
        help="Fail unless configuration removes all duplicate entries while preserving every unique Skill name",
    )
    args = parser.parse_args()
    roots = args.root or list(DEFAULT_ROOTS)
    config_path = None if args.no_config else args.config
    report = analyze_catalog(
        roots,
        config_path,
        args.description_warning,
        args.skill_line_warning,
        args.config_path_mode,
    )
    if args.live_prompt_check or args.require_positive_deduplication:
        live = live_prompt_check(
            list(report["config"]["matched_disabled_paths"]),
            int(report["configuration_effect"]["entry_reduction"]),
            args.probe_dir,
            args.codex_command,
        )
        report["live_prompt_effect"] = live
        positive = bool(report["configuration_effect"]["structural_deduplication"] and live.get("positive"))
        report["configuration_effect"]["positive_deduplication"] = positive
        report["configuration_effect"]["positive_evidence"] = live["status"]
    else:
        report["live_prompt_effect"] = {"status": "not-run", "positive": False}
    if args.runtime_check or args.require_runtime_health:
        report["runtime_catalog"] = runtime_catalog_check(
            list(report["entries"]),
            args.probe_dir,
            args.codex_command,
        )
    else:
        report["runtime_catalog"] = {"status": "not-run", "positive": False}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)

    failed = not report["ok"]
    if args.strict and report["effective"]["duplicate_entry_excess"]:
        failed = True
    if args.require_positive_deduplication and not report["configuration_effect"]["positive_deduplication"]:
        failed = True
    if args.require_runtime_health and not report["runtime_catalog"]["positive"]:
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
