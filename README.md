# MedPhil Revision Toolkit

## 基本信息

- 项目编号：`Project_038`
- 项目目录：`Project_038_medphil_revision_toolkit`
- 创建日期：`2026-07-11`
- 当前状态：`阶段 1 已完成`

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

## 安装开发依赖

```powershell
python -m pip install -r requirements.txt
```

项目目前作为本地插件源进行开发。公共 GitHub 仓库和插件目录发布将在完成 DOCX 阶段及发布前评测后配置。

## 验证

```powershell
python -m unittest discover -s evals/tests -v
python scripts/validate_journal_pack.py journal-packs/mhcp
python scripts/validate_journal_pack.py journal-packs/jme
python scripts/validate_journal_pack.py journal-packs/bioethics
python scripts/validate_journal_pack.py journal-packs/jmp
```

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
- [ ] 实现 DOCX 安全管线。

## 已知限制

- 阶段 1 不读取或修改 DOCX；相关功能属于阶段 2。
- 最近文章语料画像尚未系统构建，现有 `editorial_profile.md` 仅包含明确标注的初步编辑推断。
- 项目在独立 `feature/foundation` Git 分支中开发；按用户要求在全部构建完成后统一提交。
