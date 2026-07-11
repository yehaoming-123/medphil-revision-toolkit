from pathlib import Path


def _display_name(value):
    return Path(value).name if value else ""


def generate_revision_log(before, after, changes, violations, language="en"):
    status = "FAILED" if violations else "PASSED"
    if language == "zh":
        status = "失败" if violations else "通过"
        lines = [
            "# 修改日志",
            "",
            f"- 原稿：`{_display_name(before.get('path', ''))}`",
            f"- 原稿 SHA-256：`{before.get('sha256', '')}`",
            f"- 修订稿：`{_display_name(after.get('path', ''))}`",
            f"- 修订稿 SHA-256：`{after.get('sha256', '')}`",
            f"- 受保护字段状态：**{status}**",
            "",
            "## 修改",
            "",
        ]
        if changes:
            lines.extend(
                f"- **{item['location']}**：{item['change']}" for item in changes
            )
        else:
            lines.append("- 未记录正文修改。")
        lines.extend(["", "## 受保护字段异常", ""])
        if violations:
            lines.extend(f"- `{violation}`" for violation in violations)
        else:
            lines.append("- 无。")
        return "\n".join(lines) + "\n"
    if language != "en":
        raise ValueError("language must be 'en' or 'zh'")
    lines = [
        "# Revision Log",
        "",
        f"- Source: `{_display_name(before.get('path', ''))}`",
        f"- Source SHA-256: `{before.get('sha256', '')}`",
        f"- Output: `{_display_name(after.get('path', ''))}`",
        f"- Output SHA-256: `{after.get('sha256', '')}`",
        f"- Protected-field status: **{status}**",
        "",
        "## Changes",
        "",
    ]
    if changes:
        lines.extend(
            f"- **{item['location']}**: {item['change']}" for item in changes
        )
    else:
        lines.append("- No prose changes recorded.")
    lines.extend(["", "## Protected-field violations", ""])
    if violations:
        lines.extend(f"- `{violation}`" for violation in violations)
    else:
        lines.append("- None.")
    return "\n".join(lines) + "\n"
