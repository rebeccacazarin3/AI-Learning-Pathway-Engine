import unittest
import pandas as pd
from services.occupation_profile import (
    get_occupation_profile,
)

from models.occupation import Occupation

class TestOccupationProfile(unittest.TestCase):

    def test_invalid_occupation_profile(self):
        with self.assertRaises(ValueError):
            get_occupation_profile("INVALID")

    def test_valid_occupation_profile(self):
        profile = get_occupation_profile("15-1252.00")

        self.assertIsInstance(profile["occupation"], Occupation)
        self.assertIn("tasks", profile)
        self.assertIn("dwas", profile)
        self.assertIn("essential_skills", profile)
        self.assertIn("transferable_skills", profile)
        self.assertIn("software_skills", profile)

    def test_dwas_count_and_uniqueness(self):
        profile = get_occupation_profile("15-1252.00")
        self.assertEqual(len(profile["dwas"]), 18)
        self.assertEqual(len(profile["dwas"]), len(set(profile["dwas"])))

    def test_essential_skills(self):
        profile = get_occupation_profile("15-1252.00")
        self.assertIn("essential_skills", profile)
        self.assertIsInstance(profile["essential_skills"], pd.DataFrame)
        self.assertFalse(profile["essential_skills"].empty)

    def test_transferable_skills(self):
        profile = get_occupation_profile("15-1252.00")
        self.assertIn("transferable_skills", profile)
        self.assertIsInstance(profile["transferable_skills"], pd.DataFrame)
        self.assertFalse(profile["transferable_skills"].empty)

    def test_software_skills(self):
        profile = get_occupation_profile("15-1252.00")
        self.assertIn("software_skills", profile)
        self.assertIsInstance(profile["software_skills"], pd.DataFrame)
        self.assertFalse(profile["software_skills"].empty)
        self.assertEqual(len(profile["software_skills"]), 67)
        self.assertEqual(
            set(profile["software_skills"].columns),
            {"Element Name", "Workplace Examples"}
        )

        total_examples = sum(
            len(examples)
            for examples in profile["software_skills"]["Workplace Examples"]
        )
        self.assertEqual(total_examples, 430)

        for _, row in profile["software_skills"].iterrows():
            self.assertIsInstance(row["Workplace Examples"], list)

            for example in row["Workplace Examples"]:
                self.assertIsInstance(example, dict)

                self.assertIn(example["Hot Technology"], ["Y", "N"])
                self.assertIn(example["In Demand"], ["Y", "N"])

                self.assertEqual(
                    set(example.keys()),
                    {"Workplace Example", "Hot Technology", "In Demand"},
                    "Expected each workplace example to contain all three fields"
                )

if __name__ == "__main__":
    unittest.main()



