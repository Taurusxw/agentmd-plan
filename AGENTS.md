# Project AGENTS.md

本项目维护可移植的全局 `AGENTS.md` 纲要和 `seer-codex-rules` Skill。文档中的 `<codex-home>` 表示 Codex 配置目录，通常是 `$CODEX_HOME` 或用户目录下的 `.codex`。

## 项目目标

提供结构化、可验证、低 token 的 Codex 规则治理方案，使全局规则保持精简，详细流程由 Skill 按需加载。

## 目录结构

- `artifacts/`：可审查的全局 `AGENTS.md` 候选和补丁说明。
- `skills/seer-codex-rules/`：可安装、可维护的 Skill 源码。
- `docs/`：公开项目状态、索引和必要开发留痕。
- `VERSION`：当前项目发布版本。

## 工作规则

1. 全局规则先在 `artifacts/` 形成候选，再由使用者审查并安装。
2. Skill 源码以 `skills/seer-codex-rules/` 为公开事实来源；实质修改必须同步相关 reference、脚本和验证。
3. 文档和示例使用 `<codex-home>`、`<project-root>`、`<user-home>` 等占位符，不提交本机用户名、私有目录或当前机器状态。
4. 不提交历史私有备份、凭据、状态快照、缓存或包含机器特定信息的二进制包。
5. 规则版本遵守 `MAJOR.MINOR.PATCH`；只修改 Skill 时不自动推进全局 `AGENTS.md` 版本。
6. L2 以上实质开发在现有 `docs/progress/rounds/` 中留下最小可恢复记录；不为只读检查制造 round。
7. 正式发布时，`VERSION`、Git tag、GitHub Release 和 `docs/progress/releases/vx.y.z/` 必须一致；发布包含新全局纲要时，其版本也必须一致。

## 验证与完成标准

- Skill 通过结构校验、Python 语法检查、reference 路由、结构热点脚本测试和模板残留检查。
- 全局候选通过体量、版本、日期和语义覆盖检查。
- 发布前运行秘密扫描、私有路径扫描、`git diff --check` 和 GitHub 元数据检查。
- 最终说明列出改动、版本动作、测试、留痕和残留风险。

## Git 与公开边界

1. 默认分支为 `main`，公开远端为 GitHub；推送前只暂存当前任务文件。
2. 不改写已公开历史，除非安全事件需要且维护者明确批准。
3. `LICENSE`、`README.md`、`CONTRIBUTING.md` 和 `SECURITY.md` 是公开发布必需文件。
4. 发现真实秘密时先撤销凭据，再处理历史；删除当前文件不足以消除泄露。
5. 公开仓库不代替用户本地备份，使用者应在自己的私有位置保存 live 状态和历史快照。
