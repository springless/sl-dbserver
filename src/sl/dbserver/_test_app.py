import unittest as _ut
import sqlalchemy_utils as _su
import pytest as _pytest
from . import app as _app
from . import types as _types

_TC = _ut.TestCase()


def test_create_drop_test_db(sldb_test_url, sldb_test_schema_module):
    response = _app.create_db(
        _types.CreateDbArgs(
            url=sldb_test_url,
            append_name="test append",
            with_timestamp=True,
            schema=_types.SchemaDef(value=sldb_test_schema_module),
        )
    )
    _TC.assertTrue(_su.database_exists(response.url))
    # destroy the database, afterwards
    _app.drop_db(_types.DropDbArgs(drop_id=response.drop_id))
    _TC.assertFalse(_su.database_exists(response.url))


@_pytest.fixture(scope="function")
def sldb_created_db(sldb_test_url, sldb_test_schema_module, request):
    """Creates, yields, and cleans up a testing database"""
    test_name = request.node.name
    response = _app.create_db(
        _types.CreateDbArgs(
            url=sldb_test_url,
            append_name=test_name,
            with_timestamp=True,
            schema=_types.SchemaDef(value=sldb_test_schema_module),
        )
    )
    yield response.url
    _app.drop_db(_types.DropDbArgs(drop_id=response.drop_id))
