# Agentmd Plan

Agentmd Plan 是一套可移植的 Codex 规则治理方案：全局 `AGENTS.md` 只保留始终生效的纲要，复杂流程由 `seer-codex-rules` Skill 按任务类型加载。

## 包含内容

- `artifacts/AGENTS-27.6.0.md`：精简的全局规则纲要候选。
- `skills/seer-codex-rules/`：规则设计、版本治理、文档治理、round/phase/release、验证与低 token guardrail Skill。
- `docs/`：公开项目状态、文档索引和发布记录。

## 设计原则

1. 全局文件只保留任务分级、强制 Skill 门禁、安全底线和完成检查。
2. 详细规则按 reference 模块化，普通任务只加载当前需要的模块。
3. 可确定的同步、体量、路由和状态检查交给脚本，不依赖人工记忆。
4. 本机路径、私有备份和 live 状态不进入公开仓库。

## 安装

1. 将 `skills/seer-codex-rules/` 复制到 `<codex-home>/skills/seer-codex-rules/`。
2. 审阅 `artifacts/AGENTS-27.6.0.md`，确认适合自己的工作方式后，再合并或安装到 `<codex-home>/AGENTS.md`。
3. 项目级规则只保存项目事实，不复制全局全文。

`<codex-home>` 通常是环境变量 `CODEX_HOME` 指向的目录；未设置时一般使用 `<user-home>/.codex`。

## 校验

在仓库根目录运行：

```powershell
python skills/seer-codex-rules/scripts/measure_rules.py --strict artifacts/AGENTS-27.6.0.md
python -m py_compile skills/seer-codex-rules/scripts/guardrail_check.py skills/seer-codex-rules/scripts/measure_rules.py skills/seer-codex-rules/scripts/snapshot_state.py
python skills/seer-codex-rules/scripts/guardrail_check.py --project . --global-agents artifacts/AGENTS-27.6.0.md --downloads-agents artifacts/AGENTS-27.6.0.md --skill skills/seer-codex-rules --json
```

安装到个人环境后，可以使用 `snapshot_state.py --write` 建立私有状态清单和 Skill 快照。生成的状态与备份应保存在私有项目中，不提交到公开仓库。

## 隐私边界

公开仓库不包含个人机器路径、历史私有备份、live 状态 manifest 或凭据。公开前保留的私有历史应存放在仓库外。

## 参与和安全

提交改进前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请按 [SECURITY.md](SECURITY.md) 私下报告。

## License

[MIT](LICENSE)
