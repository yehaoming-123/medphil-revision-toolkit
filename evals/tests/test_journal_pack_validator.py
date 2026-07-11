import tempfile
import unittest
from pathlib import Path

from scripts.validate_journal_pack import validate_pack


VALID_PROFILE = """id: mhcp
name: Medicine, Health Care and Philosophy
publisher: Springer Nature
scope_summary: Philosophy of medicine, health care, and bioethics.
article_types: [conceptual, normative]
fit_signals: [clinical judgment, philosophy of medicine]
mismatch_signals: [purely technical validation]
official_urls: [https://link.springer.com/journal/11019]
checked_at: 2026-07-11
"""

VALID_REGISTRY = """---
sources:
  - claim_id: scope-001
    claim: The journal covers philosophy of medicine and health care.
    evidence_type: official_requirement
    url: https://link.springer.com/journal/11019
    checked_at: 2026-07-11
    applies_to: all articles
    status: current
---
# Source notes
"""


class JournalPackValidatorTests(unittest.TestCase):
    def make_pack(self, profile=VALID_PROFILE, registry=VALID_REGISTRY):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name)
        (path / "profile.yaml").write_text(profile, encoding="utf-8")
        (path / "source_registry.md").write_text(registry, encoding="utf-8")
        for name in (
            "official_requirements.md",
            "editorial_profile.md",
            "routing_examples.md",
        ):
            (path / name).write_text(f"# {name}\n", encoding="utf-8")
        (path / "eval_cases.yaml").write_text("cases: []\n", encoding="utf-8")
        return temp, path

    def test_valid_pack_has_no_errors(self):
        temp, path = self.make_pack()
        self.addCleanup(temp.cleanup)
        self.assertEqual(validate_pack(path, as_of="2026-07-11"), [])

    def test_missing_profile_field_is_reported(self):
        profile = VALID_PROFILE.replace("publisher: Springer Nature\n", "")
        temp, path = self.make_pack(profile=profile)
        self.addCleanup(temp.cleanup)
        self.assertIn(
            "profile missing field: publisher",
            validate_pack(path, as_of="2026-07-11"),
        )

    def test_unknown_evidence_type_is_reported(self):
        registry = VALID_REGISTRY.replace("official_requirement", "reputation")
        temp, path = self.make_pack(registry=registry)
        self.addCleanup(temp.cleanup)
        self.assertIn(
            "source scope-001 has invalid evidence_type: reputation",
            validate_pack(path, as_of="2026-07-11"),
        )

    def test_source_older_than_90_days_is_reported(self):
        registry = VALID_REGISTRY.replace("2026-07-11", "2026-01-01")
        temp, path = self.make_pack(registry=registry)
        self.addCleanup(temp.cleanup)
        self.assertIn(
            "source scope-001 is stale",
            validate_pack(path, as_of="2026-07-11"),
        )

    def test_missing_source_field_is_reported(self):
        registry = VALID_REGISTRY.replace("    applies_to: all articles\n", "")
        temp, path = self.make_pack(registry=registry)
        self.addCleanup(temp.cleanup)
        self.assertIn(
            "source scope-001 missing field: applies_to",
            validate_pack(path, as_of="2026-07-11"),
        )


if __name__ == "__main__":
    unittest.main()
