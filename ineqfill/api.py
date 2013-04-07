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


class Coloring(coloring.Coloring):

    def __init__(self, regions, config='default',
                 xlim=(-10, 10), ylim=(-10, 10)):
        config = get_config(config) or config
        super(Coloring, self).__init__(config, regions)
        self.config.xlim = xlim
        self.config.ylim = ylim


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
