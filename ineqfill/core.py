import itertools

import numpy

from .utils.chainstruct import Struct
from .mplcolors import fill_color_list


class Config(Struct):

    # Should be renamed to "Resource?"

    def __init__(self, *args, **kwds):
        # FIXME: write arguments explicitly
        self.line_args = {}
        self.fill_args = {}
        self.num_direction_arrows = 5
        self.direction_arrows_size = 0.03
        super(Config, self).__init__(*args, **kwds)

        if not hasattr(self, 'fill_color_cycle'):
            self.fill_color_cycle = itertools.cycle(fill_color_list())
            # FIXME: this does not work when initialized before the base
            #        config (and then base config is set afterwards).

    @property
    def ax(self):
        from matplotlib import pyplot
        return pyplot.gca()  # FIXME

    def set_lim(self):
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)

    def plot(self, *args, **kwds):
        kwds.update(self.line_args)
        self.ax.plot(*args, **kwds)

    def axvline(self, *args, **kwds):
        kwds.update(self.line_args)
        self.ax.axvline(*args, **kwds)

    def fill_between(self, *args, **kwds):
        """
        Configurable :meth:`matplotlib.axes.Axes.fill_between`.

        It can take additional keyword argument `autocolor`, which is
        not defined in matplotlib.  It looks like there is no good way
        to eliminate edge color natively by matplotlib [1]_.  `autocolor`
        can be used to set `facecolor` and `edgecolor` to the same color.
        If `facecolor` is specified, it is used.  Otherwise, the color is
        generated from :attr:`fill_color_cycle`.

        .. [1] See:
           http://stackoverflow.com/questions/14143092/
           http://permalink.gmane.org/gmane.comp.python.matplotlib.general/996

        """
        kwds.update(self.fill_args)
        if kwds.pop('autocolor', False):
            color = kwds.get('facecolor') or next(self.fill_color_cycle)
            kwds.update(
                facecolor=color,
                edgecolor=color,
                alpha=1,
                # this does not work in some backend?:
                linewidth=0,
            )
        self.ax.fill_between(*args, **kwds)

    def _errorbar(self, orientation, func, **kwds):
        kwds.setdefault('fmt', None)
        (xmin, xmax) = kwds.pop('xlim', None) or self.xlim
        (ymin, ymax) = kwds.pop('ylim', None) or self.ylim
        if orientation == 'y':
            (umin, umax, vmin, vmax) = (xmin, xmax, ymin, ymax)
        else:
            (umin, umax, vmin, vmax) = (ymin, ymax, xmin, xmax)
        us = numpy.linspace(umin, umax, self.num_direction_arrows + 2)[1:-1]
        vs = func(us)
        delta = (vmax - vmin) * self.direction_arrows_size
        if orientation == 'y':
            (xs, ys) = (us, vs)
            kwds.update(yerr=delta)
        else:
            (xs, ys) = (vs, us)
            kwds.update(xerr=delta)
        # FIMXE: use the same color as the line itself
        self.ax.errorbar(xs, ys, **kwds)

    def yerrorbar(self, func, less=False, **kwds):
        kwds.setdefault('lolims' if less else 'uplims', True)
        self._errorbar('y', func, **kwds)

    def xerrorbar(self, func, less=False, **kwds):
        kwds.setdefault('xlolims' if less else 'xuplims', True)
        self._errorbar('x', func, **kwds)


class Configurable(object):

    def __init__(self, baseconfig):
        self.config = Config(baseconfig)
