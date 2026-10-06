import unittest
from main import add


class TestTwoSum(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual(add([2, 7, 11, 15], 9), [0, 1])

    def test_case_2(self):
        self.assertEqual(add([3, 2, 4], 6), [1, 2])

    def test_case_3(self):
        self.assertEqual(add([3, 3], 6), [0, 1])


unittest.main(argv=[''], verbosity=2, exit=False)
