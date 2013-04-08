from .core import Config
from . import coloring


styles = {
    'none': {},
    'default': dict(
        fill_args={'autocolor': True},
    ),
}


def get_config(name):
    if name in styles:
        return Config(**styles[name])


class Plotter(coloring.Coloring):

    """
    Initialize a coloring object with a list of regions.

    :type regions: list
    :arg  regions:
        Each value of list must be a "region specifier" (see below).

    :type config: str or Config
    :arg  config:
        ``'default'``, ``'none'`` or a :class:`core.Config` object.

    :type xlim: (int, int)
    :arg  xlim:
    :type ylim: (int, int)
    :arg  ylim:

    "Region specifier" is a list of "inequality specifiers".
    Each "inequality specifier" is a tuple of ``(data[, less[, domain]])``.

    `data` is either a callable or a number.  If it is a callable,
    this defines y of boundary as a function of x.  If it is a number
    it is a vertical boundary, inidicated by that number.

    `less` is a bool.  True means *<* (less than) and False means *>*
    (larger than).  Default is False.

    `domain` is a pair ``(xmin, xmax)`` which indicates defined region
    of the function.

    An example of specifying "*x^2 > 0* or *x + 5 > 0*" is::

    >>> clg = Plotter(
    ...     [  # Regions:
    ...         [  # Inequalities:
    ...              (lambda x: x ** 2,),  # <-- Boundary data
    ...              (lambda x: x + 5,)
    ...         ],
    ...     ])

    You can access each "layer" like this:

    >>> clg.regions[0]
    <fillplots.regions... object at 0x...>
    >>> clg.regions[0].inequalities[0]
    <fillplots.inequalities... object at 0x...>
    >>> clg.regions[0].inequalities[0].boundary
    <fillplots.boundaries... object at 0x...>

    Each "layer" has configuration object which can be modified.

    >>> clg.regions[0].inequalities[0].boundary.config
    <fillplots.core.Config object at 0x...>
    >>> clg.regions[0].inequalities[0].config
    <fillplots.core.Config object at 0x...>
    >>> clg.regions[0].config
    <fillplots.core.Config object at 0x...>
    >>> clg.config
    <fillplots.core.Config object at 0x...>

    """

    def __init__(self, regions, config='default',
                 xlim=(-10, 10), ylim=(-10, 10)):
        config = get_config(config) or config
        super(Plotter, self).__init__(config, regions)
        self.config.xlim = xlim
        self.config.ylim = ylim


def plot_inequalities(regions, *args, **kwds):
    """
    Create :class:`Plotter` object and call plot function of it.

    :type ax: :class:`matplotlib.axes.Axes`
    :arg  ax: Inequalities are drawn on this axes if given.

    """
    plotkwds = {}
    if 'ax' in kwds:
        plotkwds['ax'] = kwds.pop('ax')
    clg = Plotter(regions, *args, **kwds)
    clg.plot(**plotkwds)
    return clg
