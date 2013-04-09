from fillplots import plot_regions, And, SDOr
dom01 = (0, 1)
dom12 = (1, 2)
plotter = plot_regions([
    And([(lambda x: (1.0 - x ** 2) ** 0.5, True, dom01),
         (lambda x: 0.5 * x, False, dom01),
         (lambda x: 2.0 * x, True, dom01)]),
    SDOr([(lambda x: (1.0 - (x - 1) ** 2) ** 0.5, True, dom12),
        (lambda x: 0.5 * (x - 1), False, dom12),
        (lambda x: 2.0 * (x - 1), True, dom12)]),
], xlim=(0, 2), ylim=(0, 1))
