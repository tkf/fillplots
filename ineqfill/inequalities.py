import numpy


class BaseInequality(object):
    pass


class YFunctionInequality(BaseInequality):

    def __init__(self, config, func, less=False, domain=None):
        """

          func(x) > 0

        """
        self._config = config
        self.less = less
        self._func = func
        self._domain = domain

    def _masked_y(self, xs):
        if self._domain is None:
            return self._func(xs)
        xs = numpy.ma.array(xs)
        (xmin, xmax) = self._domain
        xs.mask = xs.mask | xs < xmin
        xs.mask = xs.mask | xs > xmax
        return numpy.ma.array(self._func(xs), mask=xs.mask)

    def plot_boundary(self, ax, xs):
        ax.plot(xs, self._masked_y(xs), **self._config.line_args)


class XConstInequality(BaseInequality):

    def __init__(self, config, x, less=False, domain=None):
        self._config = config
        self.less = less
        self.x = x
        self._domain = domain

    def plot_boundary(self, ax):
        ax.axvline(self.x, **self._config.line_args)


def to_inequality(config, obj):
    if isinstance(obj, BaseInequality):
        return obj
    obj = tuple(obj)
    if callable(obj[0]):
        return YFunctionInequality(config, *obj)
    else:
        return XConstInequality(config, *obj)
