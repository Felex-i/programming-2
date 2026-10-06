import unittest

def add(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i != j and nums[i] + nums[j] == target:
                return [i, j]

class TestTwoSum(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual(add([2, 7, 11, 15], 9), [0, 1])

    def test_case_2(self):
        self.assertEqual(add([3, 2, 4], 6), [1, 2])

    def test_case_3(self):
        self.assertEqual(add([3, 3], 6), [0, 1])


unittest.main(argv=[''], verbosity=2, exit=False)
