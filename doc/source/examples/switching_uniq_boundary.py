from ineqfill import boundary, Coloring
sqrt = boundary(lambda x: x ** 0.5)
one = boundary(1)
two = boundary(2)

one.config.line_args = {'color': 'k', 'linestyle': 'dashed'}
two.config.line_args = {'color': 'k', 'linestyle': 'dotted'}

clg = Coloring([
    [(sqrt, True), (one,), (two, True)],
    [(sqrt,), (lambda x: x, True), (two, True)],
    [(lambda x: x * (4 - x) / 2, True),
     (two,)],
], xlim=(0, 4), ylim=(0, 4))

clg.plot()
