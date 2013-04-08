from matplotlib import pyplot
import pytest


@pytest.fixture()
def cleanfigure():  # FIXME: this fixture should not be required
    pyplot.clf()
