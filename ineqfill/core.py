class BaseConfig(object):

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    @property
    def ax(self):
        from matplotlib import pyplot
        return pyplot.gca()  # FIXME

    def set_lim(self):
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)


class Config(BaseConfig):

    # Should be renamed to "Resource?"

    def __init__(self, **kwds):
        # FIXME: write arguments explicitly
        self.line_args = {}
        self.fill_args = {}
        super(Config, self).__init__(**kwds)


class ModifiedConfig(BaseConfig):

    def __init__(self, base, **kwds):
        self.__base = base
        super(ModifiedConfig, self).__init__(**kwds)

    def __getattr__(self, name):
        return getattr(self.__base, name)


class Configurable(object):

    def __init__(self, config):
        self.config = config = ModifiedConfig(config)
