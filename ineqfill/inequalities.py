import numpy

from .core import Configurable


class BaseInequality(Configurable):

    def __init__(self, config, less=False, domain=None):
        super(BaseInequality, self).__init__(config)
        self.less = less
        self._domain = domain


class YFunctionInequality(BaseInequality):

    def __init__(self, config, func, *args, **kwds):
        """

          func(x) > 0

        """
        super(YFunctionInequality, self).__init__(config, *args, **kwds)
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

    def __init__(self, config, x, *args, **kwds):
        super(XConstInequality, self).__init__(config, *args, **kwds)
        self.x = x

    def plot_boundary(self):
        ax = self.config.ax
        ax.axvline(self.x, **self.config.line_args)

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
