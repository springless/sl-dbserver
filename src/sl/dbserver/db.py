import sqlalchemy.engine as _sae
import pathlib as _pl
from .util import file as _fu
from . import types as _types
from .util.db import schema as _dbus
from .util.db import seed as _db_seed


def create_schema(url: _sae.URL | str, schema: _types.SchemaDef):
    """Uses the schema definition to create the schema inside the passed database url"""
    match schema.type:
        case "sqlalchemy":
            _dbus.load_sqlalchemy_schema(url, schema.value)


def _seed_data_from_file(fname: str) -> _types.SeedData:
    fext = _pl.Path(fname).suffix.lower()
    match fext:
        case ".json":
            ftype = "json"
        case ".sql":
            ftype = "sql"
        case _:
            raise _types.ApiError(
                message=f"File type extension not recognized, must be `sql` or `json`: {fname}"
            ).to_httperr()
    with open(fname, "r") as f:
        fdata = f.read()

    return _types.SeedData(type=ftype, value=fdata)


def _seed_data_from_module(modname: str) -> _types.SeedData:
    try:
        fname = _fu.module_path(modname)
    except ValueError as e:
        raise _types.ApiError(message=str(e)).to_httperr()
    return _seed_data_from_file(fname)


def load_seed_data(url: _sae.URL | str, seed: _types.SeedData):
    if seed.type == "file":
        seed = _seed_data_from_file(seed.value)
    if seed.type == "module":
        seed = _seed_data_from_module(seed.value)

    # at this point seed should have either a "json" or "sql" type
    match seed.type:
        case "json":
            _db_seed.load_json_seed(url, seed.value)
        case "sql":
            _db_seed.load_sql_seed(url, seed.value)
