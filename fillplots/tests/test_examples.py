import os
import operator
import unittest

from ..utils.py3compat import execfile
from .testing import assert_point_in_collection


def mapcall(name, iterative):
    return list(map(operator.methodcaller(name), iterative))


class TestExamples(unittest.TestCase):

    from os.path import abspath, dirname, join
    root_path = join(dirname(dirname(dirname(abspath(__file__)))),
                     'doc', 'source', 'examples')

    def run_example(self, name):
        self.ns = ns = {}
        filename = os.path.join(self.root_path, name)
        execfile(filename, ns)
        self.plotter = plotter = ns['plotter']
        self.config = plotter.config
        self.ax = plotter.cax.ax

    def assert_number_of_lines(self, num):
        lines = self.ax.get_lines()
        assert len(lines) == num

    def test_simple(self):
        self.run_example('simple.py')
        self.assert_number_of_lines(2)

    def test_two(self):
        self.run_example('two.py')
        self.assert_number_of_lines(4)

    def test_config_inheritance(self):
        self.run_example('config_inheritance.py')
        ax = self.ax
        lines = ax.get_lines()
        colors = mapcall('get_color', lines)
        widths = mapcall('get_linewidth', lines)
        assert colors == ['blue'] + ['black'] * 3
        assert widths == [5] + [1.0] * 3

    def test_switching(self):
        self.run_example('switching.py')
        self.assert_number_of_lines(8)

    def test_switching_uniq_boundary(self):
        self.run_example('switching_uniq_boundary.py')
        ax = self.ax
        lines = ax.get_lines()
        colors = mapcall('get_color', lines)
        assert colors == ['b', 'k', 'k', 'g', 'r']

    def test_switching_region_color(self):
        from matplotlib.colors import colorConverter
        from numpy.testing import assert_almost_equal
        self.run_example('switching_region_color.py')
        actual_colors = mapcall('get_facecolor', self.ax.collections)
        desired_colors = [[colorConverter.to_rgba('gray')]] * 3
        assert_almost_equal(actual_colors, desired_colors)

    def test_positive_direction(self):
        self.run_example('positive_direction.py')
        ax = self.ax
        lines = ax.get_lines()
        colors = mapcall('get_color', lines)
        assert colors[:2] == ['b', 'g']
        assert set(colors) == set(['b', 'g'])

    def test_boundary_labels(self):
        self.run_example('boundary_labels.py')
        ax = self.ax
        leg = ax.get_legend()
        labels = [text.get_text() for text in leg.texts]
        assert labels == ['$x ^ 2$', '$x + 5$']

    def test_annotate_regions(self):
        self.run_example('annotate_regions.py')
        from matplotlib import pyplot
        pyplot.draw()

    def test_divide_regions(self):
        self.run_example('divide_regions.py')
        from matplotlib import pyplot
        pyplot.draw()

    def test_explicit_regions(self):
        self.run_example('explicit_regions.py')
        (r0, r1) = self.plotter.regions
        assert len(r0.cax.collections) == 1
        assert len(r1.cax.collections) == 1

        c0 = r0.cax.collections[0]
        c1 = r1.cax.collections[0]
        assert_point_in_collection(c0, 0 + 0.5, 0.5)
        assert_point_in_collection(c1, 1 + 0.5, 0.5)
        assert_point_in_collection(c0, 0 + 1.0, 1.0, negate=True)
        assert_point_in_collection(c1, 1 + 1.0, 1.0)
