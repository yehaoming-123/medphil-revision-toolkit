import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SkillContractTests(unittest.TestCase):
    def read_skill(self, name):
        return (ROOT / "skills" / name / "SKILL.md").read_text(
            encoding="utf-8"
        ).casefold()

    def test_revision_skill_names_all_five_outputs(self):
        text = self.read_skill("medphil-revision")
        for output in (
            "revised_manuscript.docx",
            "revision_log.md",
            "journal_routing_report.md",
            "journal_fit_report.md",
            "author_confirmation_needed.md",
        ):
            self.assertIn(output, text)

    def test_revision_skill_enforces_safety_and_confirmation(self):
        text = self.read_skill("medphil-revision")
        for phrase in (
            "preserve the author's thesis",
            "do not invent citations",
            "identifiable patient information",
            "confirm the target journal",
            "freeze the reference list",
        ):
            self.assertIn(phrase, text)

    def test_router_covers_four_journals_and_evidence_layers(self):
        text = self.read_skill("journal-router")
        for phrase in (
            "mhcp",
            "jme",
            "bioethics",
            "jmp",
            "official_requirement",
            "observed_tendency",
            "editorial_inference",
            "abstract_limited",
        ):
            self.assertIn(phrase, text)

    def test_router_requires_mismatch_reasons_and_forbids_prediction(self):
        text = self.read_skill("journal-router")
        self.assertIn("mismatch reasons", text)
        self.assertIn("never provide an acceptance probability", text)
        self.assertIn("author confirms the target", text)


if __name__ == "__main__":
    unittest.main()
