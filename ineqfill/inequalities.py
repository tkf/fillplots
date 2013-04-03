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

    def plot_boundary(self, ax, xs):
        # FIXME: load `xs` and `ax` from self.config
        ax.plot(xs, self._masked_y(xs), **self.config.line_args)


class XConstInequality(BaseInequality):

    def __init__(self, config, x, *args, **kwds):
        super(XConstInequality, self).__init__(config, *args, **kwds)
        self.x = x

    def plot_boundary(self, ax, _):
        ax.axvline(self.x, **self.config.line_args)


def to_inequality(config, obj):
    if isinstance(obj, BaseInequality):
        return obj
    obj = tuple(obj)
    if callable(obj[0]):
        return YFunctionInequality(config, *obj)
    else:
        return XConstInequality(config, *obj)
