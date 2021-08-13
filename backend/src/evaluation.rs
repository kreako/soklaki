use chrono::NaiveDate;
use rocket::http::Status;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};

use super::competency;
use super::db;
use super::done::Done;
use super::evaluation_status::EvaluationStatus;
use super::jwt;
use super::observation;
use super::period;
use super::student;
use super::user;

#[derive(Debug, Serialize)]
pub struct RawEvaluation {
    pub user_id: i64,
    pub status: EvaluationStatus,
    pub comment: Option<String>,
    pub date: NaiveDate,
}

pub fn raw_evaluation(
    client: &mut postgres::Client,
    competency_id: &i32,
    student_id: &i64,
) -> Result<Option<RawEvaluation>, postgres::error::Error> {
    debug!("raw evaluation 1");

    match client.query_opt(
        "
SELECT user_id, status, comment, date
    FROM eval_evaluation
    WHERE student_id = $1 AND competency_id = $2
    ORDER BY date DESC, updated_at DESC
    LIMIT 1
",
        &[student_id, competency_id],
    )? {
        Some(row) => {
            let user_id = row.get(0);
            let status = row.get(1);
            let comment = row.get(2);
            let date = row.get(3);
            Ok(Some(RawEvaluation {
                user_id: user_id,
                status: status,
                comment: comment,
                date: date,
            }))
        }
        None => Ok(None),
    }
}

#[derive(Debug, Serialize)]
pub struct Evaluation {
    pub user: user::User,
    pub status: EvaluationStatus,
    pub comment: Option<String>,
    pub date: NaiveDate,
    pub from_current_period: bool,
}

pub fn evaluation(
    client: &mut postgres::Client,
    competency_id: &i32,
    student_id: &i64,
    group_id: &i64,
) -> Result<Option<Evaluation>, postgres::error::Error> {
    match raw_evaluation(client, competency_id, student_id)? {
        Some(raw) => {
            let user = user::user(client, &raw.user_id)?;
            let period = period::current_period(client, group_id)?;
            let from_current_period = period.start <= raw.date && raw.date <= period.end;
            Ok(Some(Evaluation {
                user: user,
                status: raw.status,
                comment: raw.comment,
                date: raw.date,
                from_current_period: from_current_period,
            }))
        }
        None => Ok(None),
    }
}

#[derive(Debug, Serialize)]
pub struct Single {
    pub student: student::Student,
    pub competency: competency::SingleCompetency,
    pub observations: Vec<observation::SingleObservation>,
    pub evaluation: Option<Evaluation>,
}

#[get("/single/<student_id>/<competency_id>")]
pub async fn evaluation_single(
    db: db::Db,
    token: jwt::JwtToken,
    student_id: i64,
    competency_id: i32,
) -> Result<Json<Single>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    let competency = db
        .run(move |client| competency::single_competency(client, &competency_id))
        .await
        .map_err(|_err| Status::InternalServerError)?;
    if group_id != competency.group_id {
        return Err(Status::NotFound);
    }
    let student = db
        .run(move |client| student::student(client, &student_id))
        .await
        .map_err(|_err| Status::InternalServerError)?;
    if group_id != student.group_id {
        return Err(Status::NotFound);
    }
    let observations = db
        .run(move |client| {
            observation::single_competency_observations(client, &competency_id, &student_id)
        })
        .await
        .map_err(|_err| Status::InternalServerError)?;
    let evaluation = db
        .run(move |client| evaluation(client, &competency_id, &student_id, &group_id))
        .await
        .map_err(|_err| Status::InternalServerError)?;
    Ok(Json(Single {
        student: student,
        competency: competency,
        observations: observations,
        evaluation: evaluation,
    }))
}

#[derive(Debug, Deserialize)]
pub struct NewEvaluation {
    pub student_id: i64,
    pub competency_id: i32,
    pub status: EvaluationStatus,
    pub comment: Option<String>,
    pub date: NaiveDate,
}

#[post("/new", data = "<new>")]
pub async fn new_evaluation(
    db: db::Db,
    token: jwt::JwtToken,
    new: Json<NewEvaluation>,
) -> Result<Json<Done>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    let user_id = token.claim.user_id.parse::<i64>().unwrap();

    // competency permission
    let competency_id = new.competency_id.clone();
    if !db
        .run(move |client| competency::permission(client, &competency_id, &group_id))
        .await
        .map_err(|_err| Status::InternalServerError)?
    {
        return Err(Status::InternalServerError);
    }
    // student permission
    let student_id = new.student_id.clone();
    if !db
        .run(move |client| student::permission(client, &student_id, &group_id))
        .await
        .map_err(|_err| Status::InternalServerError)?
    {
        return Err(Status::InternalServerError);
    }
    db.run(move |client| {
        client.execute(
            "
INSERT INTO eval_evaluation
    (user_id, student_id, competency_id, status, comment, date)
    VALUES
    ($1, $2, $3, $4, $5, $6)
       ",
            &[
                &user_id,
                &new.student_id,
                &new.competency_id,
                &new.status,
                &new.comment,
                &new.date,
            ],
        )
    })
    .await
    .map_err(|_err| Status::InternalServerError)?;
    Ok(Json(Done::done()))
}
