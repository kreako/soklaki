import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import httpx
from typing import Optional
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
# Secret to hash password
ARGON2_SECRET = os.getenv("ARGON2_SECRET")
# Hasura admin Secret
HASURA_GRAPHQL_ADMIN_SECRET = os.getenv("HASURA_GRAPHQL_ADMIN_SECRET")
# JWT key encryption
HASURA_GRAPHQL_JWT_SECRET_KEY = os.getenv("HASURA_GRAPHQL_JWT_SECRET_KEY")
# Graphql endpoint
HASURA_GRAPHQL_ENDPOINT = os.getenv("HASURA_GRAPHQL_ENDPOINT")


app = FastAPI()
Password = PasswordHasher()


def generate_token(user) -> str:
    """
    Generates a JWT compliant with the Hasura spec, given a User object with field "id"
    """
    payload = {
        "https://hasura.io/jwt/claims": {
            "x-hasura-allowed-roles": ["user"],
            "x-hasura-default-role": "user",
            "x-hasura-user-id": user["id"],
        }
    }
    token = jwt.encode(payload, HASURA_JWT_SECRET, "HS256")
    return token.decode("utf-8")


def rehash_and_save_password_if_needed(user, plaintext_password):
    if Password.check_needs_rehash(user["password"]):
        client.update_password(user["id"], Password.hash(plaintext_password))


class GqlClient(object):
    def __init__(self):
        self.headers = {"X-Hasura-Admin-Secret": HASURA_GRAPHQL_ADMIN_SECRET}

    async def run_query(self, query, variables):
        async with httpx.AsyncClient() as client:
            r = await client.post(
                HASURA_GRAPHQL_ENDPOINT,
                headers=self.headers,
                json={
                    "query": query,
                    "variables": variables,
                },
            )
            return r.json()

    async def find_user_by_name(self, name):
        await self.run_query(
            """query UsersByName($name: String!) {
                   users(where: {name: {_eq: $name}}, limit: 1) {
                       id
                       name
                       email
                       password
                   }
               }""",
            {"name": name},
        )

    async def insert_users(self, name, email, hash):
        await self.run_query(
            """mutation InsertUsers($name: String!, $email: String!, $password: String!) {
                   insert_users_one(object: {name: $name, email: $email, password: $password}) {
                       id
                       name
                       email
                       password
                }
            }""",
            {"name": name, "email": email, "password": hash},
        )

    async def update_password(self, id, password):
        await self.run_query(
            """mutation UpdatePassword($id: Int!, $password: String!) {
                   update_users_by_pk(pk_columns: {id: $id}, _set: {password: $password}) {
                       password
                   }
               }""",
            {"id": id, "password": password},
        )


class SignupData(BaseModel):
    name: str
    email: str
    password: str


class SignupInput(BaseModel):
    input: SignupData


@app.post("/signup")
async def signup(signup: SignupInput):
    print("signup", signup)
    return {"Hello": "big world"}


@app.get("/items/{item_id}")
async def login(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# For email confirmation
# from cryptography.fernet import Fernet
# import base64
# k = Fernet.generate_key()
# f = Fernet(k)
# token = base64.urlsafe_b64encode(f.encrypt(f"{user.id}-{timestamp}".encode()))
# ...
# user_id, timestamp = f.decrypt(base64.urlsafe_b64decode(token)).split("-")
# if now() - timestamp > 1 DAY:
#     ...

# For login needs to set :
# X-hasura-User-Id
# X-hasura-User-Group