# AGENTS.md 27.8.0 候选补丁说明

本次版本动作：`27.7.0 -> 27.8.0`，属于 `MINOR`。

## 变更原因

现有边界条件准入和验收预算在普通任务中有效，但持续 Goal 缺少冻结的完成定义。开放目标在自动续跑中会把新发现不断解释成 `required work`，造成边界开发、验收工具加固和重复验证循环。

## 修改内容

1. 全局验证规则增加 Goal 模式完成契约门禁。
2. Skill 新增 `goal-mode-closure.md`，将结果、3-5 条完成条件、非目标、验证预算和结束规则保存在 Goal objective。
3. 新发现只有在契约失败、当前改动回归或重大安全风险时才自动进入当前目标。
4. 增加一次探测、禁止递归加固、无进展断路器和自动 `complete` 规则。
5. guardrail 强制检查全局门禁与 Goal reference 的关键锚点。
6. 新增 guardrail 单元测试，并将测试入口扩展为全部 `test_*.py`。

## 低 Token 边界

- 普通非 Goal 任务不加载 Goal reference。
- Goal 契约保存在目标对象中，不要求每轮读取历史 round 或新建项目文档。
- 续跑和结束只输出一行完成状态；可选发现最多列 3 条。
- 不新增 Goal 专用脚本或每轮扫描。

## 验证要求

- 候选通过严格体量、版本、日期、门禁和覆盖锚点检查。
- Skill 通过结构校验、reference 路由、Python 编译和全部单元测试。
- 项目、活动 Skill 和私有快照 tree hash 一致。
- GitHub 分支、tag、Release 和远端 `VERSION` 一致。
