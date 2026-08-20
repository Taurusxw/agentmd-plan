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
版本：27.9.0
定版日期：2026-07-28
seer-codex-rules
必须读取并遵守
最终回答必须说明
未覆盖风险
multi-agent-governance.md
无需再次确认
同一授权范围只确认一次
不因追求更强信心重跑
全量回归
agentmd-plan` 专有项目
严禁直接修改
详细变更报告
最新有效全局规则
旧对话
最高版本号
不得用文件、逐页、树或 artifact 哈希替代
没有上述需求时默认不计算、不记录
"""
            path.write_text(base, encoding="utf-8")
            self.assertIn("完成契约", MODULE.check_global_gate(path)["missing_gate_phrases"])

            path.write_text(
                base + "完成契约\n主动派生合适的子 Agent\n不设固定治理上限\n容量不是派遣目标\n",
                encoding="utf-8",
            )
            self.assertTrue(MODULE.check_global_gate(path)["ok"])

    def test_global_gate_requires_adaptive_multi_agent_authorization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "AGENTS.md"
            text = """# AGENTS.md
版本：27.9.0
定版日期：2026-07-28
seer-codex-rules
必须读取并遵守
最终回答必须说明
未覆盖风险
完成契约
multi-agent-governance.md
无需再次确认
同一授权范围只确认一次
不因追求更强信心重跑
全量回归
agentmd-plan` 专有项目
严禁直接修改
详细变更报告
最新有效全局规则
旧对话
最高版本号
不得用文件、逐页、树或 artifact 哈希替代
没有上述需求时默认不计算、不记录
"""
            path.write_text(text, encoding="utf-8")
            missing = MODULE.check_global_gate(path)["missing_gate_phrases"]
            self.assertIn("主动派生合适的子 Agent", missing)
            self.assertIn("不设固定治理上限", missing)
            self.assertIn("容量不是派遣目标", missing)

    def test_installed_skill_contains_goal_closure_anchors(self) -> None:
        skill = Path(__file__).parents[1]
        report = MODULE.check_skill(skill)

        self.assertTrue(report["ok"])
        self.assertEqual(report["missing_reference_phrases"], {})

    def test_global_gate_requires_efficiency_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "AGENTS.md"
            text = "\n".join([
                "版本：27.13.0",
                "定版日期：2026-08-03",
                *(phrase for phrase in MODULE.REQUIRED_GATE_PHRASES if phrase != "详细变更报告"),
            ])
            path.write_text(text, encoding="utf-8")
            self.assertIn("详细变更报告", MODULE.check_global_gate(path)["missing_gate_phrases"])

    def test_global_gate_requires_governance_owner_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "AGENTS.md"
            text = "\n".join([
                "版本：28.0.0",
                "定版日期：2026-08-03",
                *(phrase for phrase in MODULE.REQUIRED_GATE_PHRASES if phrase != "严禁直接修改"),
            ])
            path.write_text(text, encoding="utf-8")
            self.assertIn("严禁直接修改", MODULE.check_global_gate(path)["missing_gate_phrases"])

    def test_global_gate_requires_latest_effective_rule(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "AGENTS.md"
            text = "\n".join([
                "版本：28.2.0",
                "定版日期：2026-08-03",
                *(phrase for phrase in MODULE.REQUIRED_GATE_PHRASES if phrase != "最高版本号"),
            ])
            path.write_text(text, encoding="utf-8")
            self.assertIn("最高版本号", MODULE.check_global_gate(path)["missing_gate_phrases"])

    def test_global_gate_requires_integrity_evidence_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "AGENTS.md"
            required_phrases = (
                "不得用文件、逐页、树或 artifact 哈希替代",
                "没有上述需求时默认不计算、不记录",
            )
            for required_phrase in required_phrases:
                with self.subTest(required_phrase=required_phrase):
                    text = "\n".join([
                        "版本：29.1.0",
                        "定版日期：2026-08-20",
                        *(
                            phrase
                            for phrase in MODULE.REQUIRED_GATE_PHRASES
                            if phrase != required_phrase
                        ),
                    ])
                    path.write_text(text, encoding="utf-8")
                    self.assertIn(
                        required_phrase,
                        MODULE.check_global_gate(path)["missing_gate_phrases"],
                    )


if __name__ == "__main__":
    unittest.main()
