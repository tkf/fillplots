import itertools

import numpy

from .core import Configurable
from .inequalities import to_inequality, YFunctionInequality, XConstInequality


def add_mask(arr, mask):
    if isinstance(arr.mask, numpy.ndarray):
        arr.mask[mask] = True
    else:
        arr.mask = mask


class Region(Configurable):

    def __init__(self, config, ineqs):
        super(Region, self).__init__(config)
        self.inequalities = [to_inequality(self.config, iq) for iq in ineqs]

    def _get_xlim(self):
        (xmin, xmax) = self.config.xlim
        for ineq in self.inequalities:
            if isinstance(ineq, XConstInequality):
                if ineq.less:
                    xmax = min(xmax, ineq.boundary.x)
                else:
                    xmin = max(xmin, ineq.boundary.x)
        return (xmin, xmax)

    def _y_funcs(self):
        ineqs = [ieq for ieq in self.inequalities if
                 isinstance(ieq, YFunctionInequality)]
        lower_fs = []
        upper_fs = []
        for (key, ineqs) in itertools.groupby(ineqs, lambda x: x.less):
            if key:
                upper_fs.extend(ineq.boundary._masked_y for ineq in ineqs)
            else:
                lower_fs.extend(ineq.boundary._masked_y for ineq in ineqs)

        def make_func(fs, lim, bound):
            if fs:
                return lambda x: bound(numpy.ma.array([f(x) for f in fs]),
                                       axis=0)
            else:
                return lambda x: numpy.ma.array(numpy.ones_like(x)) * lim

        (ymin, ymax) = self.config.ylim
        return (make_func(lower_fs, ymin, numpy.min),
                make_func(upper_fs, ymax, numpy.max))

    def _y_lower_upper(self, xs):
        (lower_f, upper_f) = self._y_funcs()
        lower = lower_f(xs)
        upper = upper_f(xs)

        reverse = lower > upper
        if numpy.any(reverse):
            add_mask(upper, reverse)
            add_mask(lower, reverse)
        return (lower, upper)

    def plot_boundaries(self):
        for ineq in self.inequalities:
            ineq.boundary.plot_boundary()

    def plot_region(self):
        xs = numpy.linspace(*self._get_xlim())
        (lower, upper) = self._y_lower_upper(xs)
        self.config.fill_between(xs, lower, upper)

    @property
    def endpoints(self):
        """
        2D array: [lower-left, lower-right, upper-left, upper-right]
        """
        xs = numpy.array(self._get_xlim())
        (lower, upper) = self._y_lower_upper(xs)
        return numpy.array([
            [xs[0], lower[0]],
            [xs[1], lower[1]],
            [xs[0], upper[0]],
            [xs[1], upper[1]],
        ])

    def is_contiguous_to(self, regions):
        """
        Check if this region is contiguous to one of region in `regions`.

        Current implementation returns True if the following relationship
        is (nearly) satisfied::

            regions[i].endpoints[j] == self.endpoints[k]

        """
        endpoitns = self.endpoints
        (xmin, xmax) = self.config.xlim
        eps = (xmax - xmin) * 1e-5
        for reg in regions:
            if mindist(endpoitns, reg.endpoints) < eps:
                return True
        return False


to_region = Region


def mindist(ps, qs):
    xps = numpy.concatenate((ps,) * len(qs))
    xqs = numpy.repeat(qs, len(ps), axis=0)
    dist = numpy.sum((xps - xqs) ** 2, axis=1)
    assert len(ps) * len(qs) == len(dist)
    return numpy.sqrt(dist.min())


def contiguous_groups(regions):
    """
    Divide regions into contiguous groups.
    """
    if len(regions) == 0:
        return

    pivot = regions[0]
    groups = iter(contiguous_groups(regions[1:]))
    for group in groups:
        if pivot.is_contiguous_to(group):
            yield [pivot] + group
            break
        else:
            yield group
    else:
        yield [pivot]
    for group in groups:
        yield group


def endpoints(regions):
    """
    Combine most outer endpont` of `regions`.
    """
    points = numpy.array([r.endpoints for r in regions])
    lls = points[:, 0]
    lrs = points[:, 1]
    uls = points[:, 2]
    urs = points[:, 3]
    lla = numpy.array([-1, -1])
    lra = numpy.array([+1, -1])
    ula = numpy.array([-1, +1])
    ura = numpy.array([+1, +1])
    llp = lls[numpy.argmax(numpy.dot(lls, lla))]
    lrp = lrs[numpy.argmax(numpy.dot(lrs, lra))]
    ulp = uls[numpy.argmax(numpy.dot(uls, ula))]
    urp = urs[numpy.argmax(numpy.dot(urs, ura))]
    return numpy.array([llp, lrp, ulp, urp])


def center(regions):
    (llp, lrp, ulp, urp) = endpoints(regions)
    tricom = lambda a, b, c: (a + b + c) / 3.0
    triarea = lambda a, b, c: numpy.cross(b - a, c - a) / 2.0
    x = tricom(llp, lrp, ulp)
    y = tricom(lrp, ulp, urp)
    A = triarea(llp, lrp, ulp)
    B = triarea(lrp, ulp, urp)
    C = A + B
    return (A * x + B * y) / C


def annotate_regions(regions, text,
                     horizontalalignment='center',
                     verticalalignment='center',
                     **kwds):
    """
    Annotate `regions` with `text`.

    Put only one annotation for each contiguous group of regions.

    :type regions: [Region]
    :arg  regions:
    :type    text: str
    :arg     text:

    Other keywords are passed to :meth:`matplotlib.axes.Axes.text`.

    """
    # FIXME: Split regions before feeding it into `contiguous_groups`.
    #        One `Region` instance may have several divided regions.
    #        Use mlab.contiguous_regions(- numpy.isnan(upper - lower)).
    # FIXME: More annotation styles.  Arrows?  Points with legend?
    for group in contiguous_groups(regions):
        ax = group[0].config.ax
        (x, y) = center(group)
        ax.text(x, y, text,
                horizontalalignment=horizontalalignment,
                verticalalignment=verticalalignment,
                **kwds)
