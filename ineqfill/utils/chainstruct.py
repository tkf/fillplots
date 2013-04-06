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

    Note that changing downstream dictionaries does not change upstream ones.

    >>> 'delta' in zero.beta
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
        self._base = base

    def __setattr__(self, name, value):
        if isinstance(value, dict) and not isinstance(value, Dict):
            value = Dict(self, name, value)
        super(Struct, self).__setattr__(name, value)

    def __getattr__(self, name):
        return getattr(self._base, name)


class Dict(dict):

    """
    A subclass of `dict` which is used for :class:`Struct` attributes.

    See also :meth:`Struct.__setattr__`.

    """

    def __init__(self, struct, name, *args, **kwds):
        super(Dict, self).__init__(*args, **kwds)
        self._struct = struct
        self._name = name

    def __getitem__(self, key):
        try:
            return super(Dict, self).__getitem__(key)
        except KeyError:
            try:
                basedict = getattr(self._struct._base, self._name)
            except AttributeError:
                pass
            else:
                return basedict[key]
            raise
