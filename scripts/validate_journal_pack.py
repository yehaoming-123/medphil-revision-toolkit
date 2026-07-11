import argparse
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml


REQUIRED_FILES = {
    "profile.yaml",
    "source_registry.md",
    "official_requirements.md",
    "editorial_profile.md",
    "routing_examples.md",
    "eval_cases.yaml",
}
PROFILE_FIELDS = {
    "id",
    "name",
    "publisher",
    "scope_summary",
    "article_types",
    "fit_signals",
    "mismatch_signals",
    "official_urls",
    "checked_at",
}
EVIDENCE_TYPES = {
    "official_requirement",
    "observed_tendency",
    "editorial_inference",
    "abstract_limited",
}
SOURCE_FIELDS = {
    "claim_id",
    "claim",
    "evidence_type",
    "url",
    "checked_at",
    "applies_to",
    "status",
}
MAX_AGE_DAYS = 90


def _frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    return yaml.safe_load(text[4:end]) if end != -1 else {}


def _valid_url(value):
    parsed = urlparse(str(value))
    return parsed.scheme == "https" and bool(parsed.netloc)


def _to_date(value):
    return value if isinstance(value, date) else date.fromisoformat(str(value))


def validate_pack(pack_path, as_of=None):
    path = Path(pack_path)
    errors = []
    missing = sorted(REQUIRED_FILES - {item.name for item in path.iterdir()})
    errors.extend(f"missing file: {name}" for name in missing)
    if missing:
        return errors

    profile = yaml.safe_load(
        (path / "profile.yaml").read_text(encoding="utf-8")
    ) or {}
    for field in sorted(PROFILE_FIELDS - set(profile)):
        errors.append(f"profile missing field: {field}")
    for url in profile.get("official_urls", []):
        if not _valid_url(url):
            errors.append(f"profile has invalid official URL: {url}")

    registry = _frontmatter(
        (path / "source_registry.md").read_text(encoding="utf-8")
    )
    today = _to_date(as_of or date.today())
    for source in registry.get("sources", []):
        claim_id = source.get("claim_id", "unknown")
        for field in sorted(SOURCE_FIELDS - set(source)):
            errors.append(f"source {claim_id} missing field: {field}")
        evidence_type = source.get("evidence_type")
        if evidence_type not in EVIDENCE_TYPES:
            errors.append(
                f"source {claim_id} has invalid evidence_type: {evidence_type}"
            )
        if not _valid_url(source.get("url")):
            errors.append(f"source {claim_id} has invalid URL")
        checked_at = source.get("checked_at")
        if checked_at and (today - _to_date(checked_at)).days > MAX_AGE_DAYS:
            errors.append(f"source {claim_id} is stale")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pack")
    parser.add_argument("--as-of")
    args = parser.parse_args()
    errors = validate_pack(args.pack, as_of=args.as_of)
    for error in errors:
        print(error)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
