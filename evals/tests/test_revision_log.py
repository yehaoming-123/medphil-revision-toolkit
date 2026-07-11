import unittest
from pathlib import Path

from scripts.generate_revision_log import generate_revision_log


class RevisionLogTests(unittest.TestCase):
    def test_log_contains_hashes_changes_and_violations(self):
        text = generate_revision_log(
            {"sha256": "before-hash", "path": "source.docx"},
            {"sha256": "after-hash", "path": "working.docx"},
            [{"location": "Abstract", "change": "Clarified the thesis."}],
            ["citations_changed"],
        )
        self.assertIn("# Revision Log", text)
        self.assertIn("before-hash", text)
        self.assertIn("after-hash", text)
        self.assertIn("Protected-field status: **FAILED**", text)
        self.assertIn("Abstract", text)
        self.assertIn("citations_changed", text)

    def test_log_does_not_expose_local_absolute_paths(self):
        source = Path("D:/private/manuscripts/source.docx")
        output = Path("D:/private/manuscripts/output/working.docx")

        text = generate_revision_log(
            {"sha256": "before-hash", "path": str(source)},
            {"sha256": "after-hash", "path": str(output)},
            [],
            [],
        )

        self.assertIn("`source.docx`", text)
        self.assertIn("`working.docx`", text)
        self.assertNotIn("D:/private", text)


if __name__ == "__main__":
    unittest.main()
