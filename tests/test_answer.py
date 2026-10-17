
import unittest

from src.answer import extractive_answer


class TestExtractiveAnswers(unittest.TestCase):
    def test_bharat_ratna_year(self):
        hits = [{"text": "1997 भारत रत्न भारत का सर्वोच्च नागरिक सम्मान।"}]
        answer = extractive_answer(
            "कलाम को भारत रत्न किस वर्ष प्राप्त हुआ?", hits
        )
        self.assertEqual(answer, "1997")

    def test_slv_iii_answer(self):
        hits = [{"text": "जुलाई 1980 में SLV-III ने रोहिणी उपग्रह को कक्षा में स्थापित किया।"}]
        answer = extractive_answer(
            "SLV-III ने किस उपग्रह को कक्षा में स्थापित किया और किस वर्ष?", hits
        )
        self.assertIn("रोहिणी", answer)
        self.assertIn("1980", answer)

    def test_no_evidence(self):
        answer = extractive_answer("Unknown question", [])
        self.assertEqual(
            answer, "No supporting evidence found in the document."
        )


if __name__ == "__main__":
    unittest.main()
