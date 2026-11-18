import unittest

from add import add


class TestAdd(unittest.TestCase):
    def test_basic_case(self):
        result = add([2, 7, 11, 15], 9)
        self.assertIn(result, ([0, 1], [1, 0]))

    def test_same_element_not_used_twice(self):
        # 3 + 3 = 6, но тройка в списке одна, поэтому ответ только 2 и 4
        result = add([3, 2, 4], 6)
        self.assertIn(result, ([1, 2], [2, 1]))

    def test_equal_values(self):
        # два одинаковых числа - это два разных элемента
        result = add([3, 3], 6)
        self.assertIn(result, ([0, 1], [1, 0]))

    def test_no_pair(self):
        self.assertIsNone(add([1, 2, 3], 100))

    def test_empty_list(self):
        self.assertIsNone(add([], 5))

    def test_one_element(self):
        # 5 + 5 = 10, но элемент всего один, пары нет
        self.assertIsNone(add([5], 10))

    def test_negative_numbers(self):
        result = add([-3, 4, 3, 90], 0)
        self.assertIn(result, ([0, 2], [2, 0]))

    def test_zeros(self):
        result = add([0, 4, 3, 0], 0)
        self.assertIn(result, ([0, 3], [3, 0]))

    def test_pair_at_the_end(self):
        # единственная подходящая пара (4 и 6) стоит в конце списка
        result = add([2, 5, 9, 20, 30, 4, 6], 10)
        self.assertIn(result, ([5, 6], [6, 5]))

    def test_several_pairs(self):
        # подходят две пары: 1 + 9 и 2 + 8, можно вернуть любую
        result = add([1, 9, 2, 8], 10)
        self.assertIn(result, ([0, 1], [1, 0], [2, 3], [3, 2]))

    def test_list_not_changed(self):
        nums = [8, 1, 5, 2]
        add(nums, 7)
        self.assertEqual(nums, [8, 1, 5, 2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
