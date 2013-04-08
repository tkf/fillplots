from distutils.core import setup

import fillplots

setup(
    name='fillplots',
    version=fillplots.__version__,
    packages=['fillplots', 'fillplots.utils', 'fillplots.tests'],
    author=fillplots.__author__,
    author_email='aka.tkf@gmail.com',
    url='https://github.com/tkf/fillplots',
    license=fillplots.__license__,
    description='Library to plot regions and boundaries given inequalities',
    long_description=fillplots.__doc__,
    keywords='matplotlib, plot, inequality',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
)
