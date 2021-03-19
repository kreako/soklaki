import httpx

class GqlClient(object):
    def __init__(self, end_point, admin_secret):
        self.end_point = end_point
        self.headers = {"X-Hasura-Admin-Secret": admin_secret}

    async def run_query(self, query, variables):
        async with httpx.AsyncClient() as client:
            r = await client.post(
                self.end_point,
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

    async def insert_user_one(self, group_id, email, hash):
        await self.run_query(
            """ mutation InsertUserOne($email: String!, $hash: String!, $group_id: bigint!) {
                    insert_user_one(object: {active: true,
                                             email: $email,
                                             email_confirmed: false,
                                             group_id: $group_id,
                                             hash: $hash,
                                             manager: true,
                                             name: ""}) {
                        id
                    }
                }""",
            {"group_id": group_id, "email": email, "hash": hash},
        )

    async def insert_group_one(self, name, is_school):
        await self.run_query(
            """ mutation InsertGroupOne($name: String! $is_school: Boolean!) {
                    insert_group_one(object: {name: $name, is_school: $is_school}) {
                        id
                }
            }""",
            {"name": name, "is_school": is_school},
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