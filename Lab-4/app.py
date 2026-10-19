"""
Вариант: root=3, height=4, left=r+2, right=r*3.
"""
from collections import deque
from typing import Any, Callable

DEFAULT_LEFT: Callable[[int], int] = lambda r: r + 2
DEFAULT_RIGHT: Callable[[int], int] = lambda r: r * 3


def gen_bin_tree(
    height: int = 4,
    root: int = 3,
    left_leaf: Callable[[int], int] = DEFAULT_LEFT,
    right_leaf: Callable[[int], int] = DEFAULT_RIGHT,
) -> dict[str, Any]:
    """Строит бинарное дерево высоты ``height`` (BFS, без рекурсии).

    Args:
        height: число уровней-потомков под корнем.
        root: значение корня.
        left_leaf: функция левого потомка.
        right_leaf: функция правого потомка.

    Returns:
        Корень — словарь ``{'value', 'left', 'right'}``.
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
