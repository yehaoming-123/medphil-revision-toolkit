import shutil
from pathlib import Path

from scripts.generate_revision_log import generate_revision_log


REQUIRED_DELIVERABLES = {
    "revised_manuscript.docx",
    "revision_log.md",
    "journal_routing_report.md",
    "journal_fit_report.md",
    "author_confirmation_needed.md",
}
JOURNALS = {"mhcp", "jme", "bioethics", "jmp"}
JOURNAL_NAMES = {
    "mhcp": "MHCP",
    "jme": "JME",
    "bioethics": "Bioethics",
    "jmp": "JMP",
}


class DeliveryBundleError(ValueError):
    pass


def _as_list(value, field):
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise DeliveryBundleError(f"{field} must be a list of strings")
    return value


def _validate_records(routing, fit):
    ranking = routing.get("ranking")
    if not isinstance(ranking, list) or len(ranking) != 4:
        raise DeliveryBundleError("routing ranking must contain four journals")
    journals = {item.get("journal") for item in ranking if isinstance(item, dict)}
    ranks = {item.get("rank") for item in ranking if isinstance(item, dict)}
    if journals != JOURNALS or ranks != {1, 2, 3, 4}:
        raise DeliveryBundleError("routing ranking must cover all four journals once")
    for item in ranking:
        for field in ("fit_reasons", "mismatch_reasons", "evidence_limits"):
            _as_list(item.get(field), f"routing.{field}")

    target = routing.get("recommended_target")
    if target not in JOURNALS or fit.get("target_journal") != target:
        raise DeliveryBundleError("routing target and fit target must match")
    if routing.get("alternative") not in JOURNALS - {target}:
        raise DeliveryBundleError("routing alternative is invalid")
    _as_list(routing.get("ranking_change_conditions"), "ranking_change_conditions")
    for field in (
        "official_requirements",
        "observed_tendencies",
        "abstract_limited",
        "editorial_inferences",
        "remaining_risks",
        "pre_submission_checks",
    ):
        _as_list(fit.get(field), f"fit.{field}")


def _join(items):
    return "；".join(item.replace("|", "\\|") for item in items) or "无"


def _routing_report(routing):
    lines = [
        "# 期刊路由报告",
        "",
        "| 排名 | 期刊 | 匹配理由 | 不匹配理由 | 证据限制 |",
        "|---:|---|---|---|---|",
    ]
    for item in sorted(routing["ranking"], key=lambda row: row["rank"]):
        lines.append(
            f"| {item['rank']} | {JOURNAL_NAMES[item['journal']]} | "
            f"{_join(item['fit_reasons'])} | {_join(item['mismatch_reasons'])} | "
            f"{_join(item['evidence_limits'])} |"
        )
    lines.extend(
        [
            "",
            f"- 推荐目标：**{JOURNAL_NAMES[routing['recommended_target']]}**",
            f"- 备选期刊：**{JOURNAL_NAMES[routing['alternative']]}**",
            "- 可能改变排序的稿件变化：" + _join(routing["ranking_change_conditions"]),
        ]
    )
    return "\n".join(lines) + "\n"


def _section(lines, title, label, items):
    lines.extend(["", f"## {title}", "", f"证据标签：`{label}`", ""])
    lines.extend(f"- {item}" for item in items) if items else lines.append("- 无。")


def _fit_report(fit):
    lines = [
        "# 目标期刊适配报告",
        "",
        f"- 目标期刊：**{JOURNAL_NAMES[fit['target_journal']]}**",
    ]
    _section(lines, "当前官方要求", "official_requirement", fit["official_requirements"])
    _section(lines, "公开语料观察", "observed_tendency", fit["observed_tendencies"])
    _section(lines, "摘要级有限观察", "abstract_limited", fit["abstract_limited"])
    _section(lines, "编辑判断", "editorial_inference", fit["editorial_inferences"])
    _section(lines, "剩余风险", "editorial_inference", fit["remaining_risks"])
    _section(lines, "投稿前检查", "official_requirement", fit["pre_submission_checks"])
    return "\n".join(lines) + "\n"


def _confirmation_report(application_record, unresolved_choices):
    items = list(application_record.get("author_confirmation", []))
    items.extend(unresolved_choices or [])
    lines = ["# 需要作者确认", ""]
    if not items:
        lines.append("当前无需作者确认。")
    else:
        for item in items:
            if isinstance(item, dict):
                location = item.get("paragraph_index", item.get("location", "未指定位置"))
                reason = item.get("reason", item.get("question", "需要作者判断"))
                lines.append(f"- **{location}**：{reason}")
            else:
                lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def build_delivery_bundle(
    output_dir,
    revised_manuscript,
    before_manifest,
    after_manifest,
    application_record,
    routing,
    fit,
    unresolved_choices=None,
):
    output = Path(output_dir)
    manuscript = Path(revised_manuscript)
    if manuscript.suffix.casefold() != ".docx" or not manuscript.is_file():
        raise DeliveryBundleError("revised manuscript must be an existing DOCX")
    if output.exists():
        raise FileExistsError(f"bundle output already exists: {output.resolve()}")
    _validate_records(routing, fit)

    changes = [
        {
            "location": f"段落 {item['paragraph_index']}",
            "change": item.get("reason", "已按修订规范修改。"),
        }
        for item in application_record.get("applied", [])
    ]
    violations = application_record.get("protected_field_violations", [])
    output.mkdir(parents=True)
    try:
        shutil.copy2(manuscript, output / "revised_manuscript.docx")
        (output / "revision_log.md").write_text(
            generate_revision_log(
                before_manifest,
                after_manifest,
                changes,
                violations,
                language="zh",
            ),
            encoding="utf-8",
        )
        (output / "journal_routing_report.md").write_text(
            _routing_report(routing), encoding="utf-8"
        )
        (output / "journal_fit_report.md").write_text(
            _fit_report(fit), encoding="utf-8"
        )
        (output / "author_confirmation_needed.md").write_text(
            _confirmation_report(application_record, unresolved_choices),
            encoding="utf-8",
        )
        actual = {path.name for path in output.iterdir()}
        if actual != REQUIRED_DELIVERABLES:
            raise DeliveryBundleError("delivery bundle has missing or unexpected files")
        return {name: output / name for name in sorted(REQUIRED_DELIVERABLES)}
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise
