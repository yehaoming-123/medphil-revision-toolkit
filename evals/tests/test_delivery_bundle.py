import tempfile
import unittest
from pathlib import Path

from scripts.build_delivery_bundle import (
    REQUIRED_DELIVERABLES,
    DeliveryBundleError,
    build_delivery_bundle,
)
from scripts.inspect_docx import inspect_docx
from scripts.make_synthetic_manuscript import make_synthetic_manuscript


def routing_record():
    journals = ["mhcp", "jmp", "jme", "bioethics"]
    return {
        "ranking": [
            {
                "rank": rank,
                "journal": journal,
                "fit_reasons": ["Relevant scope"],
                "mismatch_reasons": ["Audience trade-off"],
                "evidence_limits": ["editorial_inference"],
            }
            for rank, journal in enumerate(journals, start=1)
        ],
        "recommended_target": "mhcp",
        "alternative": "jmp",
        "ranking_change_conditions": ["A more purely analytic framing would favor JMP."],
    }


def fit_record():
    return {
        "target_journal": "mhcp",
        "official_requirements": ["Verify current article-type requirements."],
        "observed_tendencies": ["Conceptual contribution is explicit."],
        "abstract_limited": ["No abstract-only claims used."],
        "editorial_inferences": ["Lead with the medical-philosophical problem."],
        "remaining_risks": ["Clarify the objection section."],
        "pre_submission_checks": ["Recheck references and declarations."],
    }


class DeliveryBundleTests(unittest.TestCase):
    def test_builds_exactly_five_required_deliverables(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            revised = make_synthetic_manuscript(root / "working.docx")
            manifest = inspect_docx(revised)
            record = {
                "applied": [
                    {
                        "paragraph_index": 2,
                        "reason": "Clarified the thesis.",
                    }
                ],
                "author_confirmation": [],
                "protected_field_violations": [],
            }
            output = root / "bundle"

            paths = build_delivery_bundle(
                output,
                revised,
                manifest,
                manifest,
                record,
                routing_record(),
                fit_record(),
            )

            self.assertEqual(set(paths), REQUIRED_DELIVERABLES)
            self.assertEqual(
                {path.name for path in output.iterdir()},
                REQUIRED_DELIVERABLES,
            )
            routing_text = (output / "journal_routing_report.md").read_text(
                encoding="utf-8"
            )
            fit_text = (output / "journal_fit_report.md").read_text(
                encoding="utf-8"
            )
            revision_log = (output / "revision_log.md").read_text(encoding="utf-8")
            confirmation = (output / "author_confirmation_needed.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("| 1 | MHCP |", routing_text)
            self.assertIn("official_requirement", fit_text)
            self.assertIn("editorial_inference", fit_text)
            self.assertIn("# 修改日志", revision_log)
            self.assertIn("当前无需作者确认", confirmation)

    def test_invalid_four_journal_ranking_fails_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            revised = make_synthetic_manuscript(root / "working.docx")
            manifest = inspect_docx(revised)
            routing = routing_record()
            routing["ranking"] = routing["ranking"][:3]
            output = root / "bundle"

            with self.assertRaises(DeliveryBundleError):
                build_delivery_bundle(
                    output,
                    revised,
                    manifest,
                    manifest,
                    {"applied": [], "author_confirmation": []},
                    routing,
                    fit_record(),
                )

            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
