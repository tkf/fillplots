import numpy
from fillplots import Plotter, annotate_regions
plotter = Plotter([
    [(lambda x: numpy.sin(numpy.pi * x) + 1.1,)],
    [(lambda x: numpy.sin(numpy.pi * x) - 1.1, True)],
], xlim=(0, 4), ylim=(-1, 1))
plotter.plot()
annotate_regions(plotter.regions, 'Annotation')
