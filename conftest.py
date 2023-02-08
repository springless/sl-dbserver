_testdb_help = (
    "URL of the testing server, in standard database URL format; eg: "
    + "`postgresql://user:pass@localhost:5432/test`"
)


def pytest_addoption(parser):
    parser.addoption(
        "--testdb",
        action="store",
        dest="testdb",
        help=_testdb_help,
    )
    parser.addini(
        "testdb",
        help=_testdb_help,
    )
