import jwt


def generate_jwt_token(jwt_secret, user_id, group_id) -> str:
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
    token = jwt.encode(payload, jwt_secret, "HS256")
    return token
