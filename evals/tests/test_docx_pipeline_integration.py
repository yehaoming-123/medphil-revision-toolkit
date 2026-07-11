import tempfile
import unittest
from pathlib import Path

from scripts.generate_revision_log import generate_revision_log
from scripts.inspect_docx import inspect_docx
from scripts.make_synthetic_manuscript import make_synthetic_manuscript
from scripts.protect_document import compare_protected_fields, create_working_copy


class DocxPipelineIntegrationTests(unittest.TestCase):
    def test_synthetic_manuscript_completes_safe_intake(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = make_synthetic_manuscript(root / "synthetic_manuscript.docx")
            before = inspect_docx(source)
            self.assertEqual(before["sensitive_markers"], [])

            working = create_working_copy(
                source,
                root / "synthetic_working_copy.docx",
            )
            after = inspect_docx(working)
            violations = compare_protected_fields(before, after)
            self.assertEqual(violations, [])
            log = generate_revision_log(before, after, [], violations)
            self.assertIn("Protected-field status: **PASSED**", log)
            self.assertIn("No prose changes recorded", log)


if __name__ == "__main__":
    unittest.main()
