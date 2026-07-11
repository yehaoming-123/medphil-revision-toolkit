import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PluginStructureTests(unittest.TestCase):
    def test_manifest_points_to_existing_skills_directory(self):
        manifest_path = ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(manifest_path.exists())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "medphil-revision-toolkit")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertTrue((ROOT / manifest["skills"]).is_dir())

    def test_required_skills_have_frontmatter_and_ui_metadata(self):
        for name in ("medphil-revision", "journal-router"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"name: {name}", text)
            self.assertIn("description:", text)
            metadata = ROOT / "skills" / name / "agents" / "openai.yaml"
            self.assertTrue(metadata.exists())
            self.assertIn(f"${name}", metadata.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
