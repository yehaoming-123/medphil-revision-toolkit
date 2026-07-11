import argparse
import json
import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.inspect_docx import sha256_file


JOURNALS = {"mhcp", "jme", "bioethics", "jmp"}
RISK_LEVELS = {"low", "medium", "high"}
TOP_LEVEL_FIELDS = {"target_journal", "source_sha256", "revisions"}
REVISION_FIELDS = {
    "paragraph_index",
    "original_text",
    "revised_text",
    "reason",
    "risk_level",
    "author_confirmation",
}
SHA256_PATTERN = re.compile(r"^[A-Fa-f0-9]{64}$")


def _nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def validate_revision_spec(spec, expected_source_hash=None):
    if not isinstance(spec, dict):
        return ["spec_must_be_object"]

    errors = []
    missing_top = TOP_LEVEL_FIELDS - set(spec)
    errors.extend(f"missing_{field}" for field in sorted(missing_top))
    if set(spec) - TOP_LEVEL_FIELDS:
        errors.append("top_level_unknown_fields")

    if spec.get("target_journal") not in JOURNALS:
        errors.append("target_journal_invalid")

    source_hash = spec.get("source_sha256")
    if not isinstance(source_hash, str) or not SHA256_PATTERN.fullmatch(source_hash):
        errors.append("source_sha256_invalid")
    elif expected_source_hash and source_hash.casefold() != expected_source_hash.casefold():
        errors.append("source_sha256_mismatch")

    revisions = spec.get("revisions")
    if not isinstance(revisions, list):
        errors.append("revisions_must_be_array")
        return errors
    if not revisions:
        errors.append("revisions_empty")

    seen_indices = set()
    for index, revision in enumerate(revisions):
        prefix = f"revision_{index}"
        if not isinstance(revision, dict):
            errors.append(f"{prefix}_must_be_object")
            continue
        for field in sorted(REVISION_FIELDS - set(revision)):
            errors.append(f"{prefix}_missing_{field}")
        if set(revision) - REVISION_FIELDS:
            errors.append(f"{prefix}_unknown_fields")

        paragraph_index = revision.get("paragraph_index")
        if (
            not isinstance(paragraph_index, int)
            or isinstance(paragraph_index, bool)
            or paragraph_index < 0
        ):
            errors.append(f"{prefix}_paragraph_index_invalid")
        elif paragraph_index in seen_indices:
            errors.append(f"{prefix}_paragraph_index_duplicate")
        else:
            seen_indices.add(paragraph_index)

        for field in ("original_text", "revised_text", "reason"):
            if not _nonempty_string(revision.get(field)):
                errors.append(f"{prefix}_{field}_invalid")
        if (
            _nonempty_string(revision.get("original_text"))
            and _nonempty_string(revision.get("revised_text"))
            and revision["original_text"] == revision["revised_text"]
        ):
            errors.append(f"{prefix}_no_text_change")
        if revision.get("risk_level") not in RISK_LEVELS:
            errors.append(f"{prefix}_risk_level_invalid")
        if not isinstance(revision.get("author_confirmation"), bool):
            errors.append(f"{prefix}_author_confirmation_invalid")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("--source")
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    expected_hash = sha256_file(args.source) if args.source else None
    errors = validate_revision_spec(spec, expected_hash)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
