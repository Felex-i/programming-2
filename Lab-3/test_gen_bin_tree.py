"""Тесты для gen_bin_tree."""
import unittest

from gen_bin_tree import Node, gen_bin_tree, gen_bin_tree_nt


class TestGenBinTree(unittest.TestCase):
    """Проверка построения бинарного дерева."""

    def test_root(self) -> None:
        """Корень по умолчанию равен 3."""
        self.assertEqual(gen_bin_tree()["value"], 3)

    def test_children(self) -> None:
        """Потомки вычисляются по алгоритмам варианта."""
        tree = gen_bin_tree()
        self.assertEqual(tree["left"]["value"], 5)    # 3 + 2
        self.assertEqual(tree["right"]["value"], 9)   # 3 * 3
        self.assertEqual(tree["left"]["right"]["value"], 15)  # 5 * 3

    def test_leaf(self) -> None:
        """При height=0 возвращается лист без потомков."""
        self.assertEqual(gen_bin_tree(0), {"value": 3, "left": None, "right": None})

    def test_custom_params(self) -> None:
        """Переданные параметры заменяют значения по умолчанию."""
        tree = gen_bin_tree(1, 10, lambda x: x - 1, lambda x: x + 1)
        self.assertEqual((tree["left"]["value"], tree["right"]["value"]), (9, 11))

    def test_invalid_height(self) -> None:
        """Высота меньше 0 вызывает ValueError."""
        with self.assertRaises(ValueError):
            gen_bin_tree(-1)

    def test_namedtuple(self) -> None:
        """Версия на namedtuple строит то же дерево."""
        self.assertEqual(
            gen_bin_tree_nt(1),
            Node(3, Node(5, None, None), Node(9, None, None)),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
