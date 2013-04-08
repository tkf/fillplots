from fillplots import plot_regions
plotter = plot_regions([
    [(lambda x: x ** 2,),  # x ^ 2 > 0 or
     (lambda x: x + 5,)],  # x + 5 > 0
])
