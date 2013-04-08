fillplots API
=============

.. autoclass:: fillplots.Plotter
   :inherited-members:
.. autofunction:: fillplots.plot_regions
.. autofunction:: fillplots.boundary
.. autofunction:: fillplots.annotate_regions


Internal classes
----------------

These classes are not meant to initialized from outside of this library.
But you can access their instance via :class:`Plotter` and call their
methods.

.. inheritance-diagram::
   fillplots.Plotter
   fillplots.boundaries.BaseBoundary
   fillplots.inequalities.BaseInequality
   fillplots.regions.BaseRegion
   :parts: 1

.. autoclass:: fillplots.boundaries.BaseBoundary
.. autoclass:: fillplots.inequalities.BaseInequality
.. autoclass:: fillplots.regions.BaseRegion


Configuration interface
-----------------------

.. inheritance-diagram::
   fillplots.core.Config
   :parts: 1

.. autoclass:: fillplots.core.Config

.. autoclass:: fillplots.utils.chainstruct.Struct
