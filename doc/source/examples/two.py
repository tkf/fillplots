from fillplots import plot_regions
plotter = plot_regions([
    [(lambda x: x ** 2,),         # x ^ 2 > 0 or
     (lambda x: x + 5,)],         # x + 5 > 0
    # Another region (True means to use "<" instead of ">"):
    [(lambda x: - x ** 2, True),  # - x^2 < 0 or
     (lambda x: x - 5, True)],    # x - 5 < 0
])
