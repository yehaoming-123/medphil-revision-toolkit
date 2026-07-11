import unittest

from scripts.validate_revision_spec import validate_revision_spec


def valid_spec():
    return {
        "target_journal": "mhcp",
        "source_sha256": "a" * 64,
        "revisions": [
            {
                "paragraph_index": 2,
                "original_text": "Prediction cannot settle a normative question.",
                "revised_text": "Prediction alone cannot settle a normative question.",
                "reason": "Clarifies the boundary between evidence and judgment.",
                "risk_level": "low",
                "author_confirmation": False,
            }
        ],
    }


class RevisionSpecTests(unittest.TestCase):
    def test_valid_spec_passes(self):
        self.assertEqual(validate_revision_spec(valid_spec(), "a" * 64), [])

    def test_invalid_journal_empty_revision_and_unknown_fields_fail(self):
        spec = valid_spec()
        spec["target_journal"] = "unknown"
        spec["unexpected"] = True
        spec["revisions"][0]["revised_text"] = spec["revisions"][0][
            "original_text"
        ]
        spec["revisions"][0]["risk_level"] = "critical"
        spec["revisions"][0]["extra"] = "not allowed"

        errors = validate_revision_spec(spec, "a" * 64)

        self.assertIn("target_journal_invalid", errors)
        self.assertIn("top_level_unknown_fields", errors)
        self.assertIn("revision_0_no_text_change", errors)
        self.assertIn("revision_0_risk_level_invalid", errors)
        self.assertIn("revision_0_unknown_fields", errors)

    def test_missing_fields_and_source_hash_mismatch_fail(self):
        spec = valid_spec()
        del spec["revisions"][0]["reason"]

        errors = validate_revision_spec(spec, "b" * 64)

        self.assertIn("source_sha256_mismatch", errors)
        self.assertIn("revision_0_missing_reason", errors)

    def test_empty_revision_list_fails(self):
        spec = valid_spec()
        spec["revisions"] = []

        self.assertIn("revisions_empty", validate_revision_spec(spec))


if __name__ == "__main__":
    unittest.main()
