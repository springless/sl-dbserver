import pytest as _pytest


@_pytest.fixture(scope="function")
def sldb_test_url(pytestconfig) -> str:
    """The test connection to use for this test run"""
    db_url = pytestconfig.getoption("--testdb")
    if db_url is None:
        db_url = pytestconfig.getini("testdb")
    return db_url
