import unittest
from contextlib import contextmanager


class DummyMouseEvent(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


@contextmanager
def mpl_bind(obj, name, value):
    """
    Bind `value` to `name` attribute of `obj` within this context.
    """
    getter = getattr(obj, 'get_{0}'.format(name))
    setter = getattr(obj, 'set_{0}'.format(name))
    orig = getter()
    try:
        setter(value)
        yield
    finally:
        setter(orig)


def assert_point_in_collection(collection, x, y, negate=False):
    """
    Check if ``(x, y)`` is in the region defined by `collection`.

    :type collection: :class:`matplotlib.collections.Collection`
    :arg  collection:
    :arg float x: x in data coordinate
    :arg float y: y in data coordinate

    """
    ax = collection.get_axes()
    # Transform data coordinate into display (pixel) coordinate
    point = ax.transData.transform_point((x, y))
    with mpl_bind(collection, 'picker', 0.0):
        (inside, info) = collection.contains(DummyMouseEvent(*point))
    if negate:
        assert not inside
    else:
        assert inside


class PlottableTestCase(unittest.TestCase):

    """
    Test case that can be executed to show plot.
    """

    def setUp(self):
        self.plot()

    def plot(self):
        """
        Set :attr:`plotter` and run plot function.
        """
