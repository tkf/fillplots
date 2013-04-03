import numpy

from .regions import to_region


def add_mask(arr, mask):
    if isinstance(arr.mask, numpy.ndarray):
        arr.mask[mask] = True
    else:
        arr.mask = mask


class Coloring(object):

    def __init__(self, config, regions):
        self._config = config
        self._regions = [to_region(config, reg) for reg in regions]

    def plot(self):
        self.plot_boundaries()
        self.plot_regions()

    def plot_boundaries(self):
        for region in self._regions:
            region.plot_boundaries()
        self._config.set_lim()

    def plot_regions(self):
        for region in self._regions:
            region.plot_region()
        self._config.set_lim()
