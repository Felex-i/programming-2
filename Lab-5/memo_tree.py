"""Бинарное дерево (вариант 3) с мемоизацией и без."""

from collections import deque
from functools import lru_cache, wraps
from typing import Any, Callable, Dict, Optional, Tuple

Tree = Dict[str, Any]
Leaf = Callable[[int], int]


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """Мемоизировать функцию; ключ - все позиционные и именованные аргументы."""
    cache: Dict[Any, Any] = {}

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            wrapper.hits += 1
            return cache[key]
        wrapper.misses += 1
        cache[key] = func(*args, **kwargs)
        return cache[key]

    def cache_clear() -> None:
        """Очистить кэш и счётчики."""
        cache.clear()
        wrapper.hits = wrapper.misses = 0

    wrapper.cache, wrapper.cache_clear = cache, cache_clear
    wrapper.hits = wrapper.misses = 0
    return wrapper


def gen_bin_tree_recursive(
    height: int = 4,
    root: int = 3,
    left_leaf: Callable[[int], int] = lambda x: x + 2,
    right_leaf: Callable[[int], int] = lambda x: x * 3,
) -> Dict[str, Optional[object]]:
    """Рекурсивно строит бинарное дерево в виде словаря (ЛР 3).

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
        "left": gen_bin_tree_recursive(height - 1, left_leaf(root), left_leaf, right_leaf),
        "right": gen_bin_tree_recursive(height - 1, right_leaf(root), left_leaf, right_leaf),
    }


def gen_bin_tree_iterative(
    height: int = 4,
    root: int = 3,
    left_leaf: Callable[[int], int] = lambda r: r + 2,
    right_leaf: Callable[[int], int] = lambda r: r * 3,
) -> Dict[str, Any]:
    """Строит бинарное дерево высоты ``height`` (BFS, без рекурсии, ЛР 4).

    Args:
        height: число уровней-потомков под корнем.
        root: значение корня.
        left_leaf: функция левого потомка.
        right_leaf: функция правого потомка.

    Returns:
        Корень - словарь ``{'value', 'left', 'right'}``.
    """
    if height < 0:
        raise ValueError("height must be >= 0")

    root_node = {"value": root, "left": None, "right": None}
    queue = deque([(root_node, height)])

    while queue:
        node, h = queue.popleft()
        if h == 0:
            continue
        node["left"] = {"value": left_leaf(node["value"]), "left": None, "right": None}
        node["right"] = {"value": right_leaf(node["value"]), "left": None, "right": None}
        queue.append((node["left"], h - 1))
        queue.append((node["right"], h - 1))

    return root_node


@memoize
def gen_bin_tree_recursive_memo(height: int = 4, root: int = 3,
                                left_leaf: Leaf = lambda x: x + 2,
                                right_leaf: Leaf = lambda x: x * 3) -> Tree:
    """Рекурсивное построение; рекурсивные вызовы идут через кэш."""
    if height < 0:
        raise ValueError("height должна быть не меньше 0")
    if height == 0:
        return {"value": root, "left": None, "right": None}
    return {
        "value": root,
        "left": gen_bin_tree_recursive_memo(height - 1, left_leaf(root),
                                            left_leaf, right_leaf),
        "right": gen_bin_tree_recursive_memo(height - 1, right_leaf(root),
                                             left_leaf, right_leaf),
    }


@lru_cache(maxsize=None)
def gen_bin_tree_recursive_lru(height: int = 4, root: int = 3,
                               left_leaf: Leaf = lambda x: x + 2,
                               right_leaf: Leaf = lambda x: x * 3) -> Tree:
    """Рекурсивное построение с functools.lru_cache."""
    if height < 0:
        raise ValueError("height должна быть не меньше 0")
    if height == 0:
        return {"value": root, "left": None, "right": None}
    return {
        "value": root,
        "left": gen_bin_tree_recursive_lru(height - 1, left_leaf(root),
                                           left_leaf, right_leaf),
        "right": gen_bin_tree_recursive_lru(height - 1, right_leaf(root),
                                            left_leaf, right_leaf),
    }


def gen_bin_tree_iterative_memo(height: int = 4, root: int = 3,
                                left_leaf: Leaf = lambda x: x + 2,
                                right_leaf: Leaf = lambda x: x * 3) -> Tree:
    """Нерекурсивно; поддерево (значение, высота) строится один раз."""
    if height < 0:
        raise ValueError("height должна быть не меньше 0")
    tree: Tree = {"value": root, "left": None, "right": None}
    cache: Dict[Tuple[int, int], Tree] = {(root, height): tree}
    stack = [(tree, height)]
    while stack:
        node, h = stack.pop()
        if h == 0:
            continue
        for side, f in (("left", left_leaf), ("right", right_leaf)):
            key = (f(node["value"]), h - 1)
            if key not in cache:
                cache[key] = {"value": key[0], "left": None, "right": None}
                stack.append((cache[key], h - 1))
            node[side] = cache[key]
    return tree
