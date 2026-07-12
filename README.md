# MedPhil Revision Toolkit

## 基本信息

- 项目编号：`Project_038`
- 项目目录：`Project_038_medphil_revision_toolkit`
- 创建日期：`2026-07-11`
- 当前状态：`v0.1.0-rc.1 发布候选`

## 项目目标

构建一个零服务器、可本地安装、可测试和可公开贡献的 Codex 插件，用于英文医学哲学、生命伦理学和医学人文论文的期刊路由、论证审查与安全修稿。

项目首先服务真实个人修稿工作流，同时从第一版起采用成熟开源工具架构。v0.1 支持 *Medicine, Health Care and Philosophy*、*Journal of Medical Ethics*、*Bioethics* 与 *The Journal of Medicine and Philosophy*。

## v0.1 范围

### 包含

- 英文 `.docx` 稿件安全读取与结构检查。
- 医学哲学和生命伦理学通用修稿内核。
- MHCP、JME、Bioethics、JMP 四刊路由和独立适配包。
- 干净修订稿、中文修改日志、期刊适配报告和作者确认清单。
- 来源登记、版权边界、自动校验和最小评测体系。

### 不包含

- Word 原生修订痕迹。
- 网页应用、服务器、数据库或用户账号系统。
- 录用概率预测、AI 写作比例检测或付费墙绕过。
- 保存未发表稿件或真实患者身份信息。

## 阶段 1 能力

- 可验证的 Codex 插件清单和两个 Agent Skills。
- 四个相互隔离的期刊包：MHCP、JME、Bioethics、JMP。
- 期刊来源类型、HTTPS URL 和 90 天时效校验。
- 不声称录用概率的透明离线路由回归基线。
- 编辑安全、版权边界和社区贡献规范。

## 阶段 2 能力

- 为 DOCX 生成包含 SHA-256、标题、段落、表格、分节、引用与参考文献指纹的结构清单。
- 对邮箱、电话号码、中国身份证号形态和 `MRN:` 标记执行保守的敏感标识门控。
- 创建不覆盖原稿的工作副本，并在复制后校验文件哈希。
- 冻结引用、参考文献指纹、表格数、分节数、批注部件和脚注部件等受保护字段。
- 生成不暴露本机绝对路径的确定性 Markdown 修改日志。
- 提供两页合成医学哲学论文、固定工作副本和端到端回归评测。

## 阶段 3 能力

- 把语义修稿判断记录为可审阅的 JSON 修订规范，而不是让模型直接改写 Word 底层结构。
- 为每个正文段落生成稳定索引、文本哈希、节标题、引用与复杂格式保护状态。
- 仅对原文精确匹配且安全的普通段落应用修订；任何预检失败都不生成部分结果。
- 将高风险或可能改变作者立场的修改留在作者确认清单，不静默落稿。
- 生成干净修订稿、中文修改日志、四刊路由报告、期刊适配报告和作者确认清单。
- 提供 Windows 兼容的 DOCX QA 渲染器，使用标准 `file:///` 用户目录 URI，避免外部渲染器的误报。

## 安装开发依赖

```powershell
python -m pip install -r requirements.txt
```

项目已公开发布至 GitHub，当前默认分支为 `feature/foundation`。Codex 插件市场发布仍需单独配置。

## 验证

```powershell
python -m unittest discover -s evals/tests -v
python scripts/validate_journal_pack.py journal-packs/mhcp
python scripts/validate_journal_pack.py journal-packs/jme
python scripts/validate_journal_pack.py journal-packs/bioethics
python scripts/validate_journal_pack.py journal-packs/jmp
```

严格检查单篇 DOCX：

```powershell
python scripts/inspect_docx.py input/manuscript.docx --strict
```

生成安全段落清单、校验并应用结构化修订规范：

```powershell
python scripts/build_revision_inventory.py input/manuscript.docx
python scripts/validate_revision_spec.py revision_spec.json --source input/manuscript.docx
python scripts/apply_revision_spec.py input/manuscript.docx output/revised_manuscript.docx revision_spec.json
```

`revision_spec.json` 必须符合 [`references/revision_spec_schema.json`](references/revision_spec_schema.json)。完整交付包由 `$medphil-revision` 按 [`references/report_contract.md`](references/report_contract.md) 生成。

`--strict` 发现明显敏感标识时会失败。它只是一道确定性安全门，不是语义去标识化证明；真实稿件仍需作者确认已移除患者与个人身份信息。

工作副本和受保护字段比较以 Python API 提供：

```python
from scripts.inspect_docx import inspect_docx
from scripts.protect_document import create_working_copy, compare_protected_fields

source = "input/manuscript.docx"
working = create_working_copy(source, "output/manuscript_working.docx")
violations = compare_protected_fields(inspect_docx(source), inspect_docx(working))
```

视觉回归使用 LibreOffice 和 Poppler 将 DOCX 转为 PDF/PNG；渲染文件仅用于本地质量检查，不进入公开仓库：

```powershell
python scripts/render_docx_qa.py output/revised_manuscript.docx output/rendered-pages
```

### 支持的自动修订

- 非空、无引用、无字段、无超链接、无图形且字符格式一致的普通正文段落。
- 段落索引与原文必须和当前 DOCX 清单精确一致。
- 段落样式保留，原稿永不覆盖。

### 默认拒绝的自动修订

- 标题、参考文献、引文段落、表格内文字、脚注和批注。
- 域代码、引用管理器对象、超链接、图片/绘图、混合字符格式段落。
- 可能改变作者立场且尚未确认的高风险修改。
- 加密、损坏、图片型正文或包含疑似身份信息的文件。

## 目录结构

```text
Project_038_medphil_revision_toolkit/
├── .codex-plugin/
├── skills/
├── journal-packs/
├── references/
├── evals/
├── scripts/
├── input/
├── output/
├── docs/
├── assets/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── project_log.md
```

## 设计与计划

- [v0.1 设计稿](docs/superpowers/specs/2026-07-11-medphil-revision-toolkit-design.md)
- [阶段 1 实施计划](docs/superpowers/plans/2026-07-11-medphil-foundation-implementation.md)
- [阶段 2 实施计划](docs/superpowers/plans/2026-07-11-docx-safety-implementation.md)
- [阶段 3 实施计划](docs/superpowers/plans/2026-07-11-end-to-end-revision-implementation.md)

## 数据安全

- 仅处理合成、公开授权或已充分去标识化材料。
- 原始输入不得包含真实患者身份信息。
- 未发表用户稿件不得进入公共示例或评测集。

## 验证状态

- [x] 用户确认项目目标、总体架构和 v0.1 范围。
- [x] 用户确认四本首发期刊。
- [x] 用户确认来源、版权、更新和测试原则。
- [x] 用户审阅书面设计稿。
- [x] 编写并批准阶段 1 实施计划。
- [x] 完成阶段 1 全量验证。
- [x] 完成阶段 1 统一提交。
- [x] 实现 DOCX 安全管线并通过 23 项自动化测试。
- [x] 完成 LibreOffice 视觉回归；源稿与工作副本均为 2 页且逐页哈希一致。
- [x] 完成阶段 2 统一提交。
- [x] 完成端到端安全修订、五项交付物和 2 页修订稿视觉验收。
- [x] 完成 v0.1 发布候选全量验证与统一提交。

## 已知限制

- v0.1 只自动修改结构简单且通过精确预检的普通正文段落；复杂段落失败关闭。
- 最近文章语料画像尚未系统构建，现有 `editorial_profile.md` 仅包含明确标注的初步编辑推断。
- 敏感标识门控只覆盖明确模式，不能替代作者的语义隐私审查。
- Codex 插件市场发布尚未配置。
- 项目在 `feature/foundation` 分支中维护；该分支已同步到公开 GitHub 仓库。
