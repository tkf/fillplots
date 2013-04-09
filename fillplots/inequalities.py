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
            """
            An instance of :class:`.BaseBoundary` instance.
            """
        else:
            self.boundary = bclass(self.config, data, domain=domain)
        self.less = less

    def get_errorbar_kwds(self):
        kwds = {}
        for line in self.boundary.config.lines:
            kwds['boundary_color'] = line.get_color()
            break
        return kwds

    def plot_positive_direction(self):
        """
        Plot direction that makes LHS of the inequality positive.
        """


class YFunctionInequality(BaseInequality):

    _boundaryclass = YFunctionBoundary

    def plot_positive_direction(self):
        self.mpl.yerrorbar(self.boundary._masked_y, self.less,
                           xlim=self.boundary._domain,
                           **self.get_errorbar_kwds())


class XConstInequality(BaseInequality):

    _boundaryclass = XConstBoundary

    def plot_positive_direction(self):
        func = lambda ys: self.x * numpy.ones_like(ys)
        self.mpl.xerrorbar(func, self.less, **self.get_errorbar_kwds())


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
