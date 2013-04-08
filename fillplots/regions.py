import itertools

import numpy

from .core import Configurable
from .inequalities import to_inequality, YFunctionInequality, XConstInequality


def add_mask(arr, mask):
    if isinstance(arr.mask, numpy.ndarray):
        arr.mask[mask] = True
    else:
        arr.mask = mask


def center_of_mass(masses, coordinates):
    x = numpy.asarray(coordinates, dtype=float)
    m = numpy.asarray(masses, dtype=float)
    com = numpy.dot(m, x) / m.sum()
    return com


class BaseRegion(Configurable):

    def __init__(self, config, ineqs):
        super(BaseRegion, self).__init__(config)
        self.inequalities = [to_inequality(self.config, iq) for iq in ineqs]

    def plot_boundaries(self):
        """
        Plot boundaries.
        """
        for ineq in self.inequalities:
            ineq.boundary.plot_boundary()

    def plot_region(self):
        """
        Plot this region.
        """


class Region(BaseRegion):

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
                return lambda x: bound([f(x) for f in fs], axis=0)
            else:
                return lambda x: numpy.ones_like(x) * lim

        (ymin, ymax) = self.config.ylim
        return (make_func(lower_fs, ymin, numpy.min),
                make_func(upper_fs, ymax, numpy.max))

    def _y_lower_upper(self, xs):
        (lower_f, upper_f) = self._y_funcs()
        lower = numpy.ma.array(lower_f(xs))
        upper = numpy.ma.array(upper_f(xs))

        (ymin, ymax) = self.config.ylim
        eps = (ymax - ymin) * 1e-5
        reverse = lower - eps > upper
        if numpy.any(reverse):
            add_mask(upper, reverse)
            add_mask(lower, reverse)
        return (lower, upper)

    def plot_region(self):
        num = self.config.num_boundary_samples
        xs = numpy.linspace(*self._get_xlim(), num=num)
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

    def mass_center(self):
        """
        Mass and center of mass.
        """
        num = self.config.num_com_samples
        xs = numpy.linspace(*self._get_xlim(), num=num)
        (lower, upper) = self._y_lower_upper(xs)
        height = (upper - lower)
        coordinates = numpy.array([xs, (upper + lower) / 2.0]).T
        return (height.sum(), center_of_mass(height, coordinates))

    def contiguous_domains(self):
        from matplotlib import mlab
        xlim = self._get_xlim()
        num = self.config.num_boundary_samples
        xs = numpy.linspace(*xlim, num=num)
        (ymin, ymax) = self.config.ylim
        (lower_f, upper_f) = self._y_funcs()
        lower = lower_f(xs)
        upper = upper_f(xs)

        def find_bound(i, fallback):
            xs2 = numpy.linspace(xs[i - 1], xs[i], num_finer)
            diff = upper_f(xs2) - lower_f(xs2)
            try:
                if diff[0] > 0:
                    j = mlab.cross_from_above(diff, 0)[0] - 1
                else:
                    j = mlab.cross_from_below(diff, 0)[0]
                return xs2[j]
            except IndexError:
                return fallback
        num_finer = num

        domains = []
        for (i, j) in mlab.contiguous_regions(lower < upper):
            if i == 0:
                x0 = xlim[0]
            else:
                x0 = find_bound(i, xs[i])
            if j == len(upper):
                x1 = xlim[1]
            else:
                x1 = find_bound(j, xs[j - 1])
            domains.append((x0, x1))

        return domains

    def contiguous_regions(self):
        regions = []
        for (x0, x1) in self.contiguous_domains():
            regions.append(Region(
                self.config,
                self.inequalities + [(x0,), (x1, True)]))
        return regions


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


def center(regions):
    masses = []
    coordinates = []
    for r in regions:
        (m, cs) = r.mass_center()
        masses.append(m)
        coordinates.append(cs)
    return center_of_mass(masses, coordinates)


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
    # FIXME: More annotation styles.  Arrows?  Points with legend?
    regions = reduce(lambda x, r: x + r.contiguous_regions(), regions, [])
    for group in contiguous_groups(regions):
        ax = group[0].config.ax
        (x, y) = center(group)
        ax.text(x, y, text,
                horizontalalignment=horizontalalignment,
                verticalalignment=verticalalignment,
                **kwds)
