from ineqfill import plot_inequalities
clg = plot_inequalities([
    [(lambda x: x ** 2,),
     (lambda x: x + 5,)],
    [(lambda x: - x ** 2, True),
     (lambda x: x - 5, True)],
])
