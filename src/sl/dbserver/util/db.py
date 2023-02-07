import sqlalchemy_utils as _su
import sqlalchemy.engine as _sae
import sqlalchemy.exc as _saex
import datetime as _dt
import slugify as _slug
import hashlib as _hashlib
from .. import types as _types


def truncate_for_postgres(name: str) -> str:
    """Postgres can only have a maximum identifier length of 63 characters, so this will take
    a passed-in name and truncate it with an MD5 hash based on the full name appended to the end.
    This is the same way that postgres will rename a too-long identifier when it is created
    under the hood. Postgres seems to cap these shortened names at 60 characters, though, rather
    than taking up the full allowed 63.
    """
    # postgres uses first five characters of md5 of the full string
    if len(name) < 63:
        return name
    hashed = _hashlib.md5(name.encode()).hexdigest()[-4:]
    return name[: 60 - len(hashed)] + hashed


def make_db_name(
    base_name: str, *, append: str = "", at_timestamp: _dt.datetime | None = None
) -> str:
    """Constructs a new database name from a base name, appending a string and a timestamp,
    if provided.

    It will take the format:

    <timestamp>-<base_name>-<append>

    If `timestamp` or `append` are omitted, then that field and the adjacent dash will also
    be omitted. The "append" name is also run through a slugify so may not be verbatim the same
    as it was submitted.

    The default build of Postgresql has trouble with names over 63 characters, and will
    truncate them with a hash at the end. This will also do the same when creating the
    database name, regardless of what database engine is being used.

    Timestamp comes first to ensure that, if the base database name is long enough to trigger
    the postgres shortening algorithm, the timestamp will still be present so the user can
    know which databases were created most recently.
    """
    new_name = "_".join(
        [
            *(
                [at_timestamp.strftime("%Y%m%d%H%M%S")]
                if at_timestamp is not None
                else []
            ),
            base_name,
            *([_slug.slugify(append, separator="_")] if append else []),
        ]
    )
    return truncate_for_postgres(new_name)


def make_url(conn_str: str) -> _sae.URL | _types.ApiError:
    """Light wrapper around SQLAlchemy's URL parser to catch and return a standardized error
    type.
    """
    try:
        return _sae.make_url(conn_str)
    except _saex.ArgumentError:
        return _types.ApiError(message="Invalid URL")


def swap_credentials(url: _sae.URL, credentials: _types.Credentials) -> _sae.URL:
    return url.set(
        username=credentials.username,
        password=credentials.password,
    )


def swap_database(url: _sae.URL, database: str) -> _sae.URL:
    return url.set(
        database=database,
    )


def drop_database(conn_str: _sae.URL | str):
    """Uses the provided connection string to ensure that the database it points to does not
    exist.
    """
    if _su.database_exists(str(conn_str)):
        _su.drop_database(str(conn_str))


def create_database(conn_str: _sae.URL | str):
    """Uses the provided connection string to ensure that the database it points to exists.
    If the database already exists, then it will destroy and recreate it.

    TODO - cogs - 20230206
    If there is a disparity between the user creating the database and the user that will be
    using the database, then will use the admin credentials to create the datbase, and then grant
    creation privileges to the non-admin user.
    """
    drop_database(conn_str)
    if not _su.database_exists(str(conn_str)):
        _su.create_database(str(conn_str))


def load_schema(url: _sae.URL | str, schema: _types.SchemaDef):
    """Uses the schema definition to create the schema inside the passed database url"""
