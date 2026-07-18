# Agentmd Plan v27.7.0

## 中文

`v27.7.0` 增加累计架构漂移治理，解决同一生产热点在多轮补丁中不断增加职责、接口和重复逻辑的问题，同时保持普通任务的低 token 路径。

### 主要内容

- 全局纲要增加重复补丁热点的 L3 升级条件和强制 Skill 路由。
- 新增 `architecture-drift.md`，按组合证据选择继续补丁、冻结新增职责或升级边界工作。
- 新增 `structure_check.py`，按需检查近期 round/Git 热点、文件规模、入口分支和同目录重复函数。
- 明确大文件不是拆分判据，避免为了结构指标制造浅层模块。
- 增加结构检查单元测试、双语说明和全局覆盖映射。

### 升级说明

同时安装 `artifacts/AGENTS-27.7.0.md` 和 `skills/seer-codex-rules/`。架构漂移检查仅在触发条件出现时运行，不应加入每个小补丁的固定流程。

## English

`v27.7.0` adds cumulative architecture-drift governance for production hotspots that keep gaining responsibilities, interface breadth, and duplicated logic across patch cycles while preserving a low-token path for ordinary work.

### Highlights

- The global outline now upgrades repeated patch hotspots with structural drift to L3 and routes them through the Skill.
- New `architecture-drift.md` guidance selects among patching, freezing new responsibility, and boundary work using combined evidence.
- New on-demand `structure_check.py` examines recent round/Git hotspots, file size, entry branches, and sibling function duplication.
- Large files are explicitly signals rather than split verdicts, preventing shallow module churn.
- Structure-check unit tests, bilingual manuals, and refreshed global coverage mappings are included.

### Upgrade Notes

Install both `artifacts/AGENTS-27.7.0.md` and `skills/seer-codex-rules/`. Run architecture-drift checks only when a trigger fires; do not add them to every tiny patch.
