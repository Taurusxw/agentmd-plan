#!/usr/bin/env python3
"""Validate adaptive multi-agent capacity and capability-based Codex roles."""

from __future__ import annotations

import argparse
import json
import os
import tomllib
from pathlib import Path


DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
DEFAULT_CONFIG = DEFAULT_CODEX_HOME / "config.toml"
DEFAULT_AGENTS_DIR = DEFAULT_CODEX_HOME / "agents"

ROLE_POLICIES = {
    "explorer-fast.toml": {
        "name": "explorer_fast",
        "model_family": "terra",
        "allowed_efforts": {"low", "medium", "high"},
        "sandbox_mode": "read-only",
    },
    "worker-balanced.toml": {
        "name": "worker_balanced",
        "model_family": "terra",
        "allowed_efforts": {"medium", "high", "max"},
    },
    "reviewer-deep.toml": {
        "name": "reviewer_deep",
        "model_family": "sol",
        "allowed_efforts": {"high", "xhigh", "max"},
        "sandbox_mode": "read-only",
    },
}

ALLOWED_DEFAULT_EFFORTS = {"low", "medium", "high"}


def read_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def is_positive_int(value: object, minimum: int = 1) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def model_matches_family(value: object, family: str) -> bool:
    return isinstance(value, str) and family in value.lower()


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
    legacy_capacity = agents.get("max_concurrent_threads_per_session")

    features = data.get("features", {})
    if not isinstance(features, dict):
        errors.append("[features] must be a table when present")
        features = {}
    v2 = features.get("multi_agent_v2")
    backend = "v1"
    source = "agents.max_concurrent_threads_per_session"
    configured_capacity: int | None = None
    total_slots: int | None = None

    if isinstance(v2, dict) and v2.get("enabled") is True:
        backend = "v2"
        source = "features.multi_agent_v2.max_concurrent_threads_per_session"
        if legacy_capacity is not None:
            errors.append("do not set the V1 child-capacity key when multi_agent_v2 is enabled")
        v2_capacity = v2.get("max_concurrent_threads_per_session")
        if not is_positive_int(v2_capacity, minimum=2):
            errors.append("V2 max_concurrent_threads_per_session must be an integer of at least 2 total slots")
        else:
            configured_capacity = v2_capacity
            total_slots = v2_capacity
    else:
        if v2 is not None and not isinstance(v2, dict):
            errors.append("features.multi_agent_v2 must be a table")
        elif isinstance(v2, dict) and v2.get("enabled") is False and v2.get("max_concurrent_threads_per_session") is not None:
            errors.append("remove V2 capacity when multi_agent_v2 is disabled")
        if not is_positive_int(legacy_capacity):
            errors.append("V1 max_concurrent_threads_per_session must be a positive child-thread integer")
        else:
            configured_capacity = legacy_capacity
            total_slots = legacy_capacity + 1

    if not model_matches_family(agents.get("default_subagent_model"), "terra"):
        errors.append("default_subagent_model must use the fast Terra family")
    effort = agents.get("default_subagent_reasoning_effort")
    if effort not in ALLOWED_DEFAULT_EFFORTS:
        errors.append("default_subagent_reasoning_effort must be low, medium, or high")

    capacity = {
        "backend": backend,
        "source": source,
        "configured_value": configured_capacity,
        "total_slots": total_slots,
        "child_slots": total_slots - 1 if total_slots is not None else None,
        "capacity_is_not_dispatch_target": True,
    }
    return {"ok": not errors, "path": str(path), "capacity": capacity, "errors": errors}


def validate_roles(directory: Path) -> dict[str, object]:
    errors: list[str] = []
    roles: dict[str, object] = {}
    for filename, policy in ROLE_POLICIES.items():
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
        if data.get("name") != policy["name"]:
            role_errors.append(f"name must be {policy['name']}")
        if not model_matches_family(data.get("model"), str(policy["model_family"])):
            role_errors.append(f"model must use the {policy['model_family']} family")
        effort = data.get("model_reasoning_effort")
        if effort not in policy["allowed_efforts"]:
            allowed = ", ".join(sorted(policy["allowed_efforts"]))
            role_errors.append(f"model_reasoning_effort must be one of: {allowed}")
        expected_sandbox = policy.get("sandbox_mode")
        if expected_sandbox is not None and data.get("sandbox_mode") != expected_sandbox:
            role_errors.append(f"sandbox_mode must be {expected_sandbox}")
        for required in ("description", "developer_instructions"):
            value = data.get(required)
            if not isinstance(value, str) or not value.strip():
                role_errors.append(f"{required} must be a non-empty string")
        instructions = str(data.get("developer_instructions", "")).lower()
        if "do not delegate unless the parent task packet explicitly authorizes" not in instructions:
            role_errors.append("developer_instructions must default to flat routing with an explicit recursive-packet exception")
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
