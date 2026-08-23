# Agentmd Plan v30.1.0

## Status

Released on 2026-08-24 after source validation, complete maintainer-environment Skill installation, and GitHub publication passed.

## 中文

`v30.1.0` 是一次治理 Skill 的 minor 发布。它新增依赖-free 的全局 Skill catalog 检查器，在不增加第三方依赖的前提下，把文件系统发现、`skills.config` 去重、模型可见 prompt 和本地文件健康统一为可执行证据。

### 主要内容

- 新增 `skill_catalog_check.py`：支持多个 Skill 根、顶层目录链接、`.system`、`agents/openai.yaml` 的隐式调用策略，以及 `skills.config` 的 `SKILL.md` 路径选择器。
- 新增真实 prompt A/B 与 runtime health：核对名称、每个来源路径、描述缩短/错配、遗漏警告和 selector 行为；prompt 中可解析的本地 `SKILL.md` 必须真实存在，托管 URI 只报告而不误判失败。
- renderer 可能刷新 `.system` Skill 时，检查器会重新读取来源元数据，避免 TOCTOU 假阳性；非法非字符串 YAML description 也会被拦截。
- `seer-codex-rules` description 从 219 个可见字符收缩到 179 个字符，同时保留治理触发词；真实 prompt 中不再被截断。
- `guardrail_check.py` 将新 catalog 检查器纳入必需脚本集合，并新增 16 项专项测试。
- 全局 `AGENTS.md` 规则内容与 `30.0.0` artifact 不变；本次不重做 Nature、历史 31-child 压测或全局规则验收。

## English

`v30.1.0` is a minor governance-Skill release. It adds a dependency-free global Skill catalog checker that turns filesystem discovery, `skills.config` deduplication, model-visible prompt exposure, and local-file health into executable evidence.

### Highlights

- Adds `skill_catalog_check.py` with multi-root discovery, top-level directory links, `.system`, implicit invocation policy from `agents/openai.yaml`, and `skills.config` `SKILL.md` selectors.
- Adds real prompt A/B and runtime health checks for names, source paths, description shortening or mismatch, omission warnings, and selector behavior. Every locally resolvable prompt `SKILL.md` must exist; managed URIs are reported without being misclassified as missing local files.
- Refreshes source metadata after renderer-driven `.system` updates to avoid TOCTOU false positives, and rejects non-string YAML descriptions.
- Reduces the model-visible `seer-codex-rules` description from 219 to 179 characters while preserving governance trigger terms; the live prompt no longer truncates it.
- Makes the catalog checker a required guardrail script and adds 16 focused tests.
- Leaves the global `AGENTS.md` behavior and `30.0.0` artifact unchanged; Nature, the historical 31-child stress test, and the existing global-rule acceptance were not rerun.

## Publication

- Source release commit: `5e06645`; project version and annotated source tag: `v30.1.0`.
- Maintainer Skill installation: complete and byte-equivalent to the release source.
- GitHub Release: <https://github.com/Taurusxw/agentmd-plan/releases/tag/v30.1.0>.
- The separate Skills distribution repository remains an independent publication target and was not changed by this source-repository release.
- The local checkout retains only the latest release record and local tag; Git history and GitHub historical tags/Releases remain intact.
