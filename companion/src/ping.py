from pydantic import BaseModel, Field
from typing import Optional

from gql_client import GqlClientException


class PingData(BaseModel):
    secret: str


class PingInput(BaseModel):
    input: PingData


class PingOutput(BaseModel):
    default_socle_competency: int
    default_socle_competency_subject: int
    default_socle_competency_template: int
    default_socle_container: int
    default_socle_subject: int
    eval_comment: int
    eval_evaluation: int
    eval_observation: int
    eval_period: int
    group: int
    report: int
    socle_competency: int
    socle_competency_subject: int
    socle_competency_template: int
    socle_container: int
    socle_subject: int
    student: int
    user: int


async def ping(gql_client, ping_secret, input: PingInput):
    if input.input.secret != ping_secret:
        return None
    answer = await gql_client.run_query(
        """
query Ping {
  default_socle_competency_aggregate {
    aggregate {
      count
    }
  }
  default_socle_competency_subject_aggregate {
    aggregate {
      count
    }
  }
  default_socle_competency_template_aggregate {
    aggregate {
      count
    }
  }
  default_socle_container_aggregate {
    aggregate {
      count
    }
  }
  default_socle_subject_aggregate {
    aggregate {
      count
    }
  }
  eval_comment_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  eval_evaluation_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  eval_observation_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  eval_period_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  group_aggregate {
    aggregate {
      count
    }
  }
  report_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  socle_competency_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  socle_competency_subject_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  socle_competency_template_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  socle_container_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  socle_subject_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  student_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
  user_aggregate(where: {active: {_eq: true}}) {
    aggregate {
      count
    }
  }
}""",
        {},
    )

    data = answer["data"]

    return PingOutput(
        default_socle_competency=data["default_socle_competency_aggregate"][
            "aggregate"
        ]["count"],
        default_socle_competency_subject=data[
            "default_socle_competency_subject_aggregate"
        ]["aggregate"]["count"],
        default_socle_competency_template=data[
            "default_socle_competency_template_aggregate"
        ]["aggregate"]["count"],
        default_socle_container=data["default_socle_container_aggregate"]["aggregate"][
            "count"
        ],
        default_socle_subject=data["default_socle_subject_aggregate"]["aggregate"][
            "count"
        ],
        eval_comment=data["eval_comment_aggregate"]["aggregate"]["count"],
        eval_evaluation=data["eval_evaluation_aggregate"]["aggregate"]["count"],
        eval_observation=data["eval_observation_aggregate"]["aggregate"]["count"],
        eval_period=data["eval_period_aggregate"]["aggregate"]["count"],
        group=data["group_aggregate"]["aggregate"]["count"],
        report=data["report_aggregate"]["aggregate"]["count"],
        socle_competency=data["socle_competency_aggregate"]["aggregate"]["count"],
        socle_competency_subject=data["socle_competency_subject_aggregate"][
            "aggregate"
        ]["count"],
        socle_competency_template=data["socle_competency_template_aggregate"][
            "aggregate"
        ]["count"],
        socle_container=data["socle_container_aggregate"]["aggregate"]["count"],
        socle_subject=data["socle_subject_aggregate"]["aggregate"]["count"],
        student=data["student_aggregate"]["aggregate"]["count"],
        user=data["user_aggregate"]["aggregate"]["count"],
    )
