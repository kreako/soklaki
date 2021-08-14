use chrono::NaiveDate;
use eyre::{eyre, WrapErr};
use rocket::http::Status;
use rocket::serde::json::Json;
use rocket_sync_db_pools::postgres;
use serde::Serialize;
use std::collections::HashMap;
use std::vec::Vec;
use tracing::debug;

use super::competency;
use super::cycle::Cycle;
use super::db;
use super::evaluation_status::EvaluationStatus;
use super::jwt;
use super::students;

#[derive(Debug, Serialize)]
pub struct EvalSingle {
    pub student_id: i64,
    pub observations: i32,
    pub evaluation: EvaluationStatus,
}

impl EvalSingle {
    fn new(student_id: i64) -> Self {
        EvalSingle {
            student_id: student_id,
            observations: 0,
            evaluation: EvaluationStatus::Empty,
        }
    }
}

fn eval_evaluation_stats_by_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
    cycle: &Cycle,
    students_index: &HashMap<i64, usize>,
    competencies_index: &HashMap<i32, usize>,
    e: &mut EvalStatsByCycle,
) -> Result<(), postgres::error::Error> {
    for row in client.query(
        "
SELECT
	eval_evaluation.competency_id,
	eval_evaluation.student_id,
	eval_evaluation.status
FROM eval_evaluation
	JOIN socle_competency
		ON socle_competency.id = eval_evaluation.competency_id
	JOIN student
		ON student.id = eval_evaluation.student_id
	WHERE eval_evaluation.active = true
		AND socle_competency.active = true
		AND socle_competency.group_id = $1
		AND student.group_id = $1
		AND eval_evaluation.date <= $2
		AND student.school_entry <= $2
		AND (
			(student.school_exit is null)
			OR
			(student.school_exit >= $2)
		)
		AND socle_competency.cycle::text = $3
	ORDER BY eval_evaluation.date DESC, eval_evaluation.updated_at DESC
	",
        &[group_id, date, &cycle.to_str()],
    )? {
        let competency_id = row.get(0);
        let student_id = row.get(1);
        let status = row.get(2);
        if let Some(student_index) = students_index.get(&student_id) {
            if let Some(competency_index) = competencies_index.get(&competency_id) {
                if e.stats[*competency_index].by_students[*student_index].evaluation
                    == EvaluationStatus::Empty
                {
                    e.stats[*competency_index].by_students[*student_index].evaluation = status;
                }
            }
        }
    }
    Ok(())
}

fn eval_observation_stats_by_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
    cycle: &Cycle,
    students_index: &HashMap<i64, usize>,
    competencies_index: &HashMap<i32, usize>,
    e: &mut EvalStatsByCycle,
) -> Result<(), postgres::error::Error> {
    debug!("eval_observation_stats_by_cycle 1");
    for row in client.query(
        "
SELECT
	eval_observation_competency.competency_id,
	eval_observation_student.student_id
FROM eval_observation 
	JOIN eval_observation_competency
		ON eval_observation_competency.observation_id = eval_observation.id 
	JOIN eval_observation_student
		ON eval_observation_student.observation_id = eval_observation.id 
	JOIN socle_competency
		ON socle_competency.id = eval_observation_competency.competency_id 
	JOIN student
		ON eval_observation_student.student_id = student.id
WHERE socle_competency.active = true
	AND socle_competency.group_id = $1
    AND socle_competency.cycle::text = $3
	AND eval_observation.active = true
	AND student.school_entry <= $2
	AND (
		(student.school_exit is null)
		OR
		(student.school_exit >= $2)
	)
	AND eval_observation.date <= $2
	AND student.group_id = $1
		",
        &[group_id, date, &cycle.to_str()],
    )? {
        let competency_id = row.get(0);
        let student_id = row.get(1);
        // debug!(?row, "eval_observation_stats_by_cycle 2");
        if let Some(student_index) = students_index.get(&student_id) {
            if let Some(competency_index) = competencies_index.get(&competency_id) {
                e.stats[*competency_index].by_students[*student_index].observations += 1;
                // debug!("eval_observation_stats_by_cycle 3");
            }
        }
    }

    debug!("eval_observation_stats_by_cycle 4");
    Ok(())
}

#[derive(Debug, Serialize)]
pub struct EvalStatsByCycleByCompetency {
    pub competency: competency::Competency,
    pub by_students: Vec<EvalSingle>,
}

#[derive(Debug, Serialize)]
pub struct EvalStatsByCycle {
    pub students: Vec<students::Student>,
    pub stats: Vec<EvalStatsByCycleByCompetency>,
}

pub fn eval_stats_by_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
    cycle: &Cycle,
) -> Result<EvalStatsByCycle, postgres::error::Error> {
    let competencies = competency::competencies_from_cycle(client, group_id, cycle)?;
    let students = students::students_by_cycle(client, group_id, date, cycle)?;

    let mut e = EvalStatsByCycle {
        students: students,
        stats: vec![],
    };

    for competency in &competencies {
        let mut by_competency = EvalStatsByCycleByCompetency {
            competency: (*competency).clone(),
            by_students: vec![],
        };
        for student in &e.students {
            by_competency.by_students.push(EvalSingle::new(student.id));
        }
        e.stats.push(by_competency);
    }
    debug!("eval_stats_by_cycle 1");

    // id -> index
    let mut students_index = HashMap::new();
    for (idx, student) in (&e.students).iter().enumerate() {
        students_index.insert(student.id, idx);
    }
    // id -> index
    let mut competencies_index = HashMap::new();
    for (idx, competency) in (&competencies).iter().enumerate() {
        competencies_index.insert(competency.id, idx);
    }

    debug!("eval_stats_by_cycle 2");

    eval_evaluation_stats_by_cycle(
        client,
        group_id,
        date,
        cycle,
        &students_index,
        &competencies_index,
        &mut e,
    )?;
    debug!("eval_stats_by_cycle 3");

    eval_observation_stats_by_cycle(
        client,
        group_id,
        date,
        cycle,
        &students_index,
        &competencies_index,
        &mut e,
    )?;
    debug!("eval_stats_by_cycle 4");

    Ok(e)
}

#[get("/<cycle>")]
pub async fn stats_by_cycle(
    db: db::Db,
    token: jwt::JwtToken,
    cycle: &str,
) -> Result<Json<EvalStatsByCycle>, Status> {
    let cycle = Cycle::from_str(cycle)
        .ok_or(eyre!("Invalid cycle : {}", cycle))
        .map_err(|_err| Status::InternalServerError)?;
    debug!(?cycle, "stats_by_cycle 1");
    let today = chrono::Local::today().naive_local();
    debug!(?today, "stats_by_cycle 2");
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    debug!(?group_id, "stats_by_cycle 3");
    let e = db
        .run(move |client| eval_stats_by_cycle(client, &group_id, &today, &cycle))
        .await
        .wrap_err("eval_stats_by_cycle error")
        .map_err(|_err| Status::InternalServerError)?;
    debug!("stats_by_cycle 4");
    Ok(Json(e))
}
