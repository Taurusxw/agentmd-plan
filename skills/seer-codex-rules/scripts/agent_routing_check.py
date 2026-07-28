#!/usr/bin/env python3
"""Validate efficient multi-agent defaults and custom Codex role files."""

from __future__ import annotations

import argparse
import json
import os
import tomllib
from pathlib import Path


DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
DEFAULT_CONFIG = DEFAULT_CODEX_HOME / "config.toml"
DEFAULT_AGENTS_DIR = DEFAULT_CODEX_HOME / "agents"

EXPECTED_ROLES = {
    "explorer-fast.toml": {
        "name": "explorer_fast",
        "model": "gpt-5.6-terra",
        "model_reasoning_effort": "high",
        "sandbox_mode": "read-only",
    },
    "worker-balanced.toml": {
        "name": "worker_balanced",
        "model": "gpt-5.6-terra",
        "model_reasoning_effort": "max",
    },
    "reviewer-deep.toml": {
        "name": "reviewer_deep",
        "model": "gpt-5.6-sol",
        "model_reasoning_effort": "high",
        "sandbox_mode": "read-only",
    },
}


def read_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def validate_config(path: Path) -> dict[str, object]:
    errors: list[str] = []
    if not path.is_file():
        return {"ok": False, "path": str(path), "errors": ["file is missing"]}
    try:
        data = read_toml(path)
    except (OSError, tomllib.TOMLDecodeError) as error:
        return {"ok": False, "path": str(path), "errors": [f"invalid TOML: {error}"]}

    agents = data.get("agents")
    if not isinstance(agents, dict):
        errors.append("[agents] table is missing")
        agents = {}
    if agents.get("enabled") is not True:
        errors.append("agents.enabled must be true")
    concurrency = agents.get("max_concurrent_threads_per_session")
    if not isinstance(concurrency, int) or isinstance(concurrency, bool) or not 1 <= concurrency <= 3:
        errors.append("max_concurrent_threads_per_session must be an integer from 1 to 3")
    if agents.get("default_subagent_model") != "gpt-5.6-terra":
        errors.append("default_subagent_model must be gpt-5.6-terra")
    if agents.get("default_subagent_reasoning_effort") != "high":
        errors.append("default_subagent_reasoning_effort must be high")
    return {"ok": not errors, "path": str(path), "errors": errors}


def validate_roles(directory: Path) -> dict[str, object]:
    errors: list[str] = []
    roles: dict[str, object] = {}
    for filename, expected in EXPECTED_ROLES.items():
        path = directory / filename
        if not path.is_file():
            errors.append(f"missing role file: {filename}")
            continue
        try:
            data = read_toml(path)
        except (OSError, tomllib.TOMLDecodeError) as error:
            errors.append(f"invalid TOML in {filename}: {error}")
            continue
        role_errors: list[str] = []
        for key, value in expected.items():
            if data.get(key) != value:
                role_errors.append(f"{key} must be {value}")
        for required in ("description", "developer_instructions"):
            value = data.get(required)
            if not isinstance(value, str) or not value.strip():
                role_errors.append(f"{required} must be a non-empty string")
        if "do not delegate" not in str(data.get("developer_instructions", "")).lower():
            role_errors.append("developer_instructions must prohibit nested delegation")
        if role_errors:
            errors.extend(f"{filename}: {message}" for message in role_errors)
        roles[filename] = {
            "name": data.get("name"),
            "model": data.get("model"),
            "reasoning_effort": data.get("model_reasoning_effort"),
            "sandbox_mode": data.get("sandbox_mode", "inherit"),
            "errors": role_errors,
        }
    return {"ok": not errors, "path": str(directory), "roles": roles, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--agents-dir", default=str(DEFAULT_AGENTS_DIR))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    config = validate_config(Path(args.config).resolve())
    roles = validate_roles(Path(args.agents_dir).resolve())
    report = {"ok": bool(config["ok"] and roles["ok"]), "config": config, "roles": roles}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"overall: {'ok' if report['ok'] else 'failed'}")
        for section in (config, roles):
            print(f"{section['path']}: {'ok' if section['ok'] else 'failed'}")
            for error in section["errors"]:
                print(f"  - {error}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
