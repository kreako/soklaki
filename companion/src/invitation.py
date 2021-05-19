from logging import exception
from pydantic import BaseModel, Field
from typing import Optional
from cryptography import fernet
import base64
import binascii
from datetime import datetime, timedelta
import json
import random
import string

from gql_client import GqlClientException
from jwt_token import generate_jwt_token


class HasuraHeaders(BaseModel):
    x_hasura_user_id: int = Field(alias="x-hasura-user-id")
    x_hasura_user_group: int = Field(alias="x-hasura-user-group")


class GenerateTokenData(BaseModel):
    user_id: int
    group_id: int


class GenerateTokenInput(BaseModel):
    input: GenerateTokenData
    session_variables: HasuraHeaders


class GenerateTokenOutput(BaseModel):
    token: str


async def generate_token(gql_client, invitation_secret, input: GenerateTokenInput):
    f = fernet.Fernet(invitation_secret)
    now = datetime.now()
    content = json.dumps(
        {
            "user_id": input.input.user_id,
            "group_id": input.input.group_id,
            "now": now.isoformat(),
        }
    )
    token = base64.urlsafe_b64encode(f.encrypt(content.encode()))
    return GenerateTokenOutput(token=token)


class VerifyTokenData(BaseModel):
    token: str


class VerifyTokenInput(BaseModel):
    input: VerifyTokenData


class VerifyTokenOutput(BaseModel):
    valid: bool
    too_old: bool
    group_id: Optional[int]
    group_name: Optional[str]
    user_id: Optional[int]
    user_firstname: Optional[str]
    user_lastname: Optional[str]


class InvalidToken(Exception):
    pass


class TooOldToken(Exception):
    pass


MAX_OLD = timedelta(days=3)


def _verify_token(invitation_secret, token):
    f = fernet.Fernet(invitation_secret)

    try:
        decoded_token = base64.urlsafe_b64decode(token)
    except binascii.Error:
        raise InvalidToken()

    try:
        content = f.decrypt(decoded_token)
    except fernet.InvalidToken:
        raise InvalidToken()

    data = json.loads(content)

    try:
        tokenDt = datetime.fromisoformat(data["now"])
    except ValueError:
        raise InvalidToken()

    now = datetime.now()
    if now - tokenDt > MAX_OLD:
        raise TooOldToken()

    return data


async def verify_token(gql_client, invitation_secret, input: VerifyTokenInput):
    try:
        data = _verify_token(invitation_secret, input.input.token)
    except InvalidToken:
        return VerifyTokenOutput(valid=False, too_old=False)
    except TooOldToken:
        return VerifyTokenOutput(valid=False, too_old=True)

    user_id = data["user_id"]
    group_id = data["group_id"]
    group = await gql_client.group_by_id(group_id)
    group_name = group["name"]

    user = await gql_client.user_by_id(user_id)
    user_firstname = user["firstname"]
    user_lastname = user["lastname"]

    return VerifyTokenOutput(
        valid=True,
        too_old=False,
        group_id=group_id,
        group_name=group_name,
        user_id=user_id,
        user_firstname=user_firstname,
        user_lastname=user_lastname,
    )


class SignupTokenData(BaseModel):
    token: str
    email: str
    password: str


class SignupTokenInput(BaseModel):
    input: SignupTokenData


class SignupTokenOutput(BaseModel):
    valid: bool
    too_old: bool
    error_weak_password: bool
    token: Optional[str]
    user_id: Optional[int]
    group_id: Optional[int]


def random_string(k):
    return "".join(random.choices(string.ascii_letters + string.digits, k=k))


async def signup_token(
    gql_client, invitation_secret, Password, jwt_secret, input: SignupTokenInput
):
    try:
        data = _verify_token(invitation_secret, input.input.token)
    except InvalidToken:
        return SignupTokenOutput(valid=False, too_old=False, error_weak_password=False)
    except TooOldToken:
        return SignupTokenOutput(valid=False, too_old=True, error_weak_password=False)

    group_id = data["group_id"]
    email = input.input.email

    # hash of the password
    h = Password.hash(input.input.password)

    # Let's check if the user with this email already exists
    existing_user = await gql_client.user_by_email(email)
    if existing_user:
        # Update it to inactive and patch email with randomness
        existing_user_id = existing_user[0]["id"]
        new_email = f"{email}  {random_string(256)}"
        await gql_client.update_user(
            user_id=existing_user_id, active=False, email=new_email
        )

    # Now create the user
    user_id = await gql_client.insert_user_one(group_id, email, h)

    # Now compute jwt
    token = generate_jwt_token(jwt_secret, user_id, group_id)

    return SignupTokenOutput(
        valid=True,
        too_old=False,
        error_weak_password=False,
        token=token,
        user_id=user_id,
        group_id=group_id,
    )
