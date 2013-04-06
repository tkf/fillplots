from .utils.chainstruct import Struct


class Config(Struct):

    # Should be renamed to "Resource?"

    def __init__(self, *args, **kwds):
        # FIXME: write arguments explicitly
        self.line_args = {}
        self.fill_args = {}
        self.num_direction_arrows = 5
        self.direction_arrows_size = 0.03
        super(Config, self).__init__(*args, **kwds)

    @property
    def ax(self):
        from matplotlib import pyplot
        return pyplot.gca()  # FIXME

    def set_lim(self):
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)


class Configurable(object):

    def __init__(self, baseconfig):
        self.config = Config(baseconfig)
