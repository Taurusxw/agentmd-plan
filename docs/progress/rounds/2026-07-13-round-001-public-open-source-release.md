# 2026-07-13 Round 001: public open-source release

## Status

completed

## Goal

将 Agentmd Plan 净化为可安全公开的 GitHub 仓库，并保留一份仓库外私有恢复包。

## Background

原始本地项目包含机器路径、历史备份、live 状态和 Skill ZIP，不适合直接公开。维护者明确批准公开、采用 MIT License，并重建干净历史。

## Scope

- 保留可复用的 `27.6.0` 全局纲要和 Skill 源码。
- 移除公开树中的私有备份、机器状态和二进制 Skill 快照。
- 将路径和脚本默认值改为跨机器形式。
- 增加开源许可证、贡献和安全文档。
- 重建单一公开根提交，创建公开 GitHub 仓库并验证元数据。

## Key Decisions

- 私有历史通过仓库外 Git bundle 保留，不推送到 GitHub。
- 公开仓库不包含个人机器路径或旧会话留痕。
- 使用 MIT License。
- 不在首次发布中增加 CodeQL、Issue 模板、规则集等额外治理。

## Tests And Verification

- 运行秘密、私有路径和高风险文件扫描。
- 校验 Skill 结构、Python 语法、reference 路由和全局候选体量。
- 校验 JSON、Git diff、单一公开历史、GitHub visibility、license 和默认分支。

## Risks And Follow-Up

- 自动扫描不能证明所有内容绝对无隐私风险；发布范围已限制为可复用源码和必要文档。
- 更复杂的 GitHub 安全策略可在项目形成外部贡献后再增加。

## Next Step

根据公开使用反馈迭代安装、测试和跨平台行为。
