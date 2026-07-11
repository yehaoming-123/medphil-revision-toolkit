import unittest

from scripts.inspect_docx import detect_sensitive_markers


class SensitiveGateTests(unittest.TestCase):
    def test_obvious_identifier_shapes_are_flagged(self):
        cases = {
            "author@example.org": "email",
            "+86 138-1234-5678": "phone",
            "11010519491231002X": "national_id",
            "MRN: ICU-88421": "medical_record_id",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                labels = {item["label"] for item in detect_sensitive_markers(text)}
                self.assertIn(expected, labels)

    def test_academic_numbers_do_not_trigger(self):
        text = "Published in 2024. DOI 10.1234/example.2024.001."
        self.assertEqual(detect_sensitive_markers(text), [])


if __name__ == "__main__":
    unittest.main()
