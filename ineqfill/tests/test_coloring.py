from ..api import Coloring


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
    colors = [l.get_color() for l in lines]
    widths = [l.get_linewidth() for l in lines]
    assert colors == ['blue'] + ['black'] * 3
    assert widths == [5] + [1.0] * 3
