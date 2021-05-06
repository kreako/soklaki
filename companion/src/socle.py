from pydantic import BaseModel, Field

from gql_client import GqlClientException


class HasuraHeaders(BaseModel):
    x_hasura_user_id: int = Field(alias="x-hasura-user-id")
    x_hasura_user_group: int = Field(alias="x-hasura-user-group")


class LoadSocleData(BaseModel):
    group_id: int


class LoadSocleInput(BaseModel):
    input: LoadSocleData
    session_variables: HasuraHeaders


class LoadSocleOutput(BaseModel):
    errorUnknownGroupId: bool
    errorNonEmptySocle: bool
    errorUnknown: bool


async def load(gql_client, input: LoadSocleInput):
    if input.input.group_id != input.session_variables.x_hasura_user_group:
        return LoadSocleOutput(
            errorUnknownGroupId=True,
            errorNonEmptySocle=False,
            errorUnknown=False,
        )
    group_id = input.input.group_id
    if not await gql_client.group_by_id(group_id):
        # Empty list so no group - should not happen...
        return LoadSocleOutput(
            errorUnknownGroupId=True,
            errorNonEmptySocle=False,
            errorUnknown=False,
        )
    counts = await gql_client.socle_counts(group_id)
    if (
        counts["socle_subject_aggregate"]["aggregate"]["count"] > 0
        or counts["socle_container_aggregate"]["aggregate"]["count"] > 0
        or counts["socle_competency_aggregate"]["aggregate"]["count"] > 0
    ):
        return LoadSocleOutput(
            errorUnknownGroupId=False,
            errorNonEmptySocle=True,
            errorUnknown=False,
        )
    default_socle = await gql_client.default_socle()
    # mapping old id -> new id
    subjects = {}
    containers = {}
    competencies = {}
    competencies_subjects = {}

    new_subjects = []
    old_subjects_id = []
    for subject in default_socle["subjects"]:
        old_subjects_id.append(subject["id"])
        new_subjects.append(
            {"active": True, "title": subject["title"], "group_id": group_id}
        )
    new_ids = await gql_client.insert_subjects(new_subjects)
    for (new_id, old_id) in zip(new_ids, old_subjects_id):
        subjects[old_id] = new_id["id"]

    new_containers = []
    old_containers_id = []
    for l1 in default_socle["containers_l1"]:
        old_containers_id.append(l1["id"])
        new_containers.append(
            {
                "group_id": group_id,
                "text": l1["text"],
                "alpha_full_rank": l1["alpha_full_rank"],
                "full_rank": l1["full_rank"],
                "rank": l1["rank"],
                "container_id": None,
                "cycle": l1["cycle"],
            }
        )
    new_ids = await gql_client.insert_containers(new_containers)
    for (new_id, old_id) in zip(new_ids, old_containers_id):
        containers[old_id] = new_id["id"]

    new_containers = []
    old_containers_id = []
    for l2 in default_socle["containers_l2"]:
        old_containers_id.append(l2["id"])
        new_containers.append(
            {
                "group_id": group_id,
                "text": l2["text"],
                "alpha_full_rank": l2["alpha_full_rank"],
                "full_rank": l2["full_rank"],
                "rank": l2["rank"],
                "container_id": containers[l2["container_id"]],  # map old id to new
                "cycle": l1["cycle"],
            }
        )
    new_ids = await gql_client.insert_containers(new_containers)
    for (new_id, old_id) in zip(new_ids, old_containers_id):
        containers[old_id] = new_id["id"]

    new_competencies = []
    old_competencies_id = []
    for competency in default_socle["competencies"]:
        old_competencies_id.append(competency["id"])
        new_competencies.append(
            {
                "group_id": group_id,
                "text": competency["text"],
                "alpha_full_rank": competency["alpha_full_rank"],
                "full_rank": competency["full_rank"],
                "rank": competency["rank"],
                "container_id": containers[
                    competency["container_id"]
                ],  # map old id to new
                "cycle": competency["cycle"],
            }
        )
    new_ids = await gql_client.insert_competencies(new_competencies)
    for (new_id, old_id) in zip(new_ids, old_competencies_id):
        competencies[old_id] = new_id["id"]

    news = []
    for cs in default_socle["competencies_subjects"]:
        news.append(
            {
                "competency_id": competencies[cs["competency_id"]],
                "subject_id": subjects[cs["subject_id"]],
            }
        )
    new_ids = await gql_client.insert_competencies_subjects(news)

    news = []
    for cs in default_socle["templates"]:
        news.append(
            {
                "competency_id": competencies[cs["competency_id"]],
                "active": True,
                "text": cs["text"],
                "group_id": group_id,
            }
        )
    new_ids = await gql_client.insert_competencies_templates(news)

    return LoadSocleOutput(
        errorUnknownGroupId=False,
        errorNonEmptySocle=False,
        errorUnknown=False,
    )