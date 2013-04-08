from fillplots import Plotter
plotter = Plotter([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
])
plotter.plot()
plotter.plot_positive_direction()
