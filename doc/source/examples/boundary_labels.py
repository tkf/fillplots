from fillplots import Plotter
plotter = Plotter([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
])
plotter.regions[0].inequalities[0].boundary.config.line_args['label'] = '$x ^ 2$'
plotter.regions[0].inequalities[1].boundary.config.line_args['label'] = '$x + 5$'
plotter.plot()
plotter.config.ax.legend(loc='best')
