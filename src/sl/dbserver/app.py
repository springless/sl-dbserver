import typing as _t
import fastapi as _fapi
import dataclasses as _dc
from slugify import slugify
from pydantic import BaseModel
from . import db_util as _dbu
from . import types as _types

@_dc.dataclass
class MakeDBParams:
    conn: str


class CreateDbSuccess(BaseModel):
    result: _t.Literal["Ok"] = "Ok"
    url: str

def create_db(args: _types.CreateDbArgs = _fapi.Body()) -> _types.CreatedDb:
    """Create a new database based on the passed-in connection string and options.
    """
    conn_url = _dbu.make_url(args.url)
    if isinstance(conn_url, _types.ApiError):
        raise conn_url.to_httperr()

    if not conn_url.database:
        raise Exception("No database found in parsed URL string")

    new_conn_url = conn_url.set(database=conn_url.database + "-" + slugify(args.append_name))

    return _types.CreatedDb(url=str(new_conn_url))

def build_app():
    app = _fapi.FastAPI()

    app.post("/create")(create_db)

    return app

main = build_app()
