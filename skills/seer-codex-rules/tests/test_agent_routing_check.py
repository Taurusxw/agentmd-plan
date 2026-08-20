from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "agent_routing_check.py"
SPEC = importlib.util.spec_from_file_location("agent_routing_check", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AgentRoutingCheckTests(unittest.TestCase):
    def test_project_templates_are_valid(self) -> None:
        project = Path(__file__).parents[3]
        config = project / "config" / "agents.toml.example"
        agents = project / "config" / "agents"

        config_report = MODULE.validate_config(config)
        self.assertTrue(config_report["ok"])
        self.assertEqual(config_report["capacity"]["backend"], "agents")
        self.assertEqual(config_report["capacity"]["total_slots"], 32)
        self.assertEqual(config_report["capacity"]["child_slots"], 31)
        self.assertTrue(config_report["capacity"]["portable_configuration"])
        roles_report = MODULE.validate_roles(agents)
        self.assertTrue(roles_report["ok"])
        self.assertEqual(
            roles_report["roles"]["explorer-fast.toml"]["static_access_class"],
            "read-only",
        )
        self.assertEqual(
            roles_report["roles"]["worker-balanced.toml"]["static_access_class"],
            "implementation-capable",
        )

    def test_accepts_large_capacity_with_backend_specific_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            documented_path = Path(directory) / "documented.toml"
            documented_path.write_text(
                """[agents]
enabled = true
max_concurrent_threads_per_session = 128
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
""",
                encoding="utf-8",
            )
            documented_report = MODULE.validate_config(documented_path)
            self.assertTrue(documented_report["ok"])
            self.assertEqual(documented_report["capacity"]["total_slots"], 129)
            self.assertEqual(documented_report["capacity"]["child_slots"], 128)
            self.assertTrue(documented_report["capacity"]["portable_configuration"])

            v2_path = Path(directory) / "legacy-v2.toml"
            v2_path.write_text(
                """[agents]
enabled = true
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"

[features.multi_agent_v2]
enabled = true
max_concurrent_threads_per_session = 128
""",
                encoding="utf-8",
            )
            v2_report = MODULE.validate_config(v2_path)
            self.assertTrue(v2_report["ok"])
            self.assertEqual(v2_report["capacity"]["total_slots"], 128)
            self.assertEqual(v2_report["capacity"]["child_slots"], 127)
            self.assertFalse(v2_report["capacity"]["portable_configuration"])
            self.assertEqual(v2_report["capacity"]["backend"], "schema-v2-override")
            self.assertIn("official JSON schema", v2_report["warnings"][0])

            minimum_path = Path(directory) / "v2-minimum.toml"
            minimum_path.write_text(
                """[agents]
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"

[features.multi_agent_v2]
enabled = true
max_concurrent_threads_per_session = 1
""",
                encoding="utf-8",
            )
            minimum_report = MODULE.validate_config(minimum_path)
            self.assertTrue(minimum_report["ok"], minimum_report)
            self.assertEqual(minimum_report["capacity"]["total_slots"], 1)
            self.assertEqual(minimum_report["capacity"]["child_slots"], 0)

    def test_v2_precedence_warns_and_rejects_expensive_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            path.write_text(
                """[agents]
enabled = true
max_concurrent_threads_per_session = 8
default_subagent_model = "gpt-5.6-sol"
default_subagent_reasoning_effort = "ultra"

[features.multi_agent_v2]
enabled = true
max_concurrent_threads_per_session = 32
""",
                encoding="utf-8",
            )
            report = MODULE.validate_config(path)
            self.assertFalse(report["ok"])
            self.assertEqual(len(report["errors"]), 2)
            self.assertIn("must use the fast Terra family", report["errors"][0])
            self.assertIn("must be low, medium, or high", report["errors"][1])
            self.assertTrue(any("is ignored" in warning for warning in report["warnings"]))

    def test_accepts_documented_defaults_and_legacy_capacity_alias(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            defaults_path = Path(directory) / "defaults.toml"
            defaults_path.write_text(
                """[agents]
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
""",
                encoding="utf-8",
            )
            defaults_report = MODULE.validate_config(defaults_path)
            self.assertTrue(defaults_report["ok"], defaults_report)
            self.assertEqual(defaults_report["capacity"]["source"], "runtime-default")
            self.assertIsNone(defaults_report["capacity"]["total_slots"])

            alias_path = Path(directory) / "alias.toml"
            alias_path.write_text(
                """[agents]
max_threads = 7
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
""",
                encoding="utf-8",
            )
            alias_report = MODULE.validate_config(alias_path)
            self.assertTrue(alias_report["ok"], alias_report)
            self.assertEqual(alias_report["capacity"]["source"], "agents.max_threads")
            self.assertEqual(alias_report["capacity"]["child_slots"], 7)
            self.assertIn("documented legacy alias", alias_report["warnings"][0])

    def test_rejects_both_documented_capacity_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.toml"
            path.write_text(
                """[agents]
max_concurrent_threads_per_session = 7
max_threads = 7
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
""",
                encoding="utf-8",
            )
            report = MODULE.validate_config(path)
            self.assertFalse(report["ok"])
            self.assertIn("set only one", report["errors"][0])

    def test_v2_boolean_override_takes_precedence_over_agents_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "v2-boolean.toml"
            path.write_text(
                """[agents]
enabled = false
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"

[features]
multi_agent_v2 = true
""",
                encoding="utf-8",
            )
            report = MODULE.validate_config(path)
            self.assertTrue(report["ok"], report)
            self.assertEqual(report["capacity"]["source"], "features.multi_agent_v2")
            self.assertIsNone(report["capacity"]["total_slots"])
            self.assertTrue(any("overridden" in warning for warning in report["warnings"]))

    def test_rejects_disabled_multi_agent_without_v2_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "disabled.toml"
            path.write_text(
                """[agents]
enabled = false
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
""",
                encoding="utf-8",
            )
            report = MODULE.validate_config(path)
            self.assertFalse(report["ok"])
            self.assertIn("disabled by agents.enabled", report["errors"][0])

    def test_rejects_write_dispatch_to_read_only_role(self) -> None:
        report = MODULE.assess_dispatch(
            "explorer_fast",
            {"read-only", "write"},
            {"E:/project/src"},
            parent_permission_checked=True,
            parent_effective_access={"read-only", "write"},
            parent_access_observation_source="current task permission profile",
        )

        self.assertFalse(report["ok"])
        self.assertEqual(report["dispatch_decision"], "blocked")
        self.assertIn("write access requires an implementation worker", report["errors"][0])

    def test_static_checker_never_claims_runtime_permissions(self) -> None:
        project = Path(__file__).parents[3]
        config_report = MODULE.validate_config(project / "config" / "agents.toml.example")
        roles_report = MODULE.validate_roles(project / "config" / "agents")
        report = MODULE.build_report(config_report, roles_report)

        self.assertTrue(report["static_configuration_ok"])
        self.assertFalse(report["runtime_permissions_verified"])
        self.assertFalse(report["dispatch_ready"])
        self.assertIn("do not verify runtime permissions", report["warnings"][0])

    def test_rejects_role_with_incomplete_permission_instruction(self) -> None:
        project = Path(__file__).parents[3]
        source_roles = project / "config" / "agents"
        with tempfile.TemporaryDirectory() as directory:
            copied_roles = Path(directory)
            for source in source_roles.glob("*.toml"):
                text = source.read_text(encoding="utf-8")
                if source.name == "worker-balanced.toml":
                    text = text.replace(
                        MODULE.PERMISSION_INSTRUCTION_ANCHOR,
                        "required effective access and current parent effective access",
                    )
                (copied_roles / source.name).write_text(text, encoding="utf-8")

            report = MODULE.validate_roles(copied_roles)

        self.assertFalse(report["ok"])
        self.assertTrue(any("compatible dispatch decision" in error for error in report["errors"]))

    def test_accepts_legal_read_only_dispatch_after_parent_check(self) -> None:
        report = MODULE.assess_dispatch(
            "reviewer_deep",
            {"read-only"},
            {"E:/project"},
            parent_permission_checked=True,
            parent_effective_access={"read-only"},
            parent_access_observation_source="current task permission profile",
        )

        self.assertTrue(report["ok"], report)
        self.assertEqual(report["dispatch_decision"], "compatible")
        self.assertEqual(report["permission_snapshot_scope"], "current-spawn-only")

    def test_accepts_legal_worker_dispatch_after_parent_check(self) -> None:
        report = MODULE.assess_dispatch(
            "worker_balanced",
            {"read-only", "write"},
            {"E:/project/src"},
            parent_permission_checked=True,
            parent_effective_access={"read-only", "write"},
            parent_access_observation_source="current task permission profile",
        )

        self.assertTrue(report["ok"], report)

    def test_rejects_dispatch_without_current_parent_permission_check(self) -> None:
        report = MODULE.assess_dispatch(
            "worker_balanced",
            {"write"},
            {"E:/project/src"},
            parent_permission_checked=False,
            parent_effective_access={"write"},
        )

        self.assertFalse(report["ok"])
        self.assertEqual(report["parent_effective_access"], [])
        self.assertIn("not checked for this spawn", report["errors"][0])

    def test_rejects_checked_parent_that_lacks_required_write_access(self) -> None:
        report = MODULE.assess_dispatch(
            "worker_balanced",
            {"write"},
            {"E:/project/src"},
            parent_permission_checked=True,
            parent_effective_access={"read-only"},
            parent_access_observation_source="current task permission profile",
        )

        self.assertFalse(report["ok"])
        self.assertIn("lacks required access: write", report["errors"][0])

    def test_network_and_approval_access_must_be_present_in_parent_snapshot(self) -> None:
        accepted = MODULE.assess_dispatch(
            "explorer_fast",
            {"read-only", "network", "approval-bearing"},
            {"official docs", "web search"},
            parent_permission_checked=True,
            parent_effective_access={"read-only", "network", "approval-bearing"},
            parent_access_observation_source="current task permission profile",
        )
        rejected = MODULE.assess_dispatch(
            "explorer_fast",
            {"read-only", "network", "approval-bearing"},
            {"official docs", "web search"},
            parent_permission_checked=True,
            parent_effective_access={"read-only", "network"},
            parent_access_observation_source="current task permission profile",
        )

        self.assertTrue(accepted["ok"], accepted)
        self.assertFalse(rejected["ok"])
        self.assertIn("lacks required access: approval-bearing", rejected["errors"][-1])

    def test_rejects_empty_unknown_role_and_unknown_access_kinds(self) -> None:
        empty_unknown_role = MODULE.assess_dispatch(
            "mystery_role",
            set(),
            set(),
            parent_permission_checked=True,
            parent_effective_access={"read-only"},
            parent_access_observation_source="current task permission profile",
        )
        unknown_access = MODULE.assess_dispatch(
            "worker_balanced",
            {"write", "secrets"},
            {"E:/project/src"},
            parent_permission_checked=True,
            parent_effective_access={"write", "root"},
            parent_access_observation_source="current task permission profile",
        )

        self.assertFalse(empty_unknown_role["ok"])
        self.assertIn("must not be empty", empty_unknown_role["errors"][0])
        self.assertIn("required capability scope", empty_unknown_role["errors"][1])
        self.assertIn("unknown role", empty_unknown_role["errors"][2])
        self.assertFalse(unknown_access["ok"])
        self.assertTrue(any("unknown required access: secrets" in error for error in unknown_access["errors"]))
        self.assertTrue(any("unknown parent effective access: root" in error for error in unknown_access["errors"]))

    def test_rejects_dispatch_without_scope_or_observation_source(self) -> None:
        report = MODULE.assess_dispatch(
            "worker_balanced",
            {"write"},
            set(),
            parent_permission_checked=True,
            parent_effective_access={"write"},
        )

        self.assertFalse(report["ok"])
        self.assertTrue(any("capability scope" in error for error in report["errors"]))
        self.assertTrue(any("observation source" in error for error in report["errors"]))

    def test_plain_text_cli_keeps_runtime_non_claims_visible(self) -> None:
        project = Path(__file__).parents[3]
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--config",
                str(project / "config" / "agents.toml.example"),
                "--agents-dir",
                str(project / "config" / "agents"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("runtime_permissions_verified: false", completed.stdout)
        self.assertIn("dispatch_ready: false", completed.stdout)


if __name__ == "__main__":
    unittest.main()
