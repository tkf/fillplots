import numpy

from .core import Configurable


class BaseBoundary(Configurable):

    def __init__(self, config, domain=None):
        super(BaseBoundary, self).__init__(config)
        self._domain = domain

    def plot_boundary(self):
        """
        Plot this boundary.
        """


class YFunctionBoundary(BaseBoundary):

    def __init__(self, config, func, *args, **kwds):
        super(YFunctionBoundary, self).__init__(config, *args, **kwds)
        self._func = func

    def _masked_y(self, xs):
        if self._domain is None:
            return self._func(xs)
        xs = numpy.ma.array(xs)
        (xmin, xmax) = self._domain
        xs.mask = numpy.ma.mask_or(xs.mask, xs < xmin)
        xs.mask = numpy.ma.mask_or(xs.mask, xs > xmax)
        return numpy.ma.array(self._func(xs), mask=xs.mask)

    def plot_boundary(self):
        num = self.config.num_boundary_samples
        xs = numpy.linspace(*self.config.xlim, num=num)
        ys = self._masked_y(xs)
        self.cax.plot(xs, ys)


class XConstBoundary(BaseBoundary):

    def __init__(self, config, x, *args, **kwds):
        super(XConstBoundary, self).__init__(config, *args, **kwds)
        self.x = x

    def plot_boundary(self):
        self.cax.axvline(self.x)


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


def boundary(function_or_number, domain=None):
    """
    Boundary factory function.

    :type function_or_number: callable or number
    :arg  function_or_number:
        If it is a callable, it is assumed to be a function that maps
        x to y.  If it is a number, the boundary is a straight line
        specified by `x = <number>`.

    :type domain: (number, number) or None
    :arg  domain:
        The boundary is defined on this domain.  If it is None, the
        boundary is defined for any real number.  If the argument
        `function_or_number` is a callable, the domain is on
        x-axis.  If `function_or_number` is a number, the domain is
        on y-axis.

    :rtype: :class:`.BaseBoundary`
    :return: An instance of :class:`.BaseBoundary` subclass.

    """
    return to_boundary(None, (function_or_number, domain))
