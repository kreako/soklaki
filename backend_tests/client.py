import os
import requests
from dotenv import load_dotenv


load_dotenv()
# Hasura admin Secret
HASURA_GRAPHQL_ADMIN_SECRET = os.getenv("HASURA_GRAPHQL_ADMIN_SECRET")
# Graphql endpoint
HASURA_GRAPHQL_ENDPOINT = os.getenv("HASURA_GRAPHQL_ENDPOINT")
# Rest endpoint prefix
HASURA_REST_ENDPOINT = os.getenv("HASURA_REST_ENDPOINT")

ADMIN_HEADERS = {"X-Hasura-Admin-Secret": HASURA_GRAPHQL_ADMIN_SECRET}


def _gql(query, variables, headers):
    data = {"query": query, "variables": variables}
    r = requests.post(HASURA_GRAPHQL_ENDPOINT, json=data, headers=headers)
    assert r.status_code == 200
    return r.json()


def admin_gql(query, variables):
    return _gql(query, variables, ADMIN_HEADERS)


def gql(query, variables, token):
    headers = {"Authorization": f"Bearer {token}"}
    return _gql(query, variables, headers)


def _post(endpoint, data, headers):
    url = f"{HASURA_REST_ENDPOINT}/{endpoint}"
    r = requests.post(url, json=data, headers=headers)
    return (r.status_code, r.json())


def admin_post(endpoint, data):
    return _post(endpoint, data, ADMIN_HEADERS)


def anonymous_post(query, variables):
    headers = {}
    return _post(query, variables, headers)


def post(query, variables, token):
    headers = {"Authorization": f"Bearer {token}"}
    return _post(query, variables, headers)
