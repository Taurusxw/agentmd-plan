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

        self.assertTrue(MODULE.validate_config(config)["ok"])
        self.assertTrue(MODULE.validate_roles(agents)["ok"])

    def test_rejects_expensive_or_excessive_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            path.write_text(
                """[agents]
enabled = true
max_concurrent_threads_per_session = 8
default_subagent_model = "gpt-5.6-sol"
default_subagent_reasoning_effort = "high"
""",
                encoding="utf-8",
            )
            report = MODULE.validate_config(path)
            self.assertFalse(report["ok"])
            self.assertEqual(len(report["errors"]), 2)


if __name__ == "__main__":
    unittest.main()
