from .testing import PlottableTestCase

from ..api import Plotter
from ..boundaries import boundary
from ..regions import annotate_regions
from .testing import assert_point_in_collection


class TestAnnotationWithFlippedXLim(PlottableTestCase):

    def plot(self):
        upper = boundary(lambda x: - x + 1)
        lower = boundary(lambda x: - x - 1)
        steeper = boundary(lambda x: 1.5 * - x - 1)
        flatter = boundary(lambda x: 0.7 * - x + 1)
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
        ], xlim=(0, -6), ylim=(0, 6))

        plotter.plot()

        annotate_regions(plotter.regions[:1], 'Low region')
        annotate_regions(plotter.regions[1:], 'High region')

        ax = plotter.ax
        self.points = [(-5, 5), (-1.5, 2.2), (-1.5, 1.5), (-1.5, 0.7)]
        for (i, (x, y)) in enumerate(self.points):
            ax.plot(x, y, 'o', label='p{0}'.format(i))
        ax.legend(loc='upper left')

    def test_point_inside(self):
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

    def test_annotations_are_in_region(self):
        ax = self.plotter.ax
        for (region, text) in zip(self.plotter.regions, ax.texts):
            (collection,) = region.cax.collections
            assert_point_in_collection(collection, *text.get_position())
