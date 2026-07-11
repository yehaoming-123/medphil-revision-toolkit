import tempfile
import unittest
from pathlib import Path

from docx import Document

from scripts.inspect_docx import inspect_docx, sha256_file
from scripts.make_synthetic_manuscript import make_synthetic_manuscript
from scripts.protect_document import compare_protected_fields, create_working_copy


class DocumentProtectionTests(unittest.TestCase):
    def test_source_and_destination_must_differ(self):
        with tempfile.TemporaryDirectory() as temp:
            source = make_synthetic_manuscript(Path(temp) / "source.docx")
            with self.assertRaises(ValueError):
                create_working_copy(source, source)

    def test_existing_destination_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            source = make_synthetic_manuscript(Path(temp) / "source.docx")
            destination = Path(temp) / "existing.docx"
            destination.write_bytes(b"existing")
            with self.assertRaises(FileExistsError):
                create_working_copy(source, destination)
            self.assertEqual(destination.read_bytes(), b"existing")

    def test_new_working_copy_matches_source_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            source = make_synthetic_manuscript(Path(temp) / "source.docx")
            before = sha256_file(source)
            destination = create_working_copy(source, Path(temp) / "working.docx")
            self.assertEqual(sha256_file(source), before)
            self.assertEqual(sha256_file(destination), before)

    def test_reference_and_citation_changes_are_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            source = make_synthetic_manuscript(Path(temp) / "source.docx")
            working = create_working_copy(source, Path(temp) / "working.docx")
            self.assertEqual(
                compare_protected_fields(inspect_docx(source), inspect_docx(working)),
                [],
            )

            document = Document(working)
            for paragraph in document.paragraphs:
                if "10.1234/example.2024.001" in paragraph.text:
                    paragraph.text = paragraph.text.replace(
                        "10.1234/example.2024.001",
                        "10.1234/changed.2024.999",
                    )
            document.save(working)
            violations = compare_protected_fields(
                inspect_docx(source),
                inspect_docx(working),
            )
            self.assertIn("citations_changed", violations)
            self.assertIn("reference_fingerprint_changed", violations)


if __name__ == "__main__":
    unittest.main()
