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
        self.clg = clg = ns['clg']
        self.config = clg.config
        self.ax = clg.config.ax

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

    def test_positive_direction(self):
        self.run_example('positive_direction.py')
        ax = self.ax
        lines = ax.get_lines()
        colors = mapcall('get_color', lines)
        assert colors[:2] == ['b', 'g']
        assert set(colors) == set(['b', 'g', 'c', 'y'])