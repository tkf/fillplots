import numpy

from ..api import Plotter
from ..regions import contiguous_groups


def test_get_xlim_when_flipped():
    plotter = Plotter([
        [(-7,),                 # x > -7
         (-5,),                 # x > -5
         (5, True),             # x < 5
         (7, True),             # x < 7
        ],
    ], xlim=(10, -10))
    (region,) = plotter.regions
    assert region._get_xlim() == (-5, 5)


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


def test_fill_domain():
    from ..regions import SDOr
    dom12 = (1, 2)
    plotter = Plotter([
        SDOr([(lambda x: (1.0 - (x - 1) ** 2) ** 0.5, True, dom12),
              (lambda x: 0.5 * (x - 1), False, dom12),
              (lambda x: 2.0 * (x - 1), True, dom12)]),
    ])
    xs = numpy.linspace(0, 2, 5)
    (lower, upper) = plotter.regions[0]._y_lower_upper(xs)
    desired_mask = [True] * 2 + [False] * 3
    numpy.testing.assert_equal(lower.mask, desired_mask)
    numpy.testing.assert_equal(upper.mask, desired_mask)
