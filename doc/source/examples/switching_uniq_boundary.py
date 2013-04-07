# Conditionally switching boundaries make many overlapping boundaries.
# To draw just one line per boundary, you can initialize the boundary
# object before creating the Coloring object.

from ineqfill import boundary, Coloring

# Initialize boundaries individually, so that they are recognized as
# one line rather than line per region.
sqrt = boundary(lambda x: x ** 0.5)
one = boundary(1)
two = boundary(2)

# Boundaries can be configured before registering to `Coloring`.
one.config.line_args = {'color': 'k', 'linestyle': 'dashed'}
two.config.line_args = {'color': 'k', 'linestyle': 'dotted'}

clg = Coloring([
    [(sqrt, True), (one,), (two, True)],
    [(sqrt,), (lambda x: x, True), (two, True)],
    [(lambda x: x * (4 - x) / 2, True),
     (two,)],
], xlim=(0, 4), ylim=(0, 4))

clg.plot()
