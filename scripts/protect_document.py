import shutil
from pathlib import Path

from scripts.inspect_docx import sha256_file


def create_working_copy(source, destination):
    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()
    if source_path == destination_path:
        raise ValueError("source and destination must differ")
    if destination_path.exists():
        raise FileExistsError(f"destination already exists: {destination_path}")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    source_hash = sha256_file(source_path)
    shutil.copy2(source_path, destination_path)
    if sha256_file(destination_path) != source_hash:
        destination_path.unlink(missing_ok=True)
        raise OSError("working-copy hash does not match source")
    return destination_path


def compare_protected_fields(before, after):
    checks = {
        "citations": "citations_changed",
        "reference_fingerprint": "reference_fingerprint_changed",
        "table_count": "table_count_changed",
        "section_count": "section_count_changed",
        "comments_present": "comments_part_changed",
        "footnotes_present": "footnotes_part_changed",
    }
    return [
        violation
        for field, violation in checks.items()
        if before.get(field) != after.get(field)
    ]
