import numpy

from .core import Configurable
from .boundaries import (
    BaseBoundary, YFunctionBoundary, XConstBoundary, to_boundary)


class BaseInequality(Configurable):

    def __init__(self, baseconfig, data, less=False, domain=None):
        super(BaseInequality, self).__init__(baseconfig)
        bclass = self._boundaryclass
        if isinstance(data, bclass):
            assert domain is None
            self.boundary = data
        else:
            self.boundary = bclass(self.config, data, domain=domain)
        self.less = less


class YFunctionInequality(BaseInequality):

    _boundaryclass = YFunctionBoundary

    def plot_positive_direction(self):
        ax = self.config.ax
        (ymin, ymax) = self.config.ylim
        (xmin, xmax) = self.boundary._domain or self.config.xlim
        xs = numpy.linspace(xmin, xmax, self.config.num_direction_arrows + 2)
        xs = xs[1:-1]
        ys = self.boundary._masked_y(xs)
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


_IEQ_CLASSES = [YFunctionInequality, XConstInequality]
_IEQ_CLASS_MAP = dict((cls._boundaryclass, cls) for cls in _IEQ_CLASSES)


def to_inequality(config, obj):
    if isinstance(obj, BaseInequality):
        # FIXME: should I care other cases?
        obj.config._set_base(config)
        return obj
    obj = tuple(obj)
    if isinstance(obj[0], BaseBoundary):
        data = to_boundary(config, obj[0])
        return _IEQ_CLASS_MAP[data.__class__](config, data, *obj[1:])
    elif callable(obj[0]):
        return YFunctionInequality(config, *obj)
    else:
        return XConstInequality(config, *obj)
