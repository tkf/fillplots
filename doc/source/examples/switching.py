# To draw complex region, you need to conditionally switch boundaries.

from fillplots import Plotter
plotter = Plotter([
    [(lambda x: x ** 0.5, True),
     (1,),
     (2, True)],
    [(lambda x: x ** 0.5,),
     (lambda x: x, True),
     (2, True)],
    [(lambda x: x * (4 - x) / 2, True),
     (2,)],
], xlim=(0, 4), ylim=(0, 4))
plotter.plot()
