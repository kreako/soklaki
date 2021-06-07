import httpx


class GqlClientException(Exception):
    pass


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

    async def find_user_by_email(self, email):
        r = await self.run_query(
            """ query UserByEmail($email: String!) {
                   user(where: {email: {_eq: $email}}, limit: 1) {
                       id
                       hash
                       group_id
                   }
               }""",
            {"email": email},
        )
        return r["data"]["user"][0]

    async def insert_user_one(self, group_id, email, hash):
        r = await self.run_query(
            """ mutation InsertUserOne($email: String!, $hash: String!, $group_id: bigint!) {
                    insert_user_one(object: {active: true,
                                             email: $email,
                                             email_confirmed: false,
                                             group_id: $group_id,
                                             hash: $hash,
                                             manager: true}) {
                        id
                    }
                }""",
            {"group_id": group_id, "email": email, "hash": hash},
        )
        if "errors" in r:
            raise GqlClientException(str(r["errors"]))
        return r["data"]["insert_user_one"]["id"]

    async def insert_group_one(self, is_school):
        r = await self.run_query(
            """ mutation InsertGroupOne($is_school: Boolean!) {
                    insert_group_one(object: {is_school: $is_school, payment_ok: false}) {
                        id
                }
            }""",
            {"is_school": is_school},
        )
        return r["data"]["insert_group_one"]["id"]

    async def group_by_id(self, group_id):
        r = await self.run_query(
            """ query group($group_id: bigint!) {
                group(where: {id: {_eq: $group_id}}) {
                    id
                }
        }""",
            {"group_id": group_id},
        )
        return r["data"]["group"]

    async def delete_group(self, group_id):
        r = await self.run_query(
            """ mutation DeleteGroup($group_id: bigint!) {
                    delete_group(where: {id: {_eq: $group_id}}) {
                        affected_rows
                    }
            }""",
            {"group_id": group_id},
        )

    async def update_password(self, id, password):
        return await self.run_query(
            """mutation UpdatePassword($id: Int!, $password: String!) {
                   update_users_by_pk(pk_columns: {id: $id}, _set: {password: $password}) {
                       password
                   }
               }""",
            {"id": id, "password": password},
        )

    async def socle_counts(self, group_id):
        r = await self.run_query(
            """ query socle_counts($group_id: bigint!) {
                    socle_subject_aggregate(where: {group_id: {_eq: $group_id}}) {
                        aggregate {
                            count
                        }
                    }
                    socle_container_aggregate(where: {group_id: {_eq: $group_id}}) {
                        aggregate {
                            count
                        }
                    }
                    socle_competency_aggregate(where: {group_id: {_eq: $group_id}}) {
                        aggregate {
                            count
                        }
                    }
                }""",
            {"group_id": group_id},
        )
        return r["data"]

    async def default_socle(self):
        r = await self.run_query(
            """ query default_socle {
                    subjects: default_socle_subject {
                        id
                        title
                    }
                    containers_l1: default_socle_container(where: {container_id: {_is_null: true}}) {
                        alpha_full_rank
                        container_id
                        cycle
                        full_rank
                        id
                        rank
                        text
                    }
                    containers_l2: default_socle_container(where: {container_id: {_is_null: false}}) {
                        alpha_full_rank
                        container_id
                        cycle
                        full_rank
                        id
                        rank
                        text
                    }
                    competencies: default_socle_competency {
                        alpha_full_rank
                        container_id
                        cycle
                        full_rank
                        id
                        rank
                        text
                    }
                    competencies_subjects: default_socle_competency_subject {
                        competency_id
                        id
                        subject_id
                    }
                    templates: default_socle_competency_template {
                        competency_id
                        id
                        text
                    }
                }""",
            {},
        )
        return r["data"]

    async def insert_subjects(self, subjects):
        r = await self.run_query(
            """ mutation InsertSubjects($objects: [socle_subject_insert_input!]!) {
                    insert_socle_subject(objects: $objects) {
                        returning {
                            id
                        }
                    }
                }""",
            {"objects": subjects},
        )
        return r["data"]["insert_socle_subject"]["returning"]

    async def insert_containers(self, containers):
        r = await self.run_query(
            """ mutation InsertContainers($objects: [socle_container_insert_input!]!) {
                    insert_socle_container(objects: $objects) {
                        returning {
                            id
                        }
                    }
            }""",
            {
                "objects": containers,
            },
        )
        return r["data"]["insert_socle_container"]["returning"]

    async def insert_competencies(self, competencies):
        r = await self.run_query(
            """ mutation InsertCompetencies($objects: [socle_competency_insert_input!]!) {
                    insert_socle_competency(objects: $objects) {
                        returning {
                            id
                        }
                    }
            }""",
            {
                "objects": competencies,
            },
        )
        return r["data"]["insert_socle_competency"]["returning"]

    async def insert_competencies_subjects(self, competencies_subjects):
        r = await self.run_query(
            """ mutation InsertCompetenciesSubjects($objects: [socle_competency_subject_insert_input!]!) {
                    insert_socle_competency_subject(objects: $objects) {
                        returning {
                            id
                        }
                    }
                }""",
            {
                "objects": competencies_subjects,
            },
        )
        return r["data"]["insert_socle_competency_subject"]["returning"]

    async def insert_competencies_templates(self, competencies_templates):
        r = await self.run_query(
            """ mutation InsertCompetenciesTemplates($objects: [socle_competency_template_insert_input!]!) {
                    insert_socle_competency_template(objects: $objects) {
                        returning {
                            id
                        }
                    }
                }""",
            {
                "objects": competencies_templates,
            },
        )
        return r["data"]["insert_socle_competency_template"]["returning"]

    async def group_by_id(self, group_id):
        r = await self.run_query(
            """ query GroupById($id: bigint!) {
                    group_by_pk(id: $id) {
                        id
                        name
                    }
                }""",
            {"id": group_id},
        )
        return r["data"]["group_by_pk"]

    async def user_by_id(self, user_id):
        r = await self.run_query(
            """ query UserById($id: bigint!) {
                    user_by_pk(id: $id) {
                        firstname
                        lastname
                        group_id
                    }
                }""",
            {"id": user_id},
        )
        return r["data"]["user_by_pk"]

    async def user_by_email(self, email):
        r = await self.run_query(
            """ query UserByEmail($email: String!) {
                    user(where: {email: {_eq: $email}}) {
                        id
                    }
                }""",
            {"email": email},
        )
        return r["data"]["user"]

    async def update_user(self, user_id, active, email):
        r = await self.run_query(
            """ mutation UserUpdate($id: bigint!, $email: String!, $active: Boolean!) {
                    update_user_by_pk(pk_columns: {id: $id}, _set: {email: $email, active: $active}) {
                        id
                    }
                }""",
            {"id": user_id, "active": active, "email": email},
        )
        return r["data"]["update_user_by_pk"]

    async def student_by_id(self, student_id):
        r = await self.run_query(
            """ query StudentById($id: bigint!) {
                    student_by_pk(id: $id) {
                        active
                        birthdate
                        firstname
                        group_id
                        id
                        lastname
                        school_entry
                        school_exit
                    }
                }""",
            {"id": student_id},
        )
        return r["data"]["student_by_pk"]

    async def period_by_id(self, group_id):
        r = await self.run_query(
            """ query PeriodById($id: Int!) {
                    eval_period_by_pk(id: $id) {
                        id
                        name
                    }
                }""",
            {"id": group_id},
        )
        return r["data"]["eval_period_by_pk"]
