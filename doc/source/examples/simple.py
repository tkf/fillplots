from fillplots import plot_inequalities
plotter = plot_inequalities([
    [(lambda x: x ** 2,),  # x ^ 2 > 0 or
     (lambda x: x + 5,)],  # x + 5 > 0
])
