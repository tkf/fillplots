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
    Plotter to fill regions with colors.

    :type regions: list
    :arg  regions:
        Each value of list must be a "region specifier" (see below).

    :type config: str or Config
    :arg  config:
        ``'default'``, ``'none'`` or a :class:`core.Config` object.

    :type xlim: (int, int)
    :arg  xlim: Limit for x-axis.  Default is ``(-10, 10)``.
    :type ylim: (int, int)
    :arg  ylim: Limit for y-axis.  Default is ``(-10, 10)``.

    "Region specifier" is a list of "inequality specifiers".
    Each "inequality specifier" is a tuple of ``(data[, less[, domain]])``.

    `data` is either a callable or a number.  If it is a callable,
    this defines y of boundary as a function of x.  If it is a number
    it is a vertical boundary, inidicated by that number.

    `less` is a bool.  True means *<* (less than) and False means *>*
    (larger than).  Default is False.

    `domain` is a pair ``(min, max)`` which indicates defined region
    of the function.  It can be None, which means that this inequality
    is defined for any real number.

    An example of specifying "*x^2 > 0* or *x + 5 > 0*" is:

    >>> plotter = Plotter(
    ...     [  # Regions:
    ...         [  # Inequalities:
    ...              (lambda x: x ** 2,),  # <-- Boundary data
    ...              (lambda x: x + 5,)
    ...         ],
    ...     ])


    **Internal representation**

    You can access internal representation as follows.
    First, :attr:`regions` attribute of this class holds a list of
    :class:`.BaseRegion` instances:

    >>> plotter.regions
    [<fillplots.regions... object at 0x...>]

    Each region object has :attr:`inequalities <.BaseRegion.inequalities>`
    attribute, which holds a list of :class:`.BaseInequality` instances:

    >>> plotter.regions[0].inequalities    # doctest: +NORMALIZE_WHITESPACE
    [<fillplots.inequalities... object at 0x...>,
     <fillplots.inequalities... object at 0x...>]

    Finally, each inequality object has :attr:`boundary
    <.BaseInequality.boundary>` attribute to hold an instance of
    :class:`.BaseBoundary`.

    >>> plotter.regions[0].inequalities[0].boundary
    <fillplots.boundaries... object at 0x...>


    **Configuration interface**

    Each of these "layer" has an instance of :class:`.Config` object
    whose attributes can be modified.

    >>> plotter.regions[0].inequalities[0].boundary.config
    <fillplots.core.Config object at 0x...>
    >>> plotter.regions[0].inequalities[0].config
    <fillplots.core.Config object at 0x...>
    >>> plotter.regions[0].config
    <fillplots.core.Config object at 0x...>
    >>> plotter.config
    <fillplots.core.Config object at 0x...>

    Modifying upstream configuration propagates to downstream configuration.
    Let's consider the following configuration:

    >>> plotter.config.line_args['ls'] = 'dotted'
    >>> plotter.config.line_args['lw'] = 8
    >>> plotter.regions[0].inequalities[0].config.line_args['ls'] = 'dashed'

    The boundary object of the 0th inequality mixes the configurations of
    the inequality and the root plotter object.

    >>> plotter.regions[0].inequalities[0].boundary.config.line_args['ls']
    'dashed'
    >>> plotter.regions[0].inequalities[0].boundary.config.line_args['lw']
    8

    The configuration for the 0th inequality does not effect to the
    1st inequality and its down stream.  So, the configuration of the
    root plotter object is used:

    >>> plotter.regions[0].inequalities[1].boundary.config.line_args['ls']
    'dotted'

    """

    def __init__(self, regions, config='default',
                 xlim=(-10, 10), ylim=(-10, 10)):
        config = get_config(config) or config
        super(Plotter, self).__init__(config, regions)
        self.config.xlim = xlim
        self.config.ylim = ylim


def plot_regions(regions, *args, **kwds):
    """
    Create :class:`.Plotter` object and call plot function of it.

    All arguments are passed to :class:`.Plotter`.

    :rtype: :class:`.Plotter`

    """
    # FIXME: Passing ax to plot functions is not implemented:
    """
    :type ax: :class:`matplotlib.axes.Axes`
    :arg  ax: Inequalities are drawn on this axes if given.

    Other arguments are passed to :class:`.Plotter`.
    """
    plotkwds = {}
    if 'ax' in kwds:
        raise NotImplementedError(
            'Passing ax to plot functions is not implemented')
        plotkwds['ax'] = kwds.pop('ax')
    plotter = Plotter(regions, *args, **kwds)
    plotter.plot(**plotkwds)
    return plotter
