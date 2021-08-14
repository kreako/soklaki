use chrono::NaiveDate;
use rocket::http::Status;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};

use super::competency;
use super::db;
use super::jwt;
use super::student;
use super::user;

#[derive(Debug, Serialize)]
pub struct SingleObservation {
    pub id: i64,
    pub text: String,
    pub date: NaiveDate,
    pub user: user::User,
}

pub fn single_competency_observations(
    client: &mut postgres::Client,
    competency_id: &i32,
    student_id: &i64,
) -> Result<Vec<SingleObservation>, postgres::error::Error> {
    Ok(client
        .query(
            "
SELECT eval_observation.id, eval_observation.text, eval_observation.date, eval_observation.user_id
FROM eval_observation
    JOIN eval_observation_student
        ON eval_observation_student.observation_id = eval_observation.id
    JOIN eval_observation_competency
        ON eval_observation_competency.observation_id = eval_observation.id
    WHERE eval_observation_student.student_id = $1
        AND eval_observation_competency.competency_id = $2
    ORDER BY eval_observation.date DESC
",
            &[student_id, competency_id],
        )?
        .iter()
        .map(|row| {
            Ok(SingleObservation {
                id: row.get(0),
                text: row.get(1),
                date: row.get(2),
                user: user::user(client, &row.get(3))?,
            })
        })
        .collect())?
}

#[derive(Debug, Serialize)]
pub struct Prefill {
    pub student: student::Student,
    pub competency: competency::SingleCompetency,
}

#[get("/prefill/<student_id>/<competency_id>")]
pub async fn prefill(
    db: db::Db,
    token: jwt::JwtToken,
    student_id: i64,
    competency_id: i32,
) -> Result<Json<Prefill>, Status> {
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
    Ok(Json(Prefill {
        student: student,
        competency: competency,
    }))
}

#[derive(Debug, Deserialize)]
pub struct NewPrefill {
    pub student_id: i64,
    pub competency_id: i32,
    pub text: String,
}

#[post("/new-prefill", data = "<new>")]
pub async fn new_prefill(
    db: db::Db,
    token: jwt::JwtToken,
    new: Json<NewPrefill>,
) -> Result<Json<ObservationId>, Status> {
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
    Ok(Json(
        db.run(move |client| {
            _new_prefill(
                client,
                &user_id,
                &new.competency_id,
                &new.student_id,
                &new.text,
            )
        })
        .await
        .map_err(|_err| Status::InternalServerError)?,
    ))
}

#[derive(Debug, Deserialize, Serialize)]
pub struct ObservationId {
    pub id: i64,
}

pub fn _new_prefill(
    client: &mut postgres::Client,
    user_id: &i64,
    competency_id: &i32,
    student_id: &i64,
    text: &str,
) -> Result<ObservationId, postgres::error::Error> {
    let today = chrono::Local::today().naive_local();
    let row = client.query_one(
        "
INSERT INTO eval_observation
    (text, user_id, date)
    VALUES
    ($1, $2, $3)
    RETURNING id
    ",
        &[&text, user_id, &today],
    )?;
    let id = row.get(0);

    client.execute(
        "
INSERT INTO eval_observation_competency
    (observation_id, competency_id)
    VALUES
    ($1, $2)
    ",
        &[&id, competency_id],
    )?;

    client.execute(
        "
INSERT INTO eval_observation_student
    (observation_id, student_id)
    VALUES
    ($1, $2)
    ",
        &[&id, student_id],
    )?;

    Ok(ObservationId { id: id })
}
