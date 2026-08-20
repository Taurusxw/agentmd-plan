#!/usr/bin/env python3
"""Validate static multi-agent capacity, roles, and dispatch compatibility."""

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
        "sandbox_mode": "read-only",
    },
    "worker-balanced.toml": {
        "name": "worker_balanced",
    },
    "reviewer-deep.toml": {
        "name": "reviewer_deep",
        "sandbox_mode": "read-only",
    },
}

ACCESS_KINDS = {"read-only", "write", "network", "approval-bearing"}
READ_ONLY_ROLES = {"explorer_fast", "reviewer_deep"}
KNOWN_ROLES = {str(policy["name"]) for policy in ROLE_POLICIES.values()}
PERMISSION_INSTRUCTION_ANCHOR = (
    "required effective access, current parent effective access, and a compatible "
    "dispatch decision"
)
RUNTIME_PERMISSION_WARNING = (
    "Static config and role defaults do not verify runtime permissions. "
    "Before each spawn, check the parent task's current effective permission mode "
    "against the packet's required access; if an old task or insufficient mode blocks "
    "the packet, keep permitted work in the parent and request access once or use a new "
    "task with the correct mode."
)


def read_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def is_positive_int(value: object, minimum: int = 1) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def assess_dispatch(
    role: str,
    required_effective_access: set[str],
    required_capability_scope: set[str],
    *,
    parent_permission_checked: bool,
    parent_effective_access: set[str] | None = None,
    parent_access_observation_source: str | None = None,
) -> dict[str, object]:
    """Assess one spawn from a caller-supplied current permission snapshot.

    This helper does not probe the runtime. ``parent_permission_checked`` records the
    orchestrator's live check immediately before the spawn and expires after that spawn.
    """
    required = set(required_effective_access)
    capability_scope = {item.strip() for item in required_capability_scope if item.strip()}
    effective = set(parent_effective_access or set())
    observation_source = (parent_access_observation_source or "").strip()
    errors: list[str] = []

    unknown_required = sorted(required - ACCESS_KINDS)
    unknown_effective = sorted(effective - ACCESS_KINDS)
    if not required:
        errors.append("required effective access must not be empty")
    if not capability_scope:
        errors.append("required capability scope must not be empty")
    if role not in KNOWN_ROLES:
        errors.append(f"unknown role: {role}")
    if unknown_required:
        errors.append(f"unknown required access: {', '.join(unknown_required)}")
    if unknown_effective:
        errors.append(f"unknown parent effective access: {', '.join(unknown_effective)}")
    if "write" in required and role in READ_ONLY_ROLES:
        errors.append(f"write access requires an implementation worker, not read-only role {role}")
    if not parent_permission_checked:
        errors.append("parent effective permission mode was not checked for this spawn")
    else:
        if not observation_source:
            errors.append("parent access observation source must be recorded for this spawn")
        if missing := sorted(required - effective):
            errors.append(f"parent effective permission mode lacks required access: {', '.join(missing)}")

    return {
        "ok": not errors,
        "dispatch_decision": "compatible" if not errors else "blocked",
        "role": role,
        "required_effective_access": sorted(required),
        "required_capability_scope": sorted(capability_scope),
        "parent_permission_checked": parent_permission_checked,
        "parent_effective_access": sorted(effective) if parent_permission_checked else [],
        "parent_access_observation_source": observation_source if parent_permission_checked else "",
        "permission_snapshot_scope": "current-spawn-only",
        "errors": errors,
    }


def validate_config(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
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
    agents_enabled = agents.get("enabled", True)
    if not isinstance(agents_enabled, bool):
        errors.append("agents.enabled must be a Boolean when explicitly set")
    canonical_capacity = agents.get("max_concurrent_threads_per_session")
    alias_capacity = agents.get("max_threads")
    if canonical_capacity is not None and alias_capacity is not None:
        errors.append(
            "set only one of agents.max_concurrent_threads_per_session and its "
            "legacy agents.max_threads alias"
        )
    documented_capacity = canonical_capacity if canonical_capacity is not None else alias_capacity
    documented_source = (
        "agents.max_concurrent_threads_per_session"
        if canonical_capacity is not None
        else "agents.max_threads" if alias_capacity is not None else "runtime-default"
    )
    if alias_capacity is not None:
        warnings.append(
            "agents.max_threads is a documented legacy alias; prefer "
            "agents.max_concurrent_threads_per_session for new configuration"
        )

    features = data.get("features", {})
    if not isinstance(features, dict):
        errors.append("[features] must be a table when present")
        features = {}
    v2 = features.get("multi_agent_v2")
    if isinstance(v2, dict) and "enabled" in v2 and not isinstance(v2.get("enabled"), bool):
        errors.append("features.multi_agent_v2.enabled must be a Boolean")
    backend = "agents"
    source = documented_source
    configured_capacity: int | None = None
    total_slots: int | None = None
    portable_configuration = True

    v2_enabled = v2 is True or (isinstance(v2, dict) and v2.get("enabled") is True)
    if not v2_enabled and agents_enabled is False:
        errors.append("multi-agent tools are disabled by agents.enabled")
    elif v2_enabled and agents_enabled is False:
        warnings.append(
            "agents.enabled=false is overridden by enabled features.multi_agent_v2"
        )
    if v2_enabled:
        backend = "schema-v2-override"
        portable_configuration = False
        warnings.append(
            "features.multi_agent_v2 is a non-public, non-portable compatibility input; "
            "do not use it in portable templates or infer runtime semantics from it"
        )
        if documented_capacity is not None:
            warnings.append(
                f"{documented_source} is ignored while features.multi_agent_v2 is enabled"
            )
        v2_capacity = v2.get("max_concurrent_threads_per_session") if isinstance(v2, dict) else None
        source = (
            "features.multi_agent_v2.max_concurrent_threads_per_session"
            if v2_capacity is not None
            else "features.multi_agent_v2"
        )
        if v2_capacity is not None:
            if not is_positive_int(v2_capacity):
                errors.append(
                    "schema V2 max_concurrent_threads_per_session must be an integer "
                    "of at least 1 when explicitly set"
                )
            else:
                configured_capacity = v2_capacity
                # Preserve the configured value in the JSON report without claiming
                # root-inclusion or effective runtime capacity semantics.
                total_slots = None
    else:
        if v2 is not None and not isinstance(v2, (bool, dict)):
            errors.append("features.multi_agent_v2 must be a Boolean or table")
        elif isinstance(v2, dict) and v2.get("enabled") is False and v2.get("max_concurrent_threads_per_session") is not None:
            errors.append("remove V2 capacity when multi_agent_v2 is disabled")
        if documented_capacity is not None:
            if not is_positive_int(documented_capacity):
                errors.append(f"{documented_source} must be a positive spawned-thread integer")
            else:
                configured_capacity = documented_capacity
                total_slots = documented_capacity + 1

    for field in ("default_subagent_model", "default_subagent_reasoning_effort"):
        value = agents.get(field)
        if value is not None and not is_nonempty_string(value):
            errors.append(f"{field} must be a non-empty string when explicitly set")

    capacity = {
        "backend": backend,
        "source": source,
        "configured_value": configured_capacity,
        "total_slots": total_slots,
        "child_slots": total_slots - 1 if total_slots is not None else None,
        "capacity_semantics": (
            "non-public-non-portable-unresolved"
            if backend == "schema-v2-override" and configured_capacity is not None
            else "spawned-threads-excluding-primary"
            if configured_capacity is not None
            else "backend-default-unresolved"
        ),
        "portable_configuration": portable_configuration,
        "capacity_is_not_dispatch_target": True,
    }
    return {
        "ok": not errors,
        "path": str(path),
        "capacity": capacity,
        "warnings": warnings,
        "errors": errors,
    }


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
        for field in ("model", "model_reasoning_effort"):
            if not is_nonempty_string(data.get(field)):
                role_errors.append(f"{field} must be a non-empty string")
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
        if PERMISSION_INSTRUCTION_ANCHOR not in instructions:
            role_errors.append(
                "developer_instructions must require required effective access, "
                "current parent effective access, and a compatible dispatch decision"
            )
        if role_errors:
            errors.extend(f"{filename}: {message}" for message in role_errors)
        roles[filename] = {
            "name": data.get("name"),
            "model": data.get("model"),
            "reasoning_effort": data.get("model_reasoning_effort"),
            "sandbox_mode": data.get("sandbox_mode", "inherit"),
            "static_access_class": (
                "read-only"
                if data.get("name") in READ_ONLY_ROLES
                else "implementation-capable"
            ),
            "static_role_default_only": True,
            "errors": role_errors,
        }
    return {"ok": not errors, "path": str(directory), "roles": roles, "errors": errors}


def build_report(config: dict[str, object], roles: dict[str, object]) -> dict[str, object]:
    """Build a static report without implying that the current spawn can execute it."""
    static_ok = bool(config["ok"] and roles["ok"])
    return {
        "ok": static_ok,
        "validation_scope": "static-configuration-only",
        "static_configuration_ok": static_ok,
        "runtime_permissions_verified": False,
        "dispatch_ready": False,
        "warnings": [RUNTIME_PERMISSION_WARNING, *config.get("warnings", [])],
        "config": config,
        "roles": roles,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--agents-dir", default=str(DEFAULT_AGENTS_DIR))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    config = validate_config(Path(args.config).resolve())
    roles = validate_roles(Path(args.agents_dir).resolve())
    report = build_report(config, roles)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"overall: {'ok' if report['ok'] else 'failed'}")
        print("runtime_permissions_verified: false")
        print("dispatch_ready: false")
        for warning in report["warnings"]:
            print(f"warning: {warning}")
        for section in (config, roles):
            print(f"{section['path']}: {'ok' if section['ok'] else 'failed'}")
            for warning in section.get("warnings", []):
                print(f"  warning: {warning}")
            for error in section["errors"]:
                print(f"  - {error}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
