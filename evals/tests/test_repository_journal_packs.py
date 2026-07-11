import unittest
from pathlib import Path

from scripts.validate_journal_pack import validate_pack


ROOT = Path(__file__).resolve().parents[2]


class RepositoryJournalPackTests(unittest.TestCase):
    def test_all_four_packs_validate(self):
        for journal_id in ("mhcp", "jme", "bioethics", "jmp"):
            with self.subTest(journal=journal_id):
                self.assertEqual(
                    validate_pack(
                        ROOT / "journal-packs" / journal_id,
                        as_of="2026-07-11",
                    ),
                    [],
                )


if __name__ == "__main__":
    unittest.main()
