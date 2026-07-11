import tempfile
import unittest
from pathlib import Path

from scripts.render_docx_qa import build_soffice_command


class RenderDocxQaTests(unittest.TestCase):
    def test_user_profile_is_a_standard_file_uri(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            command = build_soffice_command(
                root / "input.docx",
                root / "output",
                root / "profile with spaces",
                soffice="soffice.com",
            )

            profile_argument = next(
                item for item in command if item.startswith("-env:UserInstallation=")
            )
            uri = profile_argument.split("=", 1)[1]
            self.assertTrue(uri.startswith("file:///"))
            self.assertNotIn("\\", uri)
            self.assertIn("%20", uri)
            self.assertIn("-env:InstallMode=", command)


if __name__ == "__main__":
    unittest.main()
