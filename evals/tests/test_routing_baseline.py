import unittest
from pathlib import Path

import yaml

from scripts.route_journal import route_text


ROOT = Path(__file__).resolve().parents[2]


class RoutingBaselineTests(unittest.TestCase):
    def test_four_synthetic_cases_route_to_expected_primary(self):
        data = yaml.safe_load(
            (ROOT / "evals" / "fixtures" / "routing_cases.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(len(data["cases"]), 4)
        for case in data["cases"]:
            with self.subTest(case=case["id"]):
                ranking = route_text(
                    case["title"] + " " + case["abstract"],
                    ROOT / "journal-packs",
                )
                self.assertEqual(ranking[0]["journal"], case["expected_primary"])
                self.assertNotIn("acceptance_probability", ranking[0])


if __name__ == "__main__":
    unittest.main()
