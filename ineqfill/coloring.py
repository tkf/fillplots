import itertools

import numpy
from matplotlib import pyplot

from .inequalities import to_inequality, YFunctionInequality, XConstInequality


def add_mask(arr, mask):
    if isinstance(arr.mask, numpy.ndarray):
        arr.mask[mask] = True
    else:
        arr.mask = mask


class Coloring(object):

    def __init__(self, regions, xlim=(-10, 10), ylim=(-10, 10)):
        """
        Initialize a coloring object with a list of regions.

        :type regions: dict
        :arg  regions:
            Each value of dict must be a "region specifier" (see below).

        "Region specifier" must be

        """
        self._regions = [list(map(to_inequality, reg)) for reg in regions]
        self._xlim = xlim
        self._ylim = ylim

    @property
    def _ax(self):
        return pyplot.gca()

    def _set_lim(self):
        self._ax.set_xlim(*self._xlim)
        self._ax.set_ylim(*self._ylim)

    def plot(self):
        self.plot_boundaries()
        self.plot_regions()

    def plot_boundaries(self):
        ax = self._ax
        xs = numpy.linspace(*self._xlim)
        for region in self._regions:
            for ineq in region:
                ineq.plot_boundary(ax, xs)
        self._set_lim()

    def _y_lower_upper(self, region, xs):
        lower = None
        upper = None
        for (key, ineqs) in itertools.groupby(region, lambda x: x.less):
            yslist = [ineq._masked_y(xs) for ineq in ineqs]
            if key:
                upper = numpy.ma.array(yslist).max(axis=0)
            else:
                lower = numpy.ma.array(yslist).min(axis=0)
        if lower is None:
            lower = numpy.ma.array(numpy.ones_like(xs) * self._ylim[0])
        if upper is None:
            upper = numpy.ma.array(numpy.ones_like(xs) * self._ylim[1])
        reverse = lower > upper
        if numpy.any(reverse):
            add_mask(upper, reverse)
            add_mask(lower, reverse)
        return (lower, upper)

    def _xlim_of_region(self, region):
        (xmin, xmax) = self._xlim
        for ieq in region:
            if isinstance(ieq, XConstInequality):
                if ieq.less:
                    xmax = min(xmax, ieq.x)
                else:
                    xmin = max(xmin, ieq.x)
        return (xmin, xmax)

    def plot_regions(self):
        ax = self._ax
        for region in self._regions:
            xs = numpy.linspace(*self._xlim_of_region(region))
            loup_region = [ieq for ieq in region if
                           isinstance(ieq, YFunctionInequality)]
            (lower, upper) = self._y_lower_upper(loup_region, xs)
            ax.fill_between(xs, lower, upper)
        self._set_lim()
