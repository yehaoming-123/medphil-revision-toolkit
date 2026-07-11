from pathlib import Path


def _display_name(value):
    return Path(value).name if value else ""


def generate_revision_log(before, after, changes, violations):
    status = "FAILED" if violations else "PASSED"
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
