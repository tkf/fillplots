from fillplots import Plotter, annotate_regions
plotter = Plotter([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
    [(lambda x: - x ** 2, True),
     (lambda x: x - 5, True)],
])
plotter.plot()
annotate_regions(plotter.regions, 'Annotation')
