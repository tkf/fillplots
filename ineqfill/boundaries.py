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
        ax = self.config.ax
        xs = numpy.linspace(*self.config.xlim)
        ys = self._masked_y(xs)
        ax.plot(xs, ys, **self.config.line_args)


class XConstBoundary(BaseBoundary):

    def __init__(self, config, x, *args, **kwds):
        super(XConstBoundary, self).__init__(config, *args, **kwds)
        self.x = x

    def plot_boundary(self):
        ax = self.config.ax
        ax.axvline(self.x, **self.config.line_args)
