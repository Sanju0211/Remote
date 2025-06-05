import unittest
from utils import calculate_bmi # Assuming utils.py is in the parent directory or accessible via PYTHONPATH

class TestUtils(unittest.TestCase):

    def test_calculate_bmi_normal_values(self):
        self.assertAlmostEqual(calculate_bmi(weight_kg=70, height_m=1.75), 22.86, places=2)
        self.assertAlmostEqual(calculate_bmi(weight_kg=80, height_m=1.60), 31.25, places=2)

    def test_calculate_bmi_zero_height(self):
        # As per current implementation, should return 0.0 for zero height
        self.assertEqual(calculate_bmi(weight_kg=70, height_m=0), 0.0)

    def test_calculate_bmi_very_small_height(self):
        # Test with a very small height to ensure it doesn't cause unexpected issues
        # Depending on implementation, this might also lead to ZeroDivisionError or a very large BMI
        # Current utils.py returns 0.0 if height_m == 0, otherwise calculates.
        # A very small height will result in a very large BMI.
        self.assertGreater(calculate_bmi(weight_kg=70, height_m=0.00001), 1000000) # Expect a very large number

    def test_calculate_bmi_zero_weight(self):
        self.assertEqual(calculate_bmi(weight_kg=0, height_m=1.75), 0.0)

if __name__ == '__main__':
    unittest.main()
