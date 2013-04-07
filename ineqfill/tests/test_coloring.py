import operator

from ..api import Coloring
from ..boundaries import boundary


def mapcall(name, iterative):
    return map(operator.methodcaller(name), iterative)


def test_simple():
    clg = Coloring([
        [(lambda x: x ** 2,),
         (lambda x: x + 5,)],
    ])
    clg.plot()

    ax = clg.config.ax
    lines = ax.get_lines()
    assert len(lines) == 2


def test_config_inheritance():
    clg = Coloring([
        [(lambda x: x ** 2,),
         (lambda x: x + 5,)],
        [(lambda x: - x ** 2, True),
         (lambda x: x - 5, True)],
    ])
    clg.config.line_args = {'color': 'black'}
    clg.regions[0].inequalities[0].config.line_args = {'color': 'blue',
                                                       'linewidth': 5}
    clg.plot()

    ax = clg.config.ax
    lines = ax.get_lines()
    colors = mapcall('get_color', lines)
    widths = mapcall('get_linewidth', lines)
    assert colors == ['blue'] + ['black'] * 3
    assert widths == [5] + [1.0] * 3


def test_switching_uniq_boundary():
    sqrt = boundary(lambda x: x ** 0.5)
    one = boundary(1)
    two = boundary(2)

    one.config.line_args = {'color': 'k', 'linestyle': 'dashed'}
    two.config.line_args = {'color': 'k', 'linestyle': 'dotted'}

    clg = Coloring([
        [(sqrt, True), (one,), (two, True)],
        [(sqrt,), (lambda x: x, True), (two, True)],
        [(lambda x: x * (4 - x) / 2, True),
         (two,)],
    ], xlim=(0, 4), ylim=(0, 4))
    clg.plot()

    ax = clg.config.ax
    lines = ax.get_lines()
    colors = mapcall('get_color', lines)
    assert colors == ['b', 'k', 'k', 'g', 'r']
