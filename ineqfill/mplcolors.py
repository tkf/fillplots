from matplotlib import rcParams
from matplotlib.colors import colorConverter


def alpha_compositing(fg, bg, alpha):
    return tuple(f * alpha + g * (1.0 - alpha) for (f, g) in zip(fg, bg))


def fill_color_list(alpha=0.5, colors=None, bg=(1, 1, 1)):
    if colors is None:
        colors = rcParams['axes.color_cycle']
    rgbs = map(colorConverter.to_rgb, colors)
    return [alpha_compositing(fg, bg, alpha) for fg in rgbs]
