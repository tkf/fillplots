from ineqfill import Coloring, annotate_regions
clg = Coloring([
    [(lambda x: x ** 2,),
     (lambda x: x * 0.5 + 5,)],  # FIXME: make it work w/o  * 0.5
    [(lambda x: - x ** 2, True),
     (lambda x: x * 0.5 - 5, True)],  # FIXME: make it work w/o  * 0.5
])
clg.plot()
annotate_regions(clg.regions, 'Annotation')
