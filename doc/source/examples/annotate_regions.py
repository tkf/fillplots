from fillplots import Plotter, annotate_regions
clg = Plotter([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
    [(lambda x: - x ** 2, True),
     (lambda x: x - 5, True)],
])
clg.plot()
annotate_regions(clg.regions, 'Annotation')
