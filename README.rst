fillplots -- Library to plot regions and boundaries given inequalities
======================================================================

.. sidebar:: Links:

   * `Documentation <http://fillplots.readthedocs.org/>`_ (at Read the Docs)

     - `Examples <http://fillplots.readthedocs.org/en/latest/examples.html>`_

   * `Repository <https://github.com/tkf/fillplots>`_ (at GitHub)
   * `Issue tracker <https://github.com/tkf/fillplots/issues>`_ (at GitHub)
   * `PyPI <http://pypi.python.org/pypi/fillplots>`_
   * `Travis CI <https://travis-ci.org/#!/tkf/fillplots>`_ |build-status|

``fillplots`` is a library to plot regions and boundaries given
systems of inequality.  Here is a simple example to fill region like
a piece of pie.

>>> from fillplots import plot_regions
>>> plot_regions([
...     [(lambda x: (1.0 - x ** 2) ** 0.5, True),
...      (lambda x: x,)]
... ], xlim=(0, 1), ylim=(0, 1))
<fillplots.api.Plotter object at 0x...>

See documentation_ and examples_ for more information.

License
-------

`fillplots` is licensed under the terms of the BSD 2-Clause License.
See the COPYING for more information.


.. |build-status|
   image:: https://secure.travis-ci.org/tkf/fillplots.png?branch=master
   :target: http://travis-ci.org/tkf/fillplots
   :alt: Build Status
