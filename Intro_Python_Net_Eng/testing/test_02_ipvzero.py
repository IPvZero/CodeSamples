import unittest
from my_maths import multiplier, subtractor


class TestMaths(unittest.TestCase):
    def test_multiplier(self):
        total = multiplier(2, 5)
        self.assertEqual(total, 10)

    def test_subtractor(self):
        total = subtractor(8, 2)
        self.assertEqual(total, 12)

    def test_blah(self):
        my_list = [2, 4, 6, 8]
        my_num = multiplier(2, 1)
        self.assertIn(my_num, my_list)


if __name__ == "__main__":
    unittest.main()
