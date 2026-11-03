"""Замеры timeit и графики: python benchmark.py."""

import timeit
from statistics import mean
from typing import Any, Callable, Dict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import memo_tree as m  # noqa: E402

HEIGHTS = list(range(2, 19, 2))  # 18 - предел: <1 с без мемоизации
IMPLS: Dict[str, Callable[..., Any]] = {
    "recursive": m.gen_bin_tree_recursive,
    "iterative": m.gen_bin_tree_iterative,
    "recursive_memo": m.gen_bin_tree_recursive_memo,
    "iterative_memo": m.gen_bin_tree_iterative_memo,
    "recursive_lru": m.gen_bin_tree_recursive_lru,
}
# вариант 13: root=13, left=x+1, right=x-1
VARIANTS = {"v3": (3, lambda x: x + 2, lambda x: x * 3),
            "v13": (13, lambda x: x + 1, lambda x: x - 1)}


def clear(f: Callable[..., Any]) -> None:
    """Очистить кэш, если он есть."""
    if hasattr(f, "cache_clear"):
        f.cache_clear()


def run(f: Callable[..., Any], args: tuple, again: bool) -> float:
    """Среднее время одного вызова (5 запусков)."""
    def setup() -> None:
        clear(f)
        if again:
            f(*args)
    return mean(timeit.repeat(lambda: f(*args), setup=setup,
                              number=1, repeat=5))


def main() -> None:
    """Замеры, графики и подсчёт вызовов left_leaf/right_leaf."""
    for vn, (root, left, right) in VARIANTS.items():
        for scen, again in (("single", False), ("repeat", True)):
            plt.figure()
            for name, f in IMPLS.items():
                if again and not hasattr(f, "cache_clear") \
                        and name != "recursive":
                    continue  # у iterative_memo кэш локальный
                ts = [run(f, (h, root, left, right), again) for h in HEIGHTS]
                plt.plot(HEIGHTS, ts, marker="o", label=name)
                print(vn, scen, name, [f"{t*1000:.3f}" for t in ts])
            plt.yscale("log")
            plt.xlabel("height")
            plt.ylabel("время, с")
            plt.title(f"{vn}, {scen}")
            plt.legend()
            plt.savefig(f"plot_{vn}_{scen}.png", dpi=110)
            plt.close()
        for name in ("recursive", "recursive_memo", "iterative_memo"):
            cnt = [0, 0]
            l = lambda x: (cnt.__setitem__(0, cnt[0] + 1), left(x))[1]
            r = lambda x: (cnt.__setitem__(1, cnt[1] + 1), right(x))[1]
            clear(IMPLS[name])
            IMPLS[name](16, root, l, r)
            clear(IMPLS[name])
            print(vn, name, "left/right вызовов при h=16:", cnt)
        m.gen_bin_tree_recursive_lru.cache_clear()
        m.gen_bin_tree_recursive_lru(16, root, left, right)
        print(vn, "lru cache_info:", m.gen_bin_tree_recursive_lru.cache_info())


if __name__ == "__main__":
    main()
