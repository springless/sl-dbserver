import fastapi as _fapi
import datetime as _dt
from .util import db as _dbu
from . import types as _types


def create_db(args: _types.CreateDbArgs = _fapi.Body()) -> _types.CreatedDb:
    """Create a new database based on the passed-in connection string and options."""
    passed_url = _dbu.make_url(args.url)
    if isinstance(passed_url, _types.ApiError):
        raise passed_url.to_httperr()

    if not passed_url.database:
        raise Exception("No database found in parsed URL string")

    new_url = passed_url.set(
        database=_dbu.make_db_name(
            passed_url.database,
            append=args.append_name or "",
            at_timestamp=_dt.datetime.now() if args.with_timestamp else None,
        )
    )

    _dbu.create_database(new_url)

    return _types.CreatedDb(url=str(new_url), drop_id=str(new_url))


def drop_db(args: _types.DropDbArgs = _fapi.Body()) -> None:
    """Drop a created database"""
    passed_url = _dbu.make_url(args.drop_id)

    if isinstance(passed_url, _types.ApiError):
        raise passed_url.to_httperr()

    if not passed_url.database:
        raise _types.ApiError(
            message="No database found in parsed URL string"
        ).to_httperr()

    _dbu.drop_database(passed_url)

    return None


def build_app():
    app = _fapi.FastAPI()

    app.post("/create")(create_db)

    return app


main = build_app()
