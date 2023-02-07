import unittest as _ut
import sqlalchemy_utils as _su
from . import app as _app
import datetime as _dt
from . import types as _types
from .util import db as _dbu

_TC = _ut.TestCase()


def test_create_test_db(sldb_test_url, sldb_test_schema):
    response = _app.create_db(
        _types.CreateDbArgs(
            url=sldb_test_url,
            append_name="test append",
            with_timestamp=True,
            schema=_types.SchemaDef(value="sl.dbserver.__test__.db.models:metadata"),
        )
    )
    _TC.assertTrue(_su.database_exists(response.url))
    # destroy the database, afterwards
    _dbu.drop_database(response.url)
