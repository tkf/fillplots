from fillplots import Plotter
clg = Plotter([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
])
clg.plot()
clg.plot_positive_direction()
