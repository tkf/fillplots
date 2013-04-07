import numpy

from .core import Configurable


class BaseBoundary(Configurable):

    def __init__(self, config, domain=None):
        super(BaseBoundary, self).__init__(config)
        self._domain = domain


class YFunctionBoundary(BaseBoundary):

    def __init__(self, config, func, *args, **kwds):
        super(YFunctionBoundary, self).__init__(config, *args, **kwds)
        self._func = func

    def _masked_y(self, xs):
        if self._domain is None:
            return self._func(xs)
        xs = numpy.ma.array(xs)
        (xmin, xmax) = self._domain
        xs.mask = xs.mask | xs < xmin
        xs.mask = xs.mask | xs > xmax
        return numpy.ma.array(self._func(xs), mask=xs.mask)

    def plot_boundary(self):
        xs = numpy.linspace(*self.config.xlim)
        ys = self._masked_y(xs)
        self.config.plot(xs, ys)


class XConstBoundary(BaseBoundary):

    def __init__(self, config, x, *args, **kwds):
        super(XConstBoundary, self).__init__(config, *args, **kwds)
        self.x = x

    def plot_boundary(self):
        self.config.axvline(self.x)


def to_boundary(config, obj):
    if isinstance(obj, BaseBoundary):
        # FIXME: should I care other cases?
        obj.config._set_base(config)
        return obj
    obj = tuple(obj)
    if callable(obj[0]):
        return YFunctionBoundary(config, *obj)
    else:
        return XConstBoundary(config, *obj)


def boundary(*obj):
    return to_boundary(None, obj)
