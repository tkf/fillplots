from collections import MutableMapping


class Struct(object):

    """
    Chain-able struct (Like ChainMap, but for dot-access).

    >>> zero = Struct()       # most upstream struct
    >>> one = Struct(zero)
    >>> two = Struct(one)     # most downstream struct

    Setting attributes of the upstream objects "propagate" to downstream
    objects.

    >>> zero.alpha = 0
    >>> two.alpha
    0
    >>> one.alpha = 1
    >>> (zero.alpha, one.alpha, two.alpha)
    (0, 1, 1)

    :class:`Struct` has special treatment for dictionary attributes.
    Dictionaries of the same attribute in the upstream structs are mixed
    in the down stream structs.

    >>> zero.beta = {'gamma': 10}
    >>> one.beta = {'delta': 20}
    >>> two.beta['gamma']
    10
    >>> two.beta['delta']
    20
    >>> two.beta == {'gamma': 10, 'delta': 20}
    True

    Note that changing downstream dictionaries does not change upstream ones.

    >>> 'delta' in zero.beta
    False
    >>> two.beta['epsilon'] = 30
    >>> 'epsilon' in one.beta
    False

    Setting whole dictionary works as expected.

    >>> one.beta = {'gamma': 110, 'delta': 120}
    >>> two.beta['gamma']
    110
    >>> two.beta['delta']
    120

    """

    def __init__(self, *args, **kwds):
        if args:
            (base,) = args
        else:
            base = None
        self._set_base(base)

        for (key, value) in kwds.items():
            setattr(self, key, value)

    def _set_base(self, base):
        # FIXME: implement "multiple inheritance"?
        self.__base = base

    def _getbaseattr(self, name):
        return getattr(self.__base, name)

    def __setattr__(self, name, value):
        if isinstance(value, MutableMapping) and not isinstance(value, Dict):
            value = Dict(self, name, value)
        super(Struct, self).__setattr__(name, value)

    def __getattr__(self, name):
        value = self._getbaseattr(name)
        if isinstance(value, MutableMapping):
            value = Dict(self, name)
            setattr(self, name, value)
        return value


class Dict(MutableMapping):

    """
    A `dict`-like object for :class:`Struct` attributes.

    See also :meth:`Struct.__setattr__`.

    """

    def __init__(self, struct, name, *args, **kwds):
        self._data = dict(*args, **kwds)
        self._struct = struct
        self._name = name

    def _basedict(self):
        return self._struct._getbaseattr(self._name)

    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError as e:
            try:
                return self._basedict()[key]
            except AttributeError:
                pass
            raise e

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __keyset(self):
        try:
            basedict = self._basedict()
        except AttributeError:
            return set(self._data)
        else:
            return set(self._data) | set(basedict)

    def __iter__(self):
        return iter(self.__keyset())

    def __len__(self):
        return len(self.__keyset())
