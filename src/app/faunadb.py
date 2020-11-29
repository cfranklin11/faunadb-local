import os

import requests
from gql import gql, Client, AIOHTTPTransport
from dotenv import load_dotenv

load_dotenv()

FAUNADB_DOMAIN = "http://localhost:8084"
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


class FaunadbClient:
    def __init__(self, faunadb_key=None):
        self.faunadb_key = faunadb_key or os.getenv("FAUNADB_KEY")

    def import_schema(self, mode="merge"):
        url = f"{FAUNADB_DOMAIN}/import?mode={mode}"
        schema_filepath = os.path.join(ROOT_DIR, "schema.gql")

        with open(schema_filepath, "rb") as f:
            schema_file = f.read()

        requests.post(
            url,
            data=schema_file,
            params={"mode": mode},
            headers=self._headers,
        )

    def create_user(self, username=None, password=None):
        query = """
            mutation($username: String!, $password: String!) {
                createUser(data: {username: $username, password: $password}) {
                    _id
                    username
                    password
                }
            }
        """
        variables = {"username": username, "password": password}

        result = self.graphql(query, variables)
        return result["createUser"]

    def all_users(self):
        query = """
            query {
                allUsers {
                    data {
                        _id
                        username
                        password
                    }
                }
            }
        """

        result = self.graphql(query)
        return result["allUsers"]["data"]

    def graphql(self, query: str, variables=None):
        transport = AIOHTTPTransport(
            url=f"{FAUNADB_DOMAIN}/graphql",
            headers=self._headers,
        )
        graphql_client = Client(transport=transport)

        graphql_query = gql(query)
        graphql_variables = variables or {}

        result = graphql_client.execute(
            graphql_query, variable_values=graphql_variables
        )

        errors = result.get("errors", [])

        if any(errors):
            raise Exception(errors)

        return result

    @property
    def _headers(self):
        return {"Authorization": f"Bearer {self.faunadb_key}"}
