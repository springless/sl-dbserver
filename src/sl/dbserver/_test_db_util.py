from unittest import TestCase as _TestCase
import datetime as _dt
from . import db_util as _dbu
from . import types as _types

_TC = _TestCase()

_use_timestamp = _dt.datetime.strptime(
    "2022-04-23 14:05:34",
    "%Y-%m-%d %H:%M:%S",
)

def test_make_db_name(sldb_test_url: str):
    url = _dbu.make_url(sldb_test_url)
    if isinstance(url, _types.ApiError) or url.database is None:
        raise Exception(f"Problem with the sldb_test_url being used: {sldb_test_url}")
    created_name = _dbu.make_db_name(
        url.database,
        append="My appended string",
        at_timestamp=_use_timestamp,
    )
    _TC.assertEqual(
        created_name,
        "20220423140534_test_my_appended_string",
    )
