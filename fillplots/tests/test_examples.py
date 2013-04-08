import os
import operator
import unittest


def mapcall(name, iterative):
    return map(operator.methodcaller(name), iterative)


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
        self.ax = plotter.config.ax

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
