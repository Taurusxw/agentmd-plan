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


class GuardrailCheckTests(unittest.TestCase):
    def test_global_gate_requires_completion_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "AGENTS.md"
            base = """# AGENTS.md
版本：27.8.0
定版日期：2026-07-18
seer-codex-rules
必须读取并遵守
最终回答必须说明
未覆盖风险
"""
            path.write_text(base, encoding="utf-8")
            self.assertIn("完成契约", MODULE.check_global_gate(path)["missing_gate_phrases"])

            path.write_text(base + "完成契约\n", encoding="utf-8")
            self.assertTrue(MODULE.check_global_gate(path)["ok"])

    def test_installed_skill_contains_goal_closure_anchors(self) -> None:
        skill = Path(__file__).parents[1]
        report = MODULE.check_skill(skill)

        self.assertTrue(report["ok"])
        self.assertEqual(report["missing_reference_phrases"], {})


if __name__ == "__main__":
    unittest.main()
