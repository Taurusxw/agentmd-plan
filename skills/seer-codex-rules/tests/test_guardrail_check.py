from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "guardrail_check.py"
SPEC = importlib.util.spec_from_file_location("guardrail_check", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

SNAPSHOT_SCRIPT = Path(__file__).parents[1] / "scripts" / "snapshot_state.py"
SNAPSHOT_SPEC = importlib.util.spec_from_file_location("snapshot_state", SNAPSHOT_SCRIPT)
SNAPSHOT_MODULE = importlib.util.module_from_spec(SNAPSHOT_SPEC)
assert SNAPSHOT_SPEC.loader is not None
SNAPSHOT_SPEC.loader.exec_module(SNAPSHOT_MODULE)


class GuardrailCheckTests(unittest.TestCase):
    def test_global_gate_requires_governance_only_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "AGENTS.md"
            text = "\n".join([
                "版本：30.0.0",
                "定版日期：2026-08-20",
                *(phrase for phrase in MODULE.REQUIRED_GATE_PHRASES if phrase != "concrete net benefit"),
            ])
            path.write_text(text, encoding="utf-8")

            self.assertIn("concrete net benefit", MODULE.check_global_gate(path)["missing_gate_phrases"])

            path.write_text(text + "\nconcrete net benefit\n", encoding="utf-8")
            report = MODULE.check_global_gate(path)
            self.assertTrue(report["ok"], report)
            self.assertNotIn("sha256", report)

    def test_default_state_and_copy_comparison_are_off(self) -> None:
        project = Path(__file__).parents[3]
        state = MODULE.check_state(
            project,
            project / "artifacts" / "AGENTS-30.0.0.md",
            project / "skills" / "seer-codex-rules",
            required=False,
        )

        self.assertTrue(state["ok"])
        self.assertEqual(state["status"], "not-requested")

    def test_inventory_anchor_requires_version_without_persisted_digest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            inventory = Path(directory) / "global-agents-rule-inventory.md"
            inventory.write_text("Source global version: `30.0.0`\n", encoding="utf-8")

            self.assertEqual(MODULE.parse_inventory_version(inventory), "30.0.0")
            self.assertEqual(SNAPSHOT_MODULE.parse_inventory_version(inventory), "30.0.0")

    def test_installed_skill_routes_and_contains_current_multi_agent_anchors(self) -> None:
        skill = Path(__file__).parents[1]
        report = MODULE.check_skill(skill)

        self.assertTrue(report["ok"], report)
        self.assertEqual(report["missing_reference_phrases"], {})
        self.assertNotIn("tree_sha256", report)


if __name__ == "__main__":
    unittest.main()
