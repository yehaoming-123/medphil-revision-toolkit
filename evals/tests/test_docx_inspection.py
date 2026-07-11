import tempfile
import unittest
from pathlib import Path

from scripts.inspect_docx import inspect_docx
from scripts.make_synthetic_manuscript import make_synthetic_manuscript


class DocxInspectionTests(unittest.TestCase):
    def test_manifest_captures_structure_and_protected_text(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "synthetic.docx"
            make_synthetic_manuscript(path)
            manifest = inspect_docx(path)

        self.assertEqual(manifest["table_count"], 1)
        self.assertEqual(manifest["section_count"], 1)
        self.assertGreaterEqual(manifest["paragraph_count"], 10)
        for heading in ("Abstract", "Introduction", "Ethical Analysis", "References"):
            self.assertIn(heading, manifest["headings"])
        self.assertIn("(Smith, 2024)", manifest["citations"])
        self.assertIn("10.1234/example.2024.001", manifest["citations"])
        self.assertEqual(len(manifest["sha256"]), 64)
        self.assertEqual(len(manifest["reference_fingerprint"]), 64)


if __name__ == "__main__":
    unittest.main()
