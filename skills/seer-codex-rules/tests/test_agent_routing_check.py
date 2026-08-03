from __future__ import annotations

import importlib.util
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
        self.assertEqual(config_report["capacity"]["backend"], "v2")
        self.assertEqual(config_report["capacity"]["total_slots"], 32)
        self.assertEqual(config_report["capacity"]["child_slots"], 31)
        self.assertTrue(MODULE.validate_roles(agents)["ok"])

    def test_accepts_large_capacity_with_backend_specific_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            v2_path = Path(directory) / "v2.toml"
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

            v1_path = Path(directory) / "v1.toml"
            v1_path.write_text(
                """[agents]
enabled = true
max_concurrent_threads_per_session = 128
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
""",
                encoding="utf-8",
            )
            v1_report = MODULE.validate_config(v1_path)
            self.assertTrue(v1_report["ok"])
            self.assertEqual(v1_report["capacity"]["total_slots"], 129)
            self.assertEqual(v1_report["capacity"]["child_slots"], 128)

    def test_rejects_conflicting_capacity_and_expensive_fallback(self) -> None:
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
            self.assertEqual(len(report["errors"]), 3)
            self.assertIn("do not set the V1 child-capacity key", report["errors"][0])


if __name__ == "__main__":
    unittest.main()
