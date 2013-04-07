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

    def test_simple(self):
        self.run_example('simple.py')
        ax = self.ax
        lines = ax.get_lines()
        assert len(lines) == 2

    def test_config_inheritance(self):
        self.run_example('config_inheritance.py')
        ax = self.ax
        lines = ax.get_lines()
        colors = mapcall('get_color', lines)
        widths = mapcall('get_linewidth', lines)
        assert colors == ['blue'] + ['black'] * 3
        assert widths == [5] + [1.0] * 3

    def test_switching_uniq_boundary(self):
        self.run_example('switching_uniq_boundary.py')
        ax = self.ax
        lines = ax.get_lines()
        colors = mapcall('get_color', lines)
        assert colors == ['b', 'k', 'k', 'g', 'r']
