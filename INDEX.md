# 技能索引 INDEX

> 按「你现在的处境」检索，不是按目录顺序。全部 **35 个技能**。

- 想了解仓库怎么组织、怎么新增技能 → 看 [`README.md`](README.md) 与 [`CONTRIBUTING.md`](CONTRIBUTING.md)
- 只想找一个能用的技能 → 从这里往下查

---

## 一、速查路由表

### 我有个想法，还没验证

| 你的处境 | 用哪个 |
| --- | --- |
| 新系统 / 内部工具立项，开工前要摸清业务现状、一期范围、能不能复用开源底座 | [`01-discover/analyze-prebuild-needs`](01-discover/analyze-prebuild-needs/SKILL.md) |
| 「朋友都说好」「8 个人都说会用」 | [`01-discover/pain-point-discovery`](01-discover/pain-point-discovery/SKILL.md) |
| 要设计用户访谈提纲 / 做礼宾测试 | [`01-discover/pain-point-discovery`](01-discover/pain-point-discovery/SKILL.md) |
| 想法还很模糊，需要先把意图和需求探清楚 | [`01-discover/brainstorming`](01-discover/brainstorming/SKILL.md) |
| 要把想法落成提案、功能工单或缺陷单 | [`01-discover/project-planner`](01-discover/project-planner/SKILL.md) |

### 要定方案了

| 你的处境 | 用哪个 |
| --- | --- |
| 有个具体功能提议（或 demo 做起来很快、竞品已上线），要判断值不值得投入 | [`03-build/evaluate-feature-value`](03-build/evaluate-feature-value/SKILL.md) |
| 要算这个功能的增量效益、持续成本与误判代价 | [`03-build/evaluate-feature-value`](03-build/evaluate-feature-value/SKILL.md) |
| 只需要规则的场景却上了 AI / 上了大模型 | [`03-build/evaluate-feature-value`](03-build/evaluate-feature-value/SKILL.md) |
| 「半年全做完」、功能列表在膨胀、不知第一版砍到什么程度 | [`03-build/mvp-scoping`](03-build/mvp-scoping/SKILL.md) |
| 要写实现计划 / 拆多步任务 | [`02-design/writing-plans`](02-design/writing-plans/SKILL.md) |
| 任务跨多轮、`/clear` 后还想接着做 | [`02-design/planning-with-files`](02-design/planning-with-files/SKILL.md) |
| 要定前后端架构分层、领域边界 | [`02-design/architecture-patterns`](02-design/architecture-patterns/SKILL.md) |
| 要出一份架构设计文档 / 技术方案 | [`02-design/architecture-doc-writer`](02-design/architecture-doc-writer/SKILL.md) |
| 要做界面、页面、组件，且不想有 AI 味 | [`02-design/frontend-design`](02-design/frontend-design/SKILL.md) |
| 需要 UI/UX 设计参考与组件选型 | [`02-design/ui-ux-pro-max`](02-design/ui-ux-pro-max/SKILL.md) |

### 开始写了

| 你的处境 | 用哪个 |
| --- | --- |
| 要写功能或修 bug，还没写实现代码 | [`03-build/test-driven-development`](03-build/test-driven-development/SKILL.md) |
| 有写好的计划要逐步执行 | [`03-build/executing-plans`](03-build/executing-plans/SKILL.md) |
| 分支怎么切、提交怎么写、MR 怎么走 | [`03-build/git`](03-build/git/SKILL.md) |
| 要写日志 / 审查日志代码 / 做脱敏 | [`03-build/logging-standards`](03-build/logging-standards/SKILL.md) |
| 要写或优化提示词、定制指令 | [`03-build/prompt-engineering-expert`](03-build/prompt-engineering-expert/SKILL.md) |
| 要做复杂的前端 HTML artifact（React/Tailwind/shadcn） | [`03-build/web-artifacts-builder`](03-build/web-artifacts-builder/SKILL.md) |

### 出问题了 / 要验了

| 你的处境 | 用哪个 |
| --- | --- |
| 遇到 bug、测试失败、行为不符预期 | [`04-verify/systematic-debugging`](04-verify/systematic-debugging/SKILL.md) |
| 功能做完了，合并前要确认达标 | [`04-verify/requesting-code-review`](04-verify/requesting-code-review/SKILL.md) |
| 要从需求文档/接口文档生成测试用例（Excel） | [`04-verify/auto-testcase-generator`](04-verify/auto-testcase-generator/SKILL.md) |
| 要按 Web 规范审查 UI、可访问性、UX | [`04-verify/web-design-guidelines`](04-verify/web-design-guidelines/SKILL.md) |

### 上线了，数据回来了

| 你的处境 | 用哪个 |
| --- | --- |
| 「早期数据还不错」「累计注册 100 人」「平均打开 1.2 次」 | [`04-verify/value-validation`](04-verify/value-validation/SKILL.md) |
| 要判断继续投 / 转向 / 停掉 | [`04-verify/value-validation`](04-verify/value-validation/SKILL.md) |
| 要算这门生意的客单价、CAC、LTV、天花板 | [`05-business/business-model-fluency`](05-business/business-model-fluency/SKILL.md) |
| 要摸清一个陌生行业的钱怎么流动 | [`05-business/business-model-fluency`](05-business/business-model-fluency/SKILL.md) |
| 要分析某家 A 股公司基本面 / 财报排雷 | [`05-business/a-share-fundamentals`](05-business/a-share-fundamentals/SKILL.md) |

### 上线之后，系统要一直活着

| 你的处境 | 用哪个 |
| --- | --- |
| 服务器连不上了 / 数据库崩了 / 网站打不开 | [`06-operate/it-ops-personal`](06-operate/it-ops-personal/SKILL.md) |
| 怀疑被入侵、数据可能泄露，不知道先取证还是先处置 | [`06-operate/it-ops-personal`](06-operate/it-ops-personal/SKILL.md) |
| 要定备份策略、做恢复演练、确认「备份能不能真恢复」 | [`06-operate/it-ops-personal`](06-operate/it-ops-personal/SKILL.md) |
| 要做安全基线检查、漏洞修补、等保/数据合规自查 | [`06-operate/it-ops-personal`](06-operate/it-ops-personal/SKILL.md) |
| 要配监控告警、做日志检索、健康巡检与根因分析 | [`06-operate/it-ops-personal`](06-operate/it-ops-personal/SKILL.md) |

### 要交付东西了 / 要管技能本身

| 你的处境 | 用哪个 |
| --- | --- |
| 要产出 Word / PDF / PPT / Excel | [`90-docs/docx`](90-docs/docx/SKILL.md) · [`90-docs/pdf`](90-docs/pdf/SKILL.md) · [`90-docs/pptx`](90-docs/pptx/SKILL.md) · [`90-docs/xlsx`](90-docs/xlsx/SKILL.md) |
| 要写用户指南、教程、知识库、上手材料 | [`90-docs/technical-writer`](90-docs/technical-writer/SKILL.md) |
| 要造一个新技能 / 优化已有技能 / 跑 eval | [`00-meta/skill-creator`](00-meta/skill-creator/SKILL.md) |
| 想找有没有现成的技能可装 | [`00-meta/find-skills`](00-meta/find-skills/SKILL.md) |
| 跨会话记住项目上下文、上下文快满了 | [`00-meta/memory-bank`](00-meta/memory-bank/SKILL.md) |
| 要把 DSH 插件发到插件市场 | [`00-meta/dsh-plugin-publish`](00-meta/dsh-plugin-publish/SKILL.md) |

---

## 二、全清单（按阶段）

### 00-meta — 元能力（4）

| 技能 | 别名 / 备注 | 触发场景 |
| --- | --- | --- |
| [`00-meta/skill-creator`](00-meta/skill-creator/SKILL.md) | `skill-creator` | 从零造技能、改技能、跑 eval、优化 description 的触发准确率 |
| [`00-meta/find-skills`](00-meta/find-skills/SKILL.md) | `find-skills` | 「有没有能实现 X 的技能」、想扩展能力 |
| [`00-meta/memory-bank`](00-meta/memory-bank/SKILL.md) | `memory-bank` | 「记住这个」「接着上次继续」「保存进度」「还剩多少上下文」 |
| [`00-meta/dsh-plugin-publish`](00-meta/dsh-plugin-publish/SKILL.md) | `dsh-plugin-publish` | 发布 DSH 插件、插件市场还是旧版本、改 index.json |

### 01-discover — 发现真问题（4）

| 技能 | 别名 / 备注 | 触发场景 |
| --- | --- | --- |
| [`01-discover/analyze-prebuild-needs`](01-discover/analyze-prebuild-needs/SKILL.md) | [报告模板](01-discover/analyze-prebuild-needs/references/kickoff-report.md) · [底座检索与核验手册](01-discover/analyze-prebuild-needs/references/foundation-research.md) | 系统立项、一期范围、先找开源底座或核验指定平台，按证据给开工建议 |
| [`01-discover/pain-point-discovery`](01-discover/pain-point-discovery/SKILL.md) | **新增** | 判断痛点真伪、设计访谈、承诺阶梯、礼宾测试、写失败判据 |
| [`01-discover/brainstorming`](01-discover/brainstorming/SKILL.md) | `brainstorming` | 任何创造性工作之前，先探清意图、需求与设计 |
| [`01-discover/project-planner`](01-discover/project-planner/SKILL.md) | 市场 slug `project-planner` | 「提个 bug」「我有个想法」「规划这个功能」、大功能拆阶段 |

### 02-design — 定义方案（6）

| 技能 | 别名 / 备注 | 触发场景 |
| --- | --- | --- |
| [`02-design/architecture-patterns`](02-design/architecture-patterns/SKILL.md) | `architecture-patterns` | Clean / Hexagonal / DDD、拆单体为限界上下文、解依赖环 |
| [`02-design/architecture-doc-writer`](02-design/architecture-doc-writer/SKILL.md) | `architecture-doc-writer` | 写 TDD/SAD、系统设计方案、评审用技术说明 |
| [`02-design/writing-plans`](02-design/writing-plans/SKILL.md) | `writing-plans` | 有需求但还没定多步实现计划 |
| [`02-design/planning-with-files`](02-design/planning-with-files/SKILL.md) | `planning-with-files` | 复杂任务、研究型任务、预计 >5 次工具调用，`/clear` 后可恢复 |
| [`02-design/frontend-design`](02-design/frontend-design/SKILL.md) | `frontend-design` | 建页面/组件/仪表盘/海报，避免通用 AI 审美 |
| [`02-design/ui-ux-pro-max`](02-design/ui-ux-pro-max/SKILL.md) | `ui-ux-pro-max` | 可检索的 UI/UX 设计知识库 |

### 03-build — 做出 MVP（8）

| 技能 | 别名 / 备注 | 触发场景 |
| --- | --- | --- |
| [`03-build/evaluate-feature-value`](03-build/evaluate-feature-value/SKILL.md) | 与 `01-discover/analyze-prebuild-needs` 互为上下游 | 功能级投入决策：写价值假设与对照方案、算增量效益与持续成本、设计最小验证、做 / 先验证 / 改用简方案 / 暂缓 |
| [`03-build/mvp-scoping`](03-build/mvp-scoping/SKILL.md) | **新增** | 砍范围、假设排序、写验收阈值、纠正「先开发后验证」 |
| [`03-build/test-driven-development`](03-build/test-driven-development/SKILL.md) | `test-driven-development` | 写实现代码之前 |
| [`03-build/executing-plans`](03-build/executing-plans/SKILL.md) | `executing-plans` | 带评审检查点地执行成文计划 |
| [`03-build/git`](03-build/git/SKILL.md) | 市场 slug `git-xywh` | 三主干 + 五类临时分支、提交/MR 规范、安全合并与恢复 |
| [`03-build/logging-standards`](03-build/logging-standards/SKILL.md) | `logging-standards` | JSON 结构化日志、级别规范、脱敏、慢查询告警 |
| [`03-build/prompt-engineering-expert`](03-build/prompt-engineering-expert/SKILL.md) | 市场 slug `prompt-engineering-expert` | 提示词工程、自定义指令、提示词优化 |
| [`03-build/web-artifacts-builder`](03-build/web-artifacts-builder/SKILL.md) | `web-artifacts-builder` | 多组件 HTML artifact（需状态管理/路由/shadcn） |

### 04-verify — 验证价值（5）

| 技能 | 别名 / 备注 | 触发场景 |
| --- | --- | --- |
| [`04-verify/value-validation`](04-verify/value-validation/SKILL.md) | **新增** | 指标口径、留存曲线、平均值陷阱、预注册判据、继续/转向/停 |
| [`04-verify/systematic-debugging`](04-verify/systematic-debugging/SKILL.md) | `systematic-debugging` | 任何 bug / 测试失败 / 异常行为，在提修复方案之前 |
| [`04-verify/requesting-code-review`](04-verify/requesting-code-review/SKILL.md) | `requesting-code-review` | 完成任务、实现大功能、合并之前 |
| [`04-verify/auto-testcase-generator`](04-verify/auto-testcase-generator/SKILL.md) | frontmatter `name: testcase-generator`，市场 slug `auto-testcase-generator` | 从需求/接口文档生成结构化 Excel 测试用例 |
| [`04-verify/web-design-guidelines`](04-verify/web-design-guidelines/SKILL.md) | `web-design-guidelines` | 审 UI 代码、可访问性、UX、站点最佳实践 |

### 05-business — 看懂生意（2）

| 技能 | 别名 / 备注 | 触发场景 |
| --- | --- | --- |
| [`05-business/business-model-fluency`](05-business/business-model-fluency/SKILL.md) | **新增** | 一周速通行业、产业链钱流、五个数字（ARPU/CAC/LTV/毛利率/回本）、天花板、Go/Pivot/No-Go |
| [`05-business/a-share-fundamentals`](05-business/a-share-fundamentals/SKILL.md) | `a-share-fundamentals` | A 股基本面、财报分析、ROE、财务排雷、AKShare 采集 |

### 06-operate — 长期运维（1）

| 技能 | 别名 / 备注 | 触发场景 |
| --- | --- | --- |
| [`06-operate/it-ops-personal`](06-operate/it-ops-personal/SKILL.md) | `it-ops-personal`，来源 skillhub 后经个人整理（见目录内 `CHANGES.md`） | 服务器/数据库故障排查、SSH 与远程运维、安全基线加固、漏洞修复、备份与恢复演练、监控告警、日志检索、应急响应与入侵溯源、证据保全、数据合规与个人信息保护自查、运维自动化 |

### 90-docs — 交付物（5）

| 技能 | 别名 / 备注 | 触发场景 |
| --- | --- | --- |
| [`90-docs/docx`](90-docs/docx/SKILL.md) | `docx` | 任何 `.docx` 的创建、读取、编辑、格式化 |
| [`90-docs/pdf`](90-docs/pdf/SKILL.md) | `pdf` | 任何 `.pdf` 的读取、拆分、合并、水印、表单、OCR |
| [`90-docs/pptx`](90-docs/pptx/SKILL.md) | `pptx` | 任何 `.pptx` 的创建、解析、编辑、拆分合并 |
| [`90-docs/xlsx`](90-docs/xlsx/SKILL.md) | `xlsx` | 任何 `.xlsx`/`.csv`/`.tsv` 的读写、公式、图表、清洗 |
| [`90-docs/technical-writer`](90-docs/technical-writer/SKILL.md) | `technical-writer` | 用户指南、how-to、教程、知识库 |

---

## 三、端到端组合剧本

技能不是孤立用的。下面是三个真实链路的推荐组合。

### 剧本 A：从零做一个新产品

```
01-discover/analyze-prebuild-needs    系统级：还原业务问题、一期范围、底座复用、开工建议
        ↓
01-discover/pain-point-discovery      先证明痛是真的、有人会付钱
        ↓
03-build/evaluate-feature-value       每个具体功能：值不值得做，还是改用简方案
        ↓
03-build/mvp-scoping                  砍到一个闭环，把致命假设排到最前
        ↓
02-design/writing-plans               拆成可执行的里程碑
        ↓
03-build/test-driven-development      写代码（executing-plans 管节奏）
        ↓
04-verify/systematic-debugging        出问题先定位，别猜
        ↓
04-verify/requesting-code-review      合并前把关
        ↓
04-verify/value-validation            上线看留存曲线，判断去留
        ↓
05-business/business-model-fluency    数字能不能撑起生意
   （不成立 → 回到 mvp-scoping 或 pain-point-discovery）
```

### 剧本 B：接了个陌生行业的项目

```
05-business/business-model-fluency    一周速通：钱流图 + 五个数字
        ↓
01-discover/pain-point-discovery      找到真实痛点与付费人
        ↓
02-design/architecture-doc-writer     产出技术方案
        ↓
03-build/executing-plans              按计划推进
        ↓
90-docs/*                             交付文档与表格
```

### 剧本 C：只想让 AI 帮我把活干好

```
00-meta/memory-bank                   让上下文跨会话不丢
        ↓
01-discover/brainstorming             需求没说清之前别动手
        ↓
02-design/planning-with-files         复杂任务用文件跟踪进度
        ↓
03-build/prompt-engineering-expert    提示词写不好时优化
        ↓
00-meta/skill-creator                 重复劳动 → 沉淀成新技能
```

---

## 四、找不到想要的？

1. 用 [`00-meta/find-skills`](00-meta/find-skills/SKILL.md) 搜现成的
2. 没有就自己造：[`00-meta/skill-creator`](00-meta/skill-creator/SKILL.md)，规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md)
