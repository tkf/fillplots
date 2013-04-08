from fillplots import Plotter
clg = Plotter([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
])
clg.regions[0].inequalities[0].boundary.config.line_args['label'] = '$x ^ 2$'
clg.regions[0].inequalities[1].boundary.config.line_args['label'] = '$x + 5$'
clg.plot()
clg.config.ax.legend(loc='best')
