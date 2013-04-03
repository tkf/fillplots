from .core import Config, ModifiedConfig
from . import coloring


styles = {
    'none': Config(),
    'default': Config(
        fill_args={'alpha': 0.5},
    ),
}


class Coloring(coloring.Coloring):

    def __init__(self, regions, config='default',
                 xlim=(-10, 10), ylim=(-10, 10)):
        base = styles.get(config, config)
        config = ModifiedConfig(base, xlim=xlim, ylim=ylim)
        super(Coloring, self).__init__(config, regions)


def plot_inequalities(regions, *args, **kwds):
    """
    Initialize a coloring object with a list of regions.

    :type regions: dict
    :arg  regions:
        Each value of dict must be a "region specifier" (see below).

    "Region specifier" must be

    """
    plotkwds = {}
    if 'ax' in kwds:
        plotkwds['ax'] = kwds.pop('ax')
    clg = Coloring(regions, *args, **kwds)
    clg.plot(**plotkwds)
    return clg
