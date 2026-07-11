import argparse
import hashlib
import json
from pathlib import Path

from docx import Document

from scripts.inspect_docx import (
    AUTHOR_YEAR_PATTERN,
    DOI_PATTERN,
    NUMBERED_CITATION_PATTERN,
    sha256_file,
)


def _contains_citation(text):
    return any(
        pattern.search(text)
        for pattern in (DOI_PATTERN, AUTHOR_YEAR_PATTERN, NUMBERED_CITATION_PATTERN)
    )


def _format_signature(run):
    size = run.font.size.pt if run.font.size else None
    style_id = run.style.style_id if run.style else None
    return (
        run.bold,
        run.italic,
        run.underline,
        run.font.name,
        size,
        style_id,
    )


def _xml_present(paragraph, query):
    return bool(paragraph._p.xpath(query))


def _paragraph_record(paragraph, index, section, in_references):
    text = paragraph.text
    nonempty_runs = [run for run in paragraph.runs if run.text]
    signatures = {_format_signature(run) for run in nonempty_runs}
    style_name = paragraph.style.name if paragraph.style else ""
    is_heading = style_name.startswith("Heading") or style_name in {"Title", "Subtitle"}
    flags = {
        "citation": _contains_citation(text),
        "reference_section": in_references,
        "heading": is_heading,
        "empty": not text.strip(),
        "hyperlink": _xml_present(paragraph, ".//w:hyperlink"),
        "field": _xml_present(paragraph, ".//w:fldChar | .//w:instrText"),
        "drawing": _xml_present(paragraph, ".//w:drawing | .//w:pict"),
        "mixed_formatting": len(signatures) > 1,
    }
    protection_reasons = [name for name, present in flags.items() if present]
    return {
        "paragraph_index": index,
        "section": section,
        "style": style_name,
        "text": text,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "run_count": len(paragraph.runs),
        "contains_citation": flags["citation"],
        "in_reference_section": flags["reference_section"],
        "has_hyperlink": flags["hyperlink"],
        "has_field": flags["field"],
        "has_drawing": flags["drawing"],
        "has_mixed_formatting": flags["mixed_formatting"],
        "eligible": not protection_reasons,
        "protection_reasons": protection_reasons,
    }


def build_revision_inventory(path):
    source = Path(path)
    document = Document(source)
    records = []
    section = "Front matter"
    in_references = False
    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        style_name = paragraph.style.name if paragraph.style else ""
        if text.casefold() in {"references", "bibliography"}:
            in_references = True
        if text and style_name.startswith("Heading"):
            section = text
        records.append(
            _paragraph_record(paragraph, index, section, in_references)
        )
    return {
        "path": str(source.resolve()),
        "sha256": sha256_file(source),
        "paragraphs": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    print(
        json.dumps(
            build_revision_inventory(args.input),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
