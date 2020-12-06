import os

# Set FAUNADB_KEY to blank to make sure we don't accidentally use the development DB
# during tests.
os.environ["FAUNADB_KEY"] = ""
