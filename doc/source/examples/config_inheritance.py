from fillplots import Plotter
clg = Plotter([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
    [(lambda x: - x ** 2, True),
     (lambda x: x - 5, True)],
])

# Upstream configuration "propagates" to downstream ones:
clg.config.line_args = {'color': 'black'}
# Downstream configuration can be tweaked individually:
clg.regions[0].inequalities[0].config.line_args = {'color': 'blue',
                                                   'linewidth': 5}

clg.plot()
