from pydantic import BaseModel, Field
from typing import Optional

from gql_client import GqlClientException


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


async def generate_token(gql_client, input: GenerateTokenInput):
    return GenerateTokenOutput(token="meuh")


class VerifyTokenData(BaseModel):
    token: str


class VerifyTokenInput(BaseModel):
    input: VerifyTokenData
    session_variables: HasuraHeaders


class VerifyTokenOutput(BaseModel):
    valid: bool
    too_old: bool
    group_id: Optional[int]
    group_name: Optional[str]
    user_id: Optional[int]
    user_firstname: Optional[str]
    user_lastname: Optional[str]


async def verify_token(gql_client, input: VerifyTokenInput):
    return VerifyTokenOutput(
        valid=False,
        too_old=False,
    )


class SignupTokenData(BaseModel):
    token: str
    email: str
    password: str


class SignupTokenInput(BaseModel):
    input: VerifyTokenData
    session_variables: HasuraHeaders


class SignupTokenOutput(BaseModel):
    valid: bool
    too_old: bool
    errorKnownEmail: bool
    errorWeakPassword: bool
    token: Optional[str]
    user_id: Optional[int]
    user_group: Optional[int]


async def signup_token(gql_client, input: SignupTokenInput):
    return SignupTokenOutput()
