use chrono;
use chrono::NaiveDate;
use eyre::WrapErr;
use rocket::http::Status;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use tracing::debug;

use super::competency;
use super::cycle;
use super::db;
use super::jwt;
use super::period;
use super::stats::EvaluationStatus;

#[derive(Debug, Serialize)]
pub struct Student {
    pub id: i64,
    pub firstname: String,
    pub lastname: String,
    pub birthdate: NaiveDate,
    pub school_entry: NaiveDate,
    pub school_exit: Option<NaiveDate>,
    pub group_id: i64,
    pub active: bool,
}

#[derive(Debug, Serialize)]
pub struct EvalSingle {
    pub observations: i32,
    pub evaluation: EvaluationStatus,
}

impl EvalSingle {
    fn new() -> Self {
        EvalSingle {
            observations: 0,
            evaluation: EvaluationStatus::Empty,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct StudentEvalInfo {
    pub competency: competency::Competency,
    pub eval: EvalSingle,
}

impl StudentEvalInfo {
    fn new(competency: competency::Competency) -> Self {
        StudentEvalInfo {
            competency: competency,
            eval: EvalSingle::new(),
        }
    }
}

#[derive(Debug, Serialize)]
pub struct Summary {
    pub progress: i32,
    pub comment: bool,
    pub observations: i32,
    pub evaluations: i32,
}

#[derive(Debug, Serialize)]
pub struct StudentInfo {
    pub student: Student,
    pub cycle: &'static str,
    pub eval: Vec<StudentEvalInfo>,
    pub summary: Summary,
}

pub fn student(
    client: &mut postgres::Client,
    student_id: &i64,
) -> Result<Student, postgres::error::Error> {
    let row = client.query_one(
        "
SELECT id, firstname, lastname, birthdate, school_entry, school_exit, group_id, active
	FROM student
    WHERE id = $1
",
        &[student_id],
    )?;
    Ok(Student {
        id: row.get(0),
        firstname: row.get(1),
        lastname: row.get(2),
        birthdate: row.get(3),
        school_entry: row.get(4),
        school_exit: row.get(5),
        group_id: row.get(6),
        active: row.get(7),
    })
}

fn eval_evaluation_stat(
    client: &mut postgres::Client,
    date: &NaiveDate,
    cycle: &cycle::Cycle,
    student_id: &i64,
    competencies_index: &HashMap<i32, usize>,
    eval: &mut Vec<StudentEvalInfo>,
) -> Result<(), postgres::error::Error> {
    for row in client.query(
        "
SELECT
	eval_evaluation.competency_id,
	eval_evaluation.status
FROM eval_evaluation
	JOIN socle_competency
		ON socle_competency.id = eval_evaluation.competency_id
	WHERE eval_evaluation.active = true
		AND socle_competency.active = true
		AND eval_evaluation.student_id = $1
		AND eval_evaluation.date <= $2
		AND socle_competency.cycle::text = $3
	ORDER BY eval_evaluation.date DESC, eval_evaluation.updated_at DESC
	",
        &[student_id, date, &cycle.to_str()],
    )? {
        let competency_id = row.get(0);
        let status = row.get(1);

        if let Some(competency_index) = competencies_index.get(&competency_id) {
            if eval[*competency_index].eval.evaluation == EvaluationStatus::Empty {
                eval[*competency_index].eval.evaluation = status;
            }
        }
    }
    Ok(())
}

fn eval_observation_stat(
    client: &mut postgres::Client,
    date: &NaiveDate,
    cycle: &cycle::Cycle,
    student_id: &i64,
    competencies_index: &HashMap<i32, usize>,
    eval: &mut Vec<StudentEvalInfo>,
) -> Result<(), postgres::error::Error> {
    debug!("eval_observation_stats_by_cycle 1");
    for row in client.query(
        "
SELECT
	eval_observation_competency.competency_id
FROM eval_observation 
	JOIN eval_observation_competency
		ON eval_observation_competency.observation_id = eval_observation.id 
	JOIN eval_observation_student
		ON eval_observation_student.observation_id = eval_observation.id 
	JOIN socle_competency
		ON socle_competency.id = eval_observation_competency.competency_id 
WHERE socle_competency.active = true
    AND socle_competency.cycle::text = $3
	AND eval_observation.active = true
	AND eval_observation.date <= $2
	AND eval_observation_student.student_id = $1
		",
        &[student_id, date, &cycle.to_str()],
    )? {
        // debug!(?row, "eval_observation_stats_by_cycle 2");
        let competency_id = row.get(0);
        if let Some(competency_index) = competencies_index.get(&competency_id) {
            eval[*competency_index].eval.observations += 1;
            //debug!("eval_observation_stats_by_cycle 3");
        }
    }

    debug!("eval_observation_stats_by_cycle 4");
    Ok(())
}

fn student_eval(
    client: &mut postgres::Client,
    student_id: &i64,
    group_id: &i64,
    cycle: &cycle::Cycle,
    date: &NaiveDate,
) -> Result<Vec<StudentEvalInfo>, postgres::error::Error> {
    let competencies = competency::competencies_from_cycle(client, group_id, cycle)?;
    // competency id -> index cache for easier update
    let mut competencies_index = HashMap::new();
    for (idx, competency) in (&competencies).iter().enumerate() {
        competencies_index.insert(competency.id, idx);
    }
    let mut eval = competencies
        .into_iter()
        .map(|c| StudentEvalInfo::new(c))
        .collect();
    eval_evaluation_stat(
        client,
        date,
        cycle,
        student_id,
        &competencies_index,
        &mut eval,
    )?;
    eval_observation_stat(
        client,
        date,
        cycle,
        student_id,
        &competencies_index,
        &mut eval,
    )?;
    Ok(eval)
}

fn is_there_a_comment(
    client: &mut postgres::Client,
    group_id: &i64,
    student_id: &i64,
    cycle: &cycle::Cycle,
    date: &NaiveDate,
) -> Result<bool, postgres::error::Error> {
    let period = period::search_period_or_insert(client, group_id, date)?;
    let row = client.query_one(
        "
SELECT comments_count::int
	FROM eval_comment_stats
    WHERE student_id = $1
        AND period_id = $2
        AND cycle::text = $3
",
        &[student_id, &period.id, &cycle.to_str()],
    )?;
    let comments_count: i32 = row.get(0);
    Ok(comments_count > 1)
}

#[get("/<id>")]
pub async fn student_by_id(
    db: db::Db,
    token: jwt::JwtToken,
    id: i64,
) -> Result<Json<StudentInfo>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    let student = db
        .run(move |client| student(client, &id))
        .await
        .wrap_err("student_by_id error")
        .map_err(|_err| Status::InternalServerError)?;
    if student.group_id != group_id {
        return Err(Status::NotFound);
    }
    let today = chrono::Local::today().naive_local();
    let cycle = cycle::estimate_cycle(&today, &student.birthdate);
    let cloned_cycle = cycle.clone();
    let cloned_today = today.clone();
    let eval = db
        .run(move |client| student_eval(client, &id, &group_id, &cloned_cycle, &cloned_today))
        .await
        .wrap_err("student_eval error")
        .map_err(|_err| Status::InternalServerError)?;
    let cloned_cycle2 = cycle.clone();
    let cloned_today2 = today.clone();
    let comment = db
        .run(move |client| {
            is_there_a_comment(client, &group_id, &id, &cloned_cycle2, &cloned_today2)
        })
        .await
        .wrap_err("is_there_a_comment")
        .map_err(|_err| Status::InternalServerError)?;
    let competency_count = eval.len() as i32;
    let observations = eval.iter().fold(0, |acc, e| {
        if e.eval.observations > 0 {
            acc + 1
        } else {
            acc
        }
    });
    let evaluations = eval.iter().fold(0, |acc, e| {
        if e.eval.evaluation != EvaluationStatus::Empty {
            acc + 1
        } else {
            acc
        }
    });
    let progress = 100.0 as f64
        * (if comment { 1.0 / 3.0 as f64 } else { 0 as f64 }
            + ((evaluations as f64) / (3.0 * competency_count as f64))
            + ((observations as f64) / (3.0 * competency_count as f64)));
    let summary = Summary {
        comment: comment,
        progress: progress as i32,
        evaluations: (100.0 * (evaluations as f64) / (competency_count as f64)) as i32,
        observations: (100.0 * (observations as f64) / (competency_count as f64)) as i32,
    };
    let info = StudentInfo {
        student: student,
        cycle: cycle.to_str(),
        eval: eval,
        summary: summary,
    };
    Ok(Json(info))
}

#[derive(Debug, Serialize)]
pub struct Done {
    pub done: bool,
}

impl Done {
    fn done() -> Self {
        Done { done: true }
    }
}

#[derive(Debug, Deserialize)]
pub struct StudentLastname {
    pub id: i64,
    pub lastname: String,
}

#[post("/lastname", data = "<student>")]
pub async fn lastname(
    db: db::Db,
    token: jwt::JwtToken,
    student: Json<StudentLastname>,
) -> Result<Json<Done>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();

    db.run(move |client| {
        client.execute(
            "UPDATE student SET lastname = $1 WHERE id = $2 AND group_id = $3",
            &[&student.lastname, &student.id, &group_id],
        )
    })
    .await
    .map_err(|_err| Status::InternalServerError)?;
    Ok(Json(Done::done()))
}

#[derive(Debug, Deserialize)]
pub struct StudentFirstname {
    pub id: i64,
    pub firstname: String,
}

#[post("/firstname", data = "<student>")]
pub async fn firstname(
    db: db::Db,
    token: jwt::JwtToken,
    student: Json<StudentFirstname>,
) -> Result<Json<Done>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();

    db.run(move |client| {
        client.execute(
            "UPDATE student SET firstname = $1 WHERE id = $2 AND group_id = $3",
            &[&student.firstname, &student.id, &group_id],
        )
    })
    .await
    .map_err(|_err| Status::InternalServerError)?;
    Ok(Json(Done::done()))
}

#[derive(Debug, Deserialize)]
pub struct StudentBirthdate {
    pub id: i64,
    pub birthdate: NaiveDate,
}

#[post("/birthdate", data = "<student>")]
pub async fn birthdate(
    db: db::Db,
    token: jwt::JwtToken,
    student: Json<StudentBirthdate>,
) -> Result<Json<Done>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();

    db.run(move |client| {
        client.execute(
            "UPDATE student SET birthdate = $1 WHERE id = $2 AND group_id = $3",
            &[&student.birthdate, &student.id, &group_id],
        )
    })
    .await
    .map_err(|_err| Status::InternalServerError)?;
    Ok(Json(Done::done()))
}

#[derive(Debug, Deserialize)]
pub struct StudentSchoolEntry {
    pub id: i64,
    pub school_entry: NaiveDate,
}

#[post("/school_entry", data = "<student>")]
pub async fn school_entry(
    db: db::Db,
    token: jwt::JwtToken,
    student: Json<StudentSchoolEntry>,
) -> Result<Json<Done>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();

    db.run(move |client| {
        client.execute(
            "UPDATE student SET school_entry = $1 WHERE id = $2 AND group_id = $3",
            &[&student.school_entry, &student.id, &group_id],
        )
    })
    .await
    .map_err(|_err| Status::InternalServerError)?;
    Ok(Json(Done::done()))
}

#[derive(Debug, Deserialize)]
pub struct StudentSchoolExit {
    pub id: i64,
    pub school_exit: Option<NaiveDate>,
}

#[post("/school_exit", data = "<student>")]
pub async fn school_exit(
    db: db::Db,
    token: jwt::JwtToken,
    student: Json<StudentSchoolExit>,
) -> Result<Json<Done>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();

    db.run(move |client| {
        client.execute(
            "UPDATE student SET school_exit = $1 WHERE id = $2 AND group_id = $3",
            &[&student.school_exit, &student.id, &group_id],
        )
    })
    .await
    .map_err(|_err| Status::InternalServerError)?;
    Ok(Json(Done::done()))
}
