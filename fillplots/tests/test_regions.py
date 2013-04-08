from ..api import Plotter
from ..regions import contiguous_groups


def test_contiguous_groups_one():
    linear = lambda a: lambda x: a * x
    sandwich = lambda a, b: [(linear(a), False), (linear(b), True)]
    plotter = Plotter([
        sandwich(0, 0.5),
        sandwich(0.5, 1),
        sandwich(1, 1.5),
    ], xlim=(0, 1), ylim=(0, 1))
    groups = list(contiguous_groups(plotter.regions))
    lengths = list(map(len, groups))
    assert lengths == [3]


def test_contiguous_groups_two_singles():
    plotter = Plotter([
        [(lambda x: x ** 2,),
         (lambda x: x + 5,)],
        [(lambda x: - x ** 2, True),
         (lambda x: x - 5, True)],
    ])
    groups = list(contiguous_groups(plotter.regions))
    lengths = list(map(len, groups))
    assert lengths == [1, 1]
