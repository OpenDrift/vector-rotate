import pytest

def pytest_addoption(parser):
    parser.addoption("--plot",
                     action="store_true",
                     default=False,
                     help="show plots")

@pytest.fixture
def plot(pytestconfig):
    return pytestconfig.getoption('plot')

