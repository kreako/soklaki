import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel

from gql_client import GqlClient, GqlClientException
import socle
import invitation
from jwt_token import generate_jwt_token

load_dotenv()
# Secret to hash password
ARGON2_SECRET = os.getenv("ARGON2_SECRET")
# Hasura admin Secret
HASURA_GRAPHQL_ADMIN_SECRET = os.getenv("HASURA_GRAPHQL_ADMIN_SECRET")
# JWT key encryption
HASURA_GRAPHQL_JWT_SECRET = os.getenv("HASURA_GRAPHQL_JWT_SECRET")
# Graphql endpoint
HASURA_GRAPHQL_ENDPOINT = os.getenv("HASURA_GRAPHQL_ENDPOINT")
# Invitation secret
INVITATION_SECRET = os.getenv("INVITATION_SECRET")


app = FastAPI()
Password = PasswordHasher()
gql_client = GqlClient(HASURA_GRAPHQL_ENDPOINT, HASURA_GRAPHQL_ADMIN_SECRET)


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
    token = generate_jwt_token(HASURA_GRAPHQL_JWT_SECRET, user_id, group_id)
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
        gql_client.update_password(user["id"], Password.hash(plaintext_password))


@app.post("/login")
async def login(login: LoginInput):
    user = await gql_client.find_user_by_email(login.input.email)
    try:
        Password.verify(user["hash"], login.input.password)
        # TODO rehash if needed
        token = generate_jwt_token(
            HASURA_GRAPHQL_JWT_SECRET, user["id"], user["group_id"]
        )
        return LoginOutput(
            error=False, token=token, id=user["id"], group_id=user["group_id"]
        )
    except VerifyMismatchError:
        return LoginOutput(error=True)


@app.post("/load_socle")
async def load_socle(input: socle.LoadSocleInput):
    return await socle.load(gql_client, input)


@app.post("/invitation_generate_token")
async def invitation_generate_token(input: invitation.GenerateTokenInput):
    return await invitation.generate_token(gql_client, INVITATION_SECRET, input)


@app.post("/invitation_verify_token")
async def invitation_verify_token(input: invitation.VerifyTokenInput):
    return await invitation.verify_token(gql_client, INVITATION_SECRET, input)


@app.post("/invitation_signup_token")
async def invitation_signup_token(input: invitation.SignupTokenInput):
    return await invitation.signup_token(
        gql_client, INVITATION_SECRET, Password, HASURA_GRAPHQL_JWT_SECRET, input
    )


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
