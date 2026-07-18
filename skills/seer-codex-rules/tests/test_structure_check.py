from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "structure_check.py"
SPEC = importlib.util.spec_from_file_location("structure_check", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class StructureCheckTests(unittest.TestCase):
    def test_reports_combined_hotspot_and_sibling_duplication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src"
            rounds = root / "docs" / "progress" / "rounds"
            source.mkdir(parents=True)
            rounds.mkdir(parents=True)

            functions = "\n".join(f"function shared{i}() {{ return {i}; }}" for i in range(12))
            filler = "\n".join(f"const value{i} = {i};" for i in range(810))
            (source / "hot.js").write_text(functions + "\n" + filler, encoding="utf-8")
            (source / "peer.js").write_text(functions, encoding="utf-8")
            for number in range(1, 6):
                (rounds / f"2026-07-18-round-{number:03d}.md").write_text("Changed src/hot.js\n", encoding="utf-8")

            report = MODULE.analyze(root, recent_rounds=10, recent_commits=0, include_tests=False)

            self.assertTrue(report["review_required"])
            self.assertEqual(report["hotspots"][0]["path"], "src/hot.js")
            self.assertIn("patch_hotspot", report["hotspots"][0]["signals"])
            self.assertIn("size_signal", report["hotspots"][0]["signals"])
            self.assertIn("sibling_duplication", report["hotspots"][0]["signals"])
            self.assertEqual(report["duplication_candidates"][0]["shared_functions"], 12)

    def test_large_file_alone_does_not_require_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("large.py").write_text("\n".join(f"value_{i} = {i}" for i in range(801)), encoding="utf-8")

            report = MODULE.analyze(root, recent_rounds=10, recent_commits=0, include_tests=False)

            self.assertFalse(report["review_required"])
            self.assertEqual(report["hotspots"][0]["signals"], ["size_signal"])


if __name__ == "__main__":
    unittest.main()
