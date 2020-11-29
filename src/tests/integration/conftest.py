import os
from unittest.mock import patch
import re

import pytest

from src.app.faunadb import FaunadbClient


CAPTURED_MATCH = 1


# Use "session" scope and autouse to run once before all tests.
# This is to make sure that the "localhost" endpoint exists.
@pytest.fixture(scope="session", autouse=True)
def _setup_faunadb():
    os.system(
        "npx fauna add-endpoint http://faunadb:8443/ --alias localhost --key secret"
    )


# Scope "function" means that this only applies to the test function that uses it
@pytest.fixture(scope="function")
def faunadb_client():
    # We create and delete the database for each test, because it's reasonably quick,
    # and simpler than manually deleting all data.
    os.system("npx fauna create-database test --endpoint localhost")

    # Creating an API key produces output in the terminal that includes the following line:
    # secret: <API token>
    create_key_output = os.popen(
        "npx fauna create-key test --endpoint=localhost"
    ).read()
    faunadb_key = (
        re.search("secret: (.+)", create_key_output).group(CAPTURED_MATCH).strip()
    )

    client = FaunadbClient(faunadb_key=faunadb_key)
    client.import_schema()

    # For any test that uses this fixture, we patch the environment variable
    # for the FaunaDB API key and return the client. This way, all FaunaDB calls
    # will use the test DB, and the test function will have a valid client
    # to make DB calls for test setup or assertions.
    with patch.dict("os.environ", {**os.environ, "FAUNADB_KEY": faunadb_key}):
        yield client

    os.system("npx fauna delete-database test --endpoint localhost")
