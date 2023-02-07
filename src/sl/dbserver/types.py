import typing as _t
import pydantic as _pyd
import fastapi as _fapi


class ApiError(_pyd.BaseModel):
    result: _t.Literal["Err"] = "Err"
    message: str

    def to_httperr(self):
        return _fapi.HTTPException(status_code=404, detail=self.message)


class Credentials(_pyd.BaseModel):
    username: str = _pyd.Field(
        title="Username",
        description="Database username",
    )
    password: str = _pyd.Field(
        title="Password",
        description="Database password",
    )


class CreatedDb(_pyd.BaseModel):
    url: str = _pyd.Field(
        title="URL",
        description="URL string to use to connect to the newly-created database",
    )
    drop_id: str = _pyd.Field(
        title="Drop ID", description="Use this value to drop the database later."
    )


class SchemaDef(_pyd.BaseModel):
    """Define how to load the schema"""

    type: _t.Literal["sqlalchemy", "file", "raw", "detect"] = _pyd.Field(
        default="detect",
        title="Type",
        description=(
            "Specifies the type of `value`:\n"
            + "`sqlalchemy` - A path to a sqlalchemy metadata object; eg: "
            + "`sl.module.db:metadata`\n"
            + "`file` - The path to a SQL file that should be run to build the models. It is "
            + "recommended that this be an absolute path, and the file must be resident on "
            + "the same filesystem on which the server is running. eg: `/path/to/file.sql`\n"
            + "`raw` - Raw SQL passed in through the value which will create the schema."
        ),
    )
    value: str = _pyd.Field(
        title="Value",
        description=(
            "Value that corresponds to the type. See the type field for more information."
        ),
    )


class CreateDbArgs(_pyd.BaseModel):
    url: str = _pyd.Field(
        title="Connection string",
        description=(
            "A database connection string, eg: `postgres://user:password@localhost:5432/db_name`. "
            + "The user/password combination must have database CREATE privileges."
        ),
    )
    append_name: str = _pyd.Field(
        default="",
        title="Append name",
        description=(
            "String to append to the database name when creating. Used for differentiating tests"
        ),
    )
    with_timestamp: bool = _pyd.Field(
        default=False,
        title="With timestamp",
        description=(
            'Set to "true" to include a timestamp in a created database name. This can help '
            + "differentiate different runs of the same test"
        ),
    )
    schema_def: SchemaDef = _pyd.Field(
        alias="schema",
        title="Schema Definition",
        description=(
            "Used to create the database schema after the database has been created."
        ),
    )


class DropDbArgs(_pyd.BaseModel):
    drop_id: str = _pyd.Field(
        title="Drop ID",
        description=(
            "The `drop_id` passed back to you from the initial database creation."
        ),
    )
