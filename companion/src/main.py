import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import jwt

from gql_client import GqlClient, GqlClientException

load_dotenv()
# Secret to hash password
ARGON2_SECRET = os.getenv("ARGON2_SECRET")
# Hasura admin Secret
HASURA_GRAPHQL_ADMIN_SECRET = os.getenv("HASURA_GRAPHQL_ADMIN_SECRET")
# JWT key encryption
HASURA_GRAPHQL_JWT_SECRET = os.getenv("HASURA_GRAPHQL_JWT_SECRET")
# Graphql endpoint
HASURA_GRAPHQL_ENDPOINT = os.getenv("HASURA_GRAPHQL_ENDPOINT")


app = FastAPI()
Password = PasswordHasher()
gql_client = GqlClient(HASURA_GRAPHQL_ENDPOINT, HASURA_GRAPHQL_ADMIN_SECRET)


def generate_token(user_id, group_id) -> str:
    """
    Generates a JWT compliant with the Hasura spec, given a User object with field "id"
    """
    payload = {
        "https://hasura.io/jwt/claims": {
            "x-hasura-allowed-roles": ["user"],
            "x-hasura-default-role": "user",
            "x-hasura-user-id": str(user_id),
            "x-hasura-user-group": str(group_id),
        }
    }
    token = jwt.encode(payload, HASURA_GRAPHQL_JWT_SECRET, "HS256")
    return token


class SignupData(BaseModel):
    email: str
    password: str


class SignupInput(BaseModel):
    input: SignupData


class SignupOutput(BaseModel):
    errorKnownEmail: bool
    errorWeakPassword: bool
    token: Optional[str]
    id: Optional[int]
    group: Optional[int]


@app.post("/signup")
async def signup(signup: SignupInput):
    # hash of the password
    h = Password.hash(signup.input.password)
    # Create a group for the new user
    group_id = await gql_client.insert_group_one(True)
    # Now create the user
    try:
        user_id = await gql_client.insert_user_one(group_id, signup.input.email, h)
    except GqlClientException:
        # TODO is it safe to assume that this is a known email address ?
        # Delete the created - for nothing - group
        await gql_client.delete_group(group_id)
        # Return the error
        return SignupOutput(
            errorKnownEmail=True,
            errorWeakPassword=False,
            token=None,
            id=None,
            group=None,
        )
    # Now compute jwt
    token = generate_token(user_id, group_id)
    return SignupOutput(
        errorKnownEmail=False,
        errorWeakPassword=False,
        token=token,
        id=user_id,
        group=group_id,
    )


class LoginData(BaseModel):
    email: str
    password: str


class LoginInput(BaseModel):
    input: SignupData


class LoginOutput(BaseModel):
    error: bool
    token: Optional[str]
    id: Optional[int]
    group_id: Optional[int]


def rehash_and_save_password_if_needed(user, plaintext_password):
    if Password.check_needs_rehash(user["password"]):
        client.update_password(user["id"], Password.hash(plaintext_password))


@app.post("/login")
async def login(login: LoginInput):
    user = await gql_client.find_user_by_email(login.input.email)
    try:
        Password.verify(user["hash"], login.input.password)
        # TODO rehash if needed
        token = generate_token(user["id"], user["group_id"])
        return LoginOutput(
            error=False, token=token, id=user["id"], group_id=user["group_id"]
        )
    except VerifyMismatchError:
        return LoginOutput(error=True)


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