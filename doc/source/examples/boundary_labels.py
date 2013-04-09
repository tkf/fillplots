from fillplots import Plotter
plotter = Plotter([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
])
(ineq0, ineq1) = plotter.regions[0].inequalities
ineq0.boundary.config.line_args['label'] = '$x ^ 2$'
ineq1.boundary.config.line_args['label'] = '$x + 5$'
plotter.plot()
plotter.mpl.ax.legend(loc='best')
