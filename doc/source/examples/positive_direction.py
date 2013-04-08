from fillplots import Coloring
clg = Coloring([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
])
clg.plot()
clg.plot_positive_direction()
