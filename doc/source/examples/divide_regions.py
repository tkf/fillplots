import numpy
from fillplots import Coloring, annotate_regions
clg = Coloring([
    [(lambda x: numpy.sin(numpy.pi * x) + 1.1,)],
    [(lambda x: numpy.sin(numpy.pi * x) - 1.1, True)],
], xlim=(0, 4), ylim=(-1, 1))
clg.plot()
annotate_regions(clg.regions, 'Annotation')
