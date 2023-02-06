# Springless DB Server (sl-dbserver)

This is a simple Python server for the purpose of spinning up and destroying full copies of a
database on demand. An example use-case is running integration tests with a local postgres
instance in a docker container. Each test can create its own isolated database, run its
tests, and then destroy the created database instance when done.
