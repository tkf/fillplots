class Config(object):

    def __init__(self, **kwds):
        # FIXME: write arguments explicitly
        self.__dict__.update(kwds)

    @property
    def ax(self):
        from matplotlib import pyplot
        return pyplot.gca()  # FIXME

    def set_lim(self):
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)
