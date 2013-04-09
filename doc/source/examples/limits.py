from fillplots import plot_regions
plotter = plot_regions([
    [(lambda x: (1.0 - x ** 2) ** 0.5, True),
     (lambda x: 0.5 * x,),
     (lambda x: 2.0 * x, True)]
], xlim=(0, 1), ylim=(0, 1))
