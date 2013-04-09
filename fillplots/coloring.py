import numpy

from .core import Configurable
from .regions import to_region


def uniq(seq, key=lambda x: x):
    """
    Return unique elements in `seq`, preserving the order.

    >>> list(uniq([0, 1, 0, 2, 1, 2]))
    [0, 1, 2]
    >>> list(uniq(enumerate('iljkiljk'), key=lambda x: x[1]))
    [(0, 'i'), (1, 'l'), (2, 'j'), (3, 'k')]

    """
    seen = set()
    for i in seq:
        k = key(i)
        if k not in seen:
            yield i
            seen.add(k)


def add_mask(arr, mask):
    if isinstance(arr.mask, numpy.ndarray):
        arr.mask[mask] = True
    else:
        arr.mask = mask


class Coloring(Configurable):

    def __init__(self, config, regions):
        super(Coloring, self).__init__(config)
        self.regions = [to_region(self.config, reg) for reg in regions]
        """
        List of :class:`.BaseRegion` instances.
        """

    def plot(self):
        """
        Plot regions and boundaries.
        """
        self.plot_boundaries()
        self.plot_regions()

    def _get_boundaries(self):
        return uniq(iq.boundary for iq in self._get_inequalities())

    def plot_boundaries(self):
        """
        Plot boundaries.
        """
        # FIXME: option to draw only relevant boundaries
        for boundary in self._get_boundaries():
            boundary.plot_boundary()
        self.cax.set_lim()

    def plot_regions(self):
        """
        Plot regions.
        """
        for region in self.regions:
            region.plot_region()
        self.cax.set_lim()

    def _get_inequalities(self):
        ineqs = (iq for region in self.regions for iq in region.inequalities)
        return ineqs

    def plot_positive_direction(self):
        """
        Plot direction that makes LHS of the inequality positive.
        """
        for iq in self._get_inequalities():
            iq.plot_positive_direction()
