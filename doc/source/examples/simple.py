from ineqfill import plot_inequalities
clg = plot_inequalities([
    [(lambda x: x ** 2,),  # x ^ 2 > 0 or
     (lambda x: x + 5,)],  # x + 5 > 0
])
