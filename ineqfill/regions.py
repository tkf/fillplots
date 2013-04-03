import itertools

import numpy

from .core import ModifiedConfig
from .inequalities import to_inequality, YFunctionInequality, XConstInequality


def add_mask(arr, mask):
    if isinstance(arr.mask, numpy.ndarray):
        arr.mask[mask] = True
    else:
        arr.mask = mask


class Region(object):

    def __init__(self, config, ineqs):
        self.config = config = ModifiedConfig(config)
        self._ineqs = [to_inequality(config, ineq) for ineq in ineqs]

    def _get_xlim(self):
        (xmin, xmax) = self.config.xlim
        for ineq in self._ineqs:
            if isinstance(ineq, XConstInequality):
                if ineq.less:
                    xmax = min(xmax, ineq.x)
                else:
                    xmin = max(xmin, ineq.x)
        return (xmin, xmax)

    def _y_lower_upper(self, xs):
        lower = None
        upper = None
        ineqs = [ieq for ieq in self._ineqs if
                 isinstance(ieq, YFunctionInequality)]
        for (key, ineqs) in itertools.groupby(ineqs, lambda x: x.less):
            yslist = [ineq._masked_y(xs) for ineq in ineqs]
            if key:
                upper = numpy.ma.array(yslist).max(axis=0)
            else:
                lower = numpy.ma.array(yslist).min(axis=0)

        ylim = self.config.ylim
        if lower is None:
            lower = numpy.ma.array(numpy.ones_like(xs) * ylim[0])
        if upper is None:
            upper = numpy.ma.array(numpy.ones_like(xs) * ylim[1])

        reverse = lower > upper
        if numpy.any(reverse):
            add_mask(upper, reverse)
            add_mask(lower, reverse)
        return (lower, upper)

    def plot_boundaries(self):
        ax = self.config.ax
        # FIXME: option to draw only relevant boundaries
        xs = numpy.linspace(*self.config.xlim)
        for ineq in self._ineqs:
            ineq.plot_boundary(ax, xs)

    def plot_region(self):
        ax = self.config.ax
        xs = numpy.linspace(*self._get_xlim())
        (lower, upper) = self._y_lower_upper(xs)
        ax.fill_between(xs, lower, upper, **self.config.fill_args)


to_region = Region
