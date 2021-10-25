import unittest
from my_maths import multiplier, subtractor

class TestMaths(unittest.TestCase):

    def test_multiplier(self):
        total = multiplier(2, 4)
        self.assertEqual(total, 8)

    def test_subtractor(self):
        total = subtractor(7, 4)
        self.assertEqual(total, 3)
        
    def test_blah(self):
        my_list = [2, 4, 7, 8]
        my_num = multiplier(2, 3)
        self.assertIn(my_num, my_list)



if __name__ == "__main__":
    unittest.main()
