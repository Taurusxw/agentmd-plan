from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "skill_catalog_check.py"
SPEC = importlib.util.spec_from_file_location("skill_catalog_check", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def write_skill(path: Path, name: str, description: str, openai_yaml: str | None = None) -> None:
    path.mkdir(parents=True)
    (path / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    if openai_yaml is not None:
        agents = path / "agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text(openai_yaml, encoding="utf-8")


class SkillCatalogCheckTests(unittest.TestCase):
    def test_config_prunes_duplicate_and_preserves_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            codex_root = base / ".codex" / "skills"
            agents_root = base / ".agents" / "skills"
            alias = codex_root / "nature-writing"
            canonical = agents_root / "nature-writing"
            write_skill(alias, "nature-writing", "duplicate alias")
            write_skill(canonical, "nature-writing", "canonical entry")
            write_skill(codex_root / ".system" / "skill-creator", "skill-creator", "system skill")
            write_skill(
                codex_root / "explicit-tool",
                "explicit-tool",
                "explicit tool",
                "policy:\n  allow_implicit_invocation: false\ndependencies:\n  tools:\n    - browser\n",
            )
            config = base / ".codex" / "config.toml"
            config.write_text(
                f"[[skills.config]]\npath = '{alias / 'SKILL.md'}'\nenabled = false\n",
                encoding="utf-8",
            )

            report = MODULE.analyze_catalog([codex_root, agents_root], config)

            self.assertTrue(report["ok"], report)
            self.assertEqual(report["raw"]["entries"], 4)
            self.assertEqual(report["raw"]["unique_name_count"], 3)
            self.assertEqual(report["raw"]["duplicate_entry_excess"], 1)
            self.assertEqual(report["effective"]["entries"], 3)
            self.assertEqual(report["effective"]["duplicate_entry_excess"], 0)
            self.assertEqual(report["effective"]["unique_names"], report["raw"]["unique_names"])
            self.assertEqual(report["effective"]["explicit_only_entries"], ["explicit-tool"])
            self.assertEqual(report["effective"]["dependency_entries"], ["explicit-tool"])
            self.assertGreater(
                report["effective"]["total_metadata_chars"],
                report["effective"]["selection_metadata_chars"],
            )
            self.assertTrue(report["configuration_effect"]["structural_deduplication"])
            self.assertFalse(report["configuration_effect"]["positive_deduplication"])
            self.assertGreater(report["configuration_effect"]["metadata_chars_reduction"], 0)

    def test_discovery_follows_a_top_level_directory_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "skills"
            root.mkdir()
            target = base / "managed" / "linked-tool"
            write_skill(target, "linked-tool", "linked entry")
            link = root / "linked-tool"
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")

            paths, warnings = MODULE.discover_skill_dirs([root])

            self.assertEqual(warnings, [])
            self.assertEqual(paths, [link.absolute()])
            self.assertEqual(MODULE.inspect_skill(paths[0])["name"], "linked-tool")

    def test_disabling_unique_skill_is_not_positive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "skills"
            only = root / "only-skill"
            write_skill(only, "only-skill", "only capability")
            config = base / "config.toml"
            config.write_text(
                f"[[skills.config]]\npath = '{only / 'SKILL.md'}'\nenabled = false\n",
                encoding="utf-8",
            )

            report = MODULE.analyze_catalog([root], config)

            self.assertFalse(report["ok"])
            self.assertFalse(report["configuration_effect"]["capability_names_preserved"])
            self.assertEqual(report["configuration_effect"]["removed_capability_names"], ["only-skill"])
            self.assertFalse(report["configuration_effect"]["positive_deduplication"])

    def test_folder_override_is_stale_in_skill_file_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "skills"
            duplicate = root / "duplicate"
            peer_root = base / "peer"
            write_skill(duplicate, "same-name", "first")
            write_skill(peer_root / "same-name", "same-name", "second")
            config = base / "config.toml"
            config.write_text(
                f"[[skills.config]]\npath = '{duplicate}'\nenabled = false\n",
                encoding="utf-8",
            )

            report = MODULE.analyze_catalog([root, peer_root], config)

            self.assertEqual(report["config"]["match_mode"], "skill-file")
            self.assertEqual(report["effective"]["duplicate_entry_excess"], 1)
            self.assertEqual(len(report["config"]["stale_entries"]), 1)
            self.assertFalse(report["configuration_effect"]["positive_deduplication"])

    def test_live_prompt_gate_rejects_context_growth(self) -> None:
        configured = {
            "section_chars": 110,
            "catalog_chars": 100,
            "file_entries": 2,
            "entry_line_chars": 95,
        }
        enabled_control = {
            "section_chars": 100,
            "catalog_chars": 90,
            "file_entries": 3,
            "entry_line_chars": 85,
        }

        result = MODULE.compare_prompt_metrics(configured, enabled_control, expected_entry_reduction=1)

        self.assertFalse(result["positive"])
        self.assertEqual(result["reductions"]["file_entries"], 1)
        self.assertLess(result["reductions"]["section_chars"], 0)

    def test_live_prompt_gate_accepts_strict_net_reduction(self) -> None:
        configured_json = '{"input":[{"content":"<skills_instructions>\\n### Available skills\\n- one: first (file: a)\\n</skills_instructions>"}]}'
        control_json = '{"input":[{"content":"<skills_instructions>\\n### Available skills\\n- one: first (file: a)\\n- one: duplicate (file: b)\\n</skills_instructions>"}]}'
        configured = MODULE.prompt_metrics_from_json(configured_json)
        control = MODULE.prompt_metrics_from_json(control_json)

        result = MODULE.compare_prompt_metrics(configured, control, expected_entry_reduction=1)

        self.assertTrue(result["positive"])
        self.assertEqual(result["reductions"]["file_entries"], 1)

    def test_prompt_catalog_parses_namespaced_names_and_omission_warning(self) -> None:
        prompt = {
            "input": [
                {
                    "content": (
                        "<skills_instructions>\n### Available skills\n"
                        "- chrome:control-chrome: Control Chrome. (file: r0/chrome/SKILL.md)\n"
                        "Showing 1 of 2 skills due to context limits.\n"
                        "</skills_instructions>"
                    )
                }
            ]
        }

        catalog = MODULE.prompt_catalog_from_json(json.dumps(prompt))

        self.assertEqual(catalog["names"], ["chrome:control-chrome"])
        self.assertEqual(catalog["file_entries"], 1)
        self.assertEqual(len(catalog["omission_warnings"]), 1)

    def test_prompt_catalog_resolves_compact_skill_root_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "skills"
            root_value = root.as_posix()
            prompt = {
                "input": [
                    {
                        "content": (
                            "<skills_instructions>\n### Skill roots\n"
                            f"- `r0` = `{root_value}`\n"
                            "### Available skills\n"
                            "- probe: compact path (file: r0/probe/SKILL.md)\n"
                            "</skills_instructions>"
                        )
                    }
                ]
            }

            catalog = MODULE.prompt_catalog_from_json(json.dumps(prompt))

            self.assertEqual(catalog["skill_roots"], {"r0": root_value})
            self.assertEqual(
                Path(catalog["entries"][0]["resolved_file"]),
                (root / "probe" / "SKILL.md").absolute(),
            )

    def test_prompt_file_health_rejects_missing_local_plugin_and_reports_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            installed = base / "installed"
            write_skill(installed, "installed", "installed skill")
            installed_file = installed / "SKILL.md"
            missing_file = base / "plugin-cache" / "missing" / "SKILL.md"
            remote_file = "skill://managed/remote/SKILL.md"
            entries = [
                {"file": str(installed_file), "resolved_file": str(installed_file)},
                {"file": str(missing_file), "resolved_file": str(missing_file)},
                {"file": remote_file, "resolved_file": None},
            ]

            result = MODULE.prompt_file_health(entries)

            self.assertFalse(result["positive"])
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["prompt_entries"], 3)
            self.assertEqual(result["resolved_entries"], 2)
            self.assertEqual(result["existing_entries"], 1)
            self.assertEqual(result["missing_files"], [str(missing_file)])
            self.assertEqual(result["unresolved_files"], [remote_file])

    def test_path_visibility_detects_hidden_duplicate_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            first = base / "first" / "same-name"
            second = base / "second" / "same-name"
            entries = [
                {
                    "name": "same-name",
                    "path": str(path),
                    "description": description,
                    "enabled": True,
                    "openai_yaml": {"allow_implicit_invocation": True},
                }
                for path, description in (
                    (first, "first description"),
                    (second, "second description"),
                )
            ]
            catalog = {
                "names": ["same-name"],
                "entries": [
                    {
                        "name": "same-name",
                        "description": "first description",
                        "file": str(first / "SKILL.md"),
                        "resolved_file": str(first / "SKILL.md"),
                    }
                ],
                "omission_warnings": [],
                "unique_name_count": 1,
                "file_entries": 1,
                "duplicate_name_excess": 0,
                "section_chars": 100,
                "catalog_chars": 80,
            }

            result = MODULE.compare_runtime_visibility(entries, catalog)

            self.assertEqual(result["unexpected_missing_names"], [])
            self.assertFalse(result["positive"])
            self.assertEqual(result["path_visibility"]["visible_expected_entries"], 1)
            self.assertEqual(result["path_visibility"]["expected_implicit_entries"], 2)
            self.assertEqual(
                result["path_visibility"]["unexpected_missing_paths"],
                [str(second / "SKILL.md")],
            )

    def test_path_provenance_ignores_foreign_same_name_description(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            local = base / "local" / "same-name"
            foreign = base / "foreign" / "same-name"
            entries = [
                {
                    "name": "same-name",
                    "path": str(local),
                    "description": "local description with trigger words",
                    "enabled": True,
                    "openai_yaml": {"allow_implicit_invocation": True},
                }
            ]
            catalog = {
                "names": ["same-name", "same-name"],
                "entries": [
                    {
                        "name": "same-name",
                        "description": "local description",
                        "file": str(local / "SKILL.md"),
                        "resolved_file": str(local / "SKILL.md"),
                    },
                    {
                        "name": "same-name",
                        "description": "unrelated foreign description that is deliberately longer",
                        "file": str(foreign / "SKILL.md"),
                        "resolved_file": str(foreign / "SKILL.md"),
                    },
                ],
                "omission_warnings": [],
                "unique_name_count": 1,
                "file_entries": 2,
                "duplicate_name_excess": 1,
                "section_chars": 100,
                "catalog_chars": 80,
            }

            result = MODULE.compare_runtime_visibility(entries, catalog)

            self.assertTrue(result["positive"])
            self.assertEqual(result["description_visibility"]["mismatch_names"], [])
            self.assertEqual(result["description_visibility"]["shortened_names"], ["same-name"])
            loss = result["description_visibility"]["loss_ranking"][0]
            self.assertEqual(loss["prompt_file"], str(local / "SKILL.md"))
            self.assertEqual(loss["lost_preview"], " with trigger words")

    def test_runtime_source_refresh_uses_post_renderer_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "changing-skill"
            write_skill(skill, "changing-skill", "before renderer")
            entry = MODULE.inspect_skill(skill)
            (skill / "SKILL.md").write_text(
                "---\nname: changing-skill\ndescription: after renderer\n---\nbody\n",
                encoding="utf-8",
            )

            refreshed, report = MODULE.refresh_runtime_entries([entry])

            self.assertTrue(report["positive"])
            self.assertEqual(refreshed[0]["description"], "after renderer")
            self.assertEqual(report["changed_entries"][0]["fields"], ["description"])

    def test_runtime_visibility_excludes_explicit_only_from_required_coverage(self) -> None:
        entries = [
            {
                "name": "implicit-skill",
                "description": "implicit description with trigger words",
                "enabled": True,
                "openai_yaml": {"allow_implicit_invocation": True},
            },
            {
                "name": "explicit-skill",
                "description": "explicit description",
                "enabled": True,
                "openai_yaml": {"allow_implicit_invocation": False},
            },
        ]
        catalog = {
            "names": ["implicit-skill"],
            "entries": [
                {
                    "name": "implicit-skill",
                    "description": "implicit description",
                }
            ],
            "omission_warnings": [],
            "unique_name_count": 1,
            "file_entries": 1,
            "duplicate_name_excess": 0,
            "section_chars": 100,
            "catalog_chars": 80,
        }

        result = MODULE.compare_runtime_visibility(entries, catalog)

        self.assertTrue(result["positive"])
        self.assertEqual(result["visible_expected_names"], 1)
        self.assertEqual(result["explicit_only_not_listed"], ["explicit-skill"])
        self.assertEqual(result["description_visibility"]["exact_names"], [])
        self.assertEqual(
            result["description_visibility"]["shortened_names"],
            ["implicit-skill"],
        )

        catalog["names"] = []
        missing = MODULE.compare_runtime_visibility(entries, catalog)
        self.assertFalse(missing["positive"])
        self.assertEqual(missing["unexpected_missing_names"], ["implicit-skill"])

    def test_selector_mode_uses_target_visibility_not_prompt_size(self) -> None:
        baseline = {"names": ["probe", "other"], "file_entries": 2}
        skill_file_disabled = {"names": ["other"], "file_entries": 1}
        folder_disabled = {"names": ["probe", "other", "replacement"], "file_entries": 3}

        result = MODULE.classify_selector_mode(
            "probe",
            baseline,
            skill_file_disabled,
            folder_disabled,
        )

        self.assertTrue(result["positive"])
        self.assertEqual(result["detected_mode"], "skill-file")
        self.assertGreater(
            result["file_entry_counts"]["folder_disabled"],
            result["file_entry_counts"]["baseline"],
        )

    def test_folded_description_and_invalid_config_are_reported(self) -> None:
        fields, body, errors = MODULE.parse_frontmatter(
            "---\nname: folded\ndescription: >-\n  first line\n  second line\n---\nbody\n"
        )
        self.assertEqual(fields["description"], "first line second line")
        self.assertEqual(body, ["body"])
        self.assertEqual(errors, [])

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "skills"
            write_skill(root / "folded", "folded", "valid")
            config = base / "config.toml"
            config.write_text("[[skills.config]\n", encoding="utf-8")

            report = MODULE.analyze_catalog([root], config)

            self.assertFalse(report["ok"])
            self.assertEqual(report["config"]["status"], "invalid")
            self.assertTrue(report["config"]["errors"])

    def test_flow_collection_description_is_not_accepted_as_a_string(self) -> None:
        fields, _, errors = MODULE.parse_frontmatter(
            "---\nname: invalid-description\ndescription: [TODO: replace me]\n---\nbody\n"
        )

        self.assertEqual(fields["description"], "[TODO: replace me]")
        self.assertIn("description must be a YAML string scalar", errors)


if __name__ == "__main__":
    unittest.main()
