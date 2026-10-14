"""Построение бинарного дерева (вариант 3).

root = 3, height = 4, left_leaf = root + 2, right_leaf = root * 3.
"""
from collections import namedtuple
from typing import Callable, Dict, Optional

Node = namedtuple("Node", ["value", "left", "right"])


def gen_bin_tree(
    height: int = 4,
    root: int = 3,
    left_leaf: Callable[[int], int] = lambda x: x + 2,
    right_leaf: Callable[[int], int] = lambda x: x * 3,
) -> Dict[str, Optional[object]]:
    """Рекурсивно строит бинарное дерево в виде словаря.

    :param height: высота дерева в рёбрах (у одного корня высота 0).
    :param root: значение в корне дерева.
    :param left_leaf: функция вычисления левого потомка по значению узла.
    :param right_leaf: функция вычисления правого потомка по значению узла.
    :return: словарь с ключами value, left, right.
    :raises ValueError: если height меньше 0.
    """
    if height < 0:
        raise ValueError("height должна быть не меньше 0")
    if height == 0:
        return {"value": root, "left": None, "right": None}
    return {
        "value": root,
        "left": gen_bin_tree(height - 1, left_leaf(root), left_leaf, right_leaf),
        "right": gen_bin_tree(height - 1, right_leaf(root), left_leaf, right_leaf),
    }


def gen_bin_tree_nt(
    height: int = 4,
    root: int = 3,
    left_leaf: Callable[[int], int] = lambda x: x + 2,
    right_leaf: Callable[[int], int] = lambda x: x * 3,
) -> Node:
    """То же дерево, но узлы хранятся в collections.namedtuple.

    Параметры и исключение такие же, как у gen_bin_tree.
    """
    if height < 0:
        raise ValueError("height должна быть не меньше 0")
    if height == 0:
        return Node(root, None, None)
    return Node(
        root,
        gen_bin_tree_nt(height - 1, left_leaf(root), left_leaf, right_leaf),
        gen_bin_tree_nt(height - 1, right_leaf(root), left_leaf, right_leaf),
    )
