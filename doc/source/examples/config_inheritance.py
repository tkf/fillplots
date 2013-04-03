from ineqfill import Coloring
clg = Coloring([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
    [(lambda x: - x ** 2, True),
     (lambda x: x - 5, True)],
])
clg.config.line_args = {'color': 'black'}
clg.regions[0].inequalities[0].config.line_args = {'color': 'blue',
                                                   'linewidth': 5}
clg.plot()
