"""A file containing fixtures exported automatically by pytest for every suite
built in this directory."""
import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--runslow', action='store_true', default=False, help='run slow tests'
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption('--runslow'):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason='need --runslow option to run')
    for item in items:
        if 'slow' in item.keywords:
            item.add_marker(skip_slow)
