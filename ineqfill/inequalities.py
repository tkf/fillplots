import numpy

from .core import Configurable
from .boundaries import YFunctionBoundary, XConstBoundary


class BaseInequality(Configurable):

    def __init__(self, config, data, less=False, domain=None):
        super(BaseInequality, self).__init__(config)
        self.boundary = self._boundaryclass(self.config, data, domain=domain)
        self.less = less


class YFunctionInequality(BaseInequality):

    _boundaryclass = YFunctionBoundary

    def plot_positive_direction(self):
        ax = self.config.ax
        (ymin, ymax) = self.config.ylim
        (xmin, xmax) = self._domain or self.config.xlim
        xs = numpy.linspace(xmin, xmax, self.config.num_direction_arrows + 2)
        xs = xs[1:-1]
        ys = self._masked_y(xs)
        dy = (ymax - ymin) * self.config.direction_arrows_size
        kwds = dict(fmt=None)
        kwds.update({('lolims' if self.less else 'uplims'): True})
        # FIMXE: use the same color as the line itself
        ax.errorbar(xs, ys, yerr=dy, **kwds)


class XConstInequality(BaseInequality):

    _boundaryclass = XConstBoundary

    def plot_positive_direction(self):
        ax = self.config.ax
        (ymin, ymax) = self.config.ylim
        (xmin, xmax) = self.config.xlim
        ys = numpy.linspace(ymin, ymax, self.config.num_direction_arrows + 2)
        ys = ys[1:-1]
        xs = self.x * numpy.ones_like(ys)
        dx = (xmax - xmin) * self.config.direction_arrows_size
        kwds = dict(fmt=None)
        kwds.update({('xlolims' if self.less else 'xuplims'): True})
        ax.errorbar(xs, ys, xerr=dx, **kwds)


def to_inequality(config, obj):
    if isinstance(obj, BaseInequality):
        return obj
    obj = tuple(obj)
    if callable(obj[0]):
        return YFunctionInequality(config, *obj)
    else:
        return XConstInequality(config, *obj)
