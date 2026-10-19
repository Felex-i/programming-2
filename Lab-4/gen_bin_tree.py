import unittest
from app import gen_bin_tree


class TestGenBinTree(unittest.TestCase):

    def test_height_zero(self):
        t = gen_bin_tree(0, 7)
        self.assertEqual(t["value"], 7)
        self.assertIsNone(t["left"])
        self.assertIsNone(t["right"])

    def test_height_one_defaults(self):
        t = gen_bin_tree(1, 3)
        self.assertEqual((t["left"]["value"], t["right"]["value"]), (5, 9))

    def test_height_two(self):
        t = gen_bin_tree(2, 3)
        self.assertEqual(t["left"]["left"]["value"], 7)
        self.assertEqual(t["right"]["right"]["value"], 27)

    def test_defaults(self):
        self.assertEqual(gen_bin_tree()["value"], 3)

    def test_custom_lambdas(self):
        t = gen_bin_tree(1, 4, lambda x: x - 1, lambda x: x + 100)
        self.assertEqual((t["left"]["value"], t["right"]["value"]), (3, 104))

    def test_negative_height(self):
        with self.assertRaises(ValueError):
            gen_bin_tree(-1, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)