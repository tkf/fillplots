from .testing import PlottableTestCase

from ..api import Plotter
from ..regions import annotate_regions
from .testing import assert_point_in_collection


class TestTwoRegionsAnnotation(PlottableTestCase):

    def plot(self):
        upper = lambda x: x + 1
        lower = lambda x: x - 1
        steeper = lambda x: 2 * x - 3
        flatter = lambda x: 0.5 * x + 2
        self.plotter = plotter = Plotter([
            [(upper, True),
             (lower,),
             (steeper, True),
            ],
            [(upper, True),
             (lower,),
             (steeper,),
             (flatter,)
            ],
        ], xlim=(0, 6), ylim=(0, 6))
        plotter.plot()
        annotate_regions(plotter.regions[:1], 'Low region')
        annotate_regions(plotter.regions[1:], 'High region')

        ax = plotter.ax
        self.points = [(5, 5), (3, 3.7), (3, 3.2), (3, 2.5)]
        for (i, (x, y)) in enumerate(self.points):
            ax.plot(x, y, 'o', label='p{0}'.format(i))
        ax.legend(loc='upper left')

    def test(self):
        (r0, r1) = self.plotter.regions
        (c0,) = r0.cax.collections
        (c1,) = r1.cax.collections
        assert_point_in_collection(c0, *self.points[0])
        assert_point_in_collection(c1, *self.points[0], negate=True)
        assert_point_in_collection(c0, *self.points[1], negate=True)
        assert_point_in_collection(c1, *self.points[1])
        assert_point_in_collection(c0, *self.points[2], negate=True)
        assert_point_in_collection(c1, *self.points[2], negate=True)
        assert_point_in_collection(c0, *self.points[3])
        assert_point_in_collection(c1, *self.points[3], negate=True)
