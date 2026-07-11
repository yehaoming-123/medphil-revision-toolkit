import argparse
import json
import sys
from pathlib import Path

from docx import Document

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_revision_inventory import build_revision_inventory
from scripts.inspect_docx import inspect_docx, sha256_file
from scripts.protect_document import compare_protected_fields, create_working_copy
from scripts.validate_revision_spec import validate_revision_spec


class RevisionApplicationError(ValueError):
    def __init__(self, message, record):
        super().__init__(message)
        self.record = record


def _record_base(source, output, spec):
    return {
        "source": Path(source).name,
        "source_sha256": sha256_file(source),
        "output": Path(output).name,
        "target_journal": spec.get("target_journal"),
        "applied": [],
        "rejected": [],
        "author_confirmation": [],
        "protected_field_violations": [],
    }


def _preflight(source, output, spec):
    record = _record_base(source, output, spec)
    spec_errors = validate_revision_spec(spec, record["source_sha256"])
    if spec_errors:
        record["rejected"].append(
            {"reason": "revision_spec_invalid", "errors": spec_errors}
        )
        raise RevisionApplicationError("revision specification is invalid", record)

    inventory = build_revision_inventory(source)
    paragraphs = inventory["paragraphs"]
    candidates = []
    for revision in spec["revisions"]:
        index = revision["paragraph_index"]
        if index >= len(paragraphs):
            record["rejected"].append(
                {"paragraph_index": index, "reason": "paragraph_index_out_of_range"}
            )
            continue
        paragraph = paragraphs[index]
        if paragraph["text"] != revision["original_text"]:
            record["rejected"].append(
                {"paragraph_index": index, "reason": "original_text_mismatch"}
            )
            continue
        if not paragraph["eligible"]:
            record["rejected"].append(
                {
                    "paragraph_index": index,
                    "reason": "protected_paragraph",
                    "protection_reasons": paragraph["protection_reasons"],
                }
            )
            continue
        if revision["author_confirmation"]:
            record["author_confirmation"].append(dict(revision))
            continue
        candidates.append(revision)

    if record["rejected"]:
        raise RevisionApplicationError("revision preflight failed", record)
    return record, candidates


def apply_revision_spec(source, output, spec):
    source_path = Path(source)
    output_path = Path(output)
    if output_path.exists():
        raise FileExistsError(f"output already exists: {output_path.resolve()}")

    record, candidates = _preflight(source_path, output_path, spec)
    create_working_copy(source_path, output_path)
    try:
        document = Document(output_path)
        for revision in candidates:
            paragraph = document.paragraphs[revision["paragraph_index"]]
            if not paragraph.runs:
                raise RevisionApplicationError(
                    "eligible paragraph has no editable runs",
                    record,
                )
            paragraph.runs[0].text = revision["revised_text"]
            for run in paragraph.runs[1:]:
                run.text = ""
            record["applied"].append(dict(revision))
        document.save(output_path)

        before = inspect_docx(source_path)
        after = inspect_docx(output_path)
        violations = compare_protected_fields(before, after)
        record["protected_field_violations"] = violations
        record["output_sha256"] = after["sha256"]
        if violations:
            raise RevisionApplicationError(
                "protected fields changed during revision",
                record,
            )
        return record
    except Exception:
        output_path.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("spec")
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    try:
        record = apply_revision_spec(args.source, args.output, spec)
    except RevisionApplicationError as error:
        print(json.dumps(error.record, ensure_ascii=False, indent=2))
        raise SystemExit(1) from error
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
