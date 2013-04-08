# [[[cog import cog; cog.outl('"""\n%s\n"""' % file('../README.rst').read())]]]
"""
fillplots -- Library to plot regions and boundaries given inequalities
======================================================================

Links:

* `Documentation <http://fillplots.readthedocs.org/>`_ (at Read the Docs)
* `Repository <https://github.com/tkf/fillplots>`_ (at GitHub)
* `Issue tracker <https://github.com/tkf/fillplots/issues>`_ (at GitHub)
* `PyPI <http://pypi.python.org/pypi/fillplots>`_
* `Travis CI <https://travis-ci.org/#!/tkf/fillplots>`_ |build-status|


License
-------

`fillplots` is licensed under the terms of the BSD 2-Clause License.
See the COPYING for more information.

"""
# [[[end]]]

from .api import *
from .boundaries import boundary
from .regions import annotate_regions

__version__ = '0.0.1.dev0'
__author__ = 'Takafumi Arakaki'
__license__ = 'BSD License'
