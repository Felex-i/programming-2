"""Тесты для memo_tree."""

import unittest

from memo_tree import (gen_bin_tree_iterative, gen_bin_tree_iterative_memo,
                       gen_bin_tree_recursive, gen_bin_tree_recursive_lru,
                       gen_bin_tree_recursive_memo, memoize)

ALL = [gen_bin_tree_recursive, gen_bin_tree_iterative]
MEMO = [gen_bin_tree_recursive_memo, gen_bin_tree_iterative_memo,
        gen_bin_tree_recursive_lru]


def inc(x: int) -> int:
    """Вернуть x + 1."""
    return x + 1


def dec(x: int) -> int:
    """Вернуть x - 1."""
    return x - 1


class TestBasics(unittest.TestCase):
    """Тесты из ЛР 4 для всех пяти реализаций."""

    def setUp(self) -> None:
        gen_bin_tree_recursive_memo.cache_clear()
        gen_bin_tree_recursive_lru.cache_clear()

    def test_basics(self) -> None:
        for f in ALL + MEMO:
            with self.subTest(f=f.__name__):
                t = f(0, 7)
                self.assertEqual(t, {"value": 7, "left": None, "right": None})
                t = f(2, 3)
                self.assertEqual((t["left"]["value"], t["right"]["value"]),
                                 (5, 9))
                self.assertEqual(t["left"]["left"]["value"], 7)
                self.assertEqual(t["right"]["right"]["value"], 27)
                self.assertEqual(f()["value"], 3)
                t = f(1, 4, lambda x: x - 1, lambda x: x + 100)
                self.assertEqual((t["left"]["value"], t["right"]["value"]),
                                 (3, 104))
                with self.assertRaises(ValueError):
                    f(-1, 1)


class TestMemoTree(unittest.TestCase):
    """Тесты мемоизованных версий и декоратора."""

    def setUp(self) -> None:
        gen_bin_tree_recursive_memo.cache_clear()
        gen_bin_tree_recursive_lru.cache_clear()

    def test_same_tree_defaults(self) -> None:
        for f in MEMO + [gen_bin_tree_iterative]:
            self.assertEqual(f(), gen_bin_tree_recursive())

    def test_same_tree_custom(self) -> None:
        expected = gen_bin_tree_recursive(6, 0, inc, dec)
        for f in MEMO:
            self.assertEqual(f(6, 0, inc, dec), expected)
            self.assertEqual(f(height=6, root=0, left_leaf=inc,
                               right_leaf=dec), expected)

    def test_negative_height(self) -> None:
        for f in MEMO:
            with self.assertRaises(ValueError):
                f(-1, 1)

    def test_memoize_calls_once(self) -> None:
        calls = []

        @memoize
        def f(x: int = 0) -> int:
            """Тождество."""
            calls.append(x)
            return x

        f(1), f(1), f(x=1), f(2)
        self.assertEqual(calls, [1, 1, 2])  # f(x=1) - другой ключ
        self.assertEqual(f.__name__, "f")
        f.cache_clear()
        self.assertEqual((f.hits, f.misses), (0, 0))

    def test_shared_subtrees(self) -> None:
        for f in (gen_bin_tree_recursive_memo, gen_bin_tree_iterative_memo):
            t = f(2, 0, inc, dec)
            self.assertIs(t["left"]["right"], t["right"]["left"])
            t["left"]["right"]["value"] = 999
            self.assertEqual(t["right"]["left"]["value"], 999)

    def test_cache_between_calls_shares_result(self) -> None:
        t1 = gen_bin_tree_recursive_memo(2, 0, inc, dec)
        t1["left"]["right"]["value"] = 999
        t2 = gen_bin_tree_recursive_memo(2, 0, inc, dec)
        self.assertEqual(t2["right"]["left"]["value"], 999)

    def test_no_sharing_without_memo(self) -> None:
        t = gen_bin_tree_recursive(2, 0, inc, dec)
        self.assertIsNot(t["left"]["right"], t["right"]["left"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
