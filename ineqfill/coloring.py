import numpy

from .core import Configurable
from .regions import to_region


def add_mask(arr, mask):
    if isinstance(arr.mask, numpy.ndarray):
        arr.mask[mask] = True
    else:
        arr.mask = mask


class Coloring(Configurable):

    def __init__(self, config, regions):
        super(Coloring, self).__init__(config)
        self._regions = [to_region(self.config, reg) for reg in regions]

    def plot(self):
        self.plot_boundaries()
        self.plot_regions()

    def plot_boundaries(self):
        for region in self._regions:
            region.plot_boundaries()
        self.config.set_lim()

    def plot_regions(self):
        for region in self._regions:
            region.plot_region()
        self.config.set_lim()
