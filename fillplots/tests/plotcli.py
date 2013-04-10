"""
Plot test case.
"""


def import_object(path):
    """
    Import object given dot-separated path.

    :type path: str
    :arg  path: dot-separated path.
                Use `module.class` to do ``from module import class``.

    """
    root = __import__(path.rsplit('.', 1)[0])
    reload(root)
    obj = root
    for p in path.split('.')[1:]:
        obj = getattr(obj, p)
    return obj


def plotcase(caseclass):
    class runnable(caseclass):

        def __init__(self):
            pass

    case = runnable()
    case.plot()

    from matplotlib import pyplot
    pyplot.show()
    return case


def plotcli(classpath):
    return plotcase(import_object(classpath))


def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    parser.add_argument('classpath')
    ns = parser.parse_args()
    return plotcli(**vars(ns))


if __name__ == '__main__':
    ret = main()
