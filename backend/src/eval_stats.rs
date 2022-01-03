use eyre::{eyre, WrapErr};
use rocket::http::Status;
use rocket::serde::json::Json;
use serde::Serialize;
//use tracing::debug;

use super::competency;
use super::cycle::Cycle;
use super::db;
use super::jwt;
use super::period;
use super::students;

#[derive(Debug, Serialize)]
pub struct EvalStatsByCycleByCompetency {
  pub competency: competency::Competency,
  pub count: usize,
}

#[derive(Debug, Serialize)]
pub struct EvalStatsByCycle {
  pub competencies: Vec<EvalStatsByCycleByCompetency>,
  pub comment_count: usize,
  pub total: usize,
}

fn _eval_stats_by_cycle(
  client: &mut postgres::Client,
  group_id: &i64,
  cycle: &Cycle,
) -> Result<EvalStatsByCycle, postgres::error::Error> {
  let competencies = competency::competencies_from_cycle(client, group_id, cycle)?;
  let period = period::current_period(client, &group_id)?;
  let students = students::students_by_cycle_in_period(client, group_id, &period, cycle)?;
  //debug!("_eval_stats_by_cycle {:?}", students);

  let mut by_competency = Vec::new();

  for competency in &competencies {
    let count = client
      .query(
        "
SELECT student_id
FROM eval_evaluation
  WHERE competency_id = $1
    AND status != 'Empty'
    AND date >= $2 AND date <= $3
  GROUP BY student_id   
      ",
        &[&competency.id, &period.start, &period.end],
      )?
      .iter()
      .count();
    by_competency.push(EvalStatsByCycleByCompetency {
      competency: (*competency).clone(),
      count: count,
    })
  }

  let mut comment_count = 0;
  for student in &students {
    let count = client
      .query(
        "
SELECT student_id
FROM eval_comment
    WHERE student_id = $1
      AND date >= $2 AND date <= $3
      ",
        &[&student.id, &period.start, &period.end],
      )?
      .iter()
      .count();
    if count > 0 {
      comment_count += 1;
    }
  }

  let e = EvalStatsByCycle {
    competencies: by_competency,
    comment_count: comment_count,
    total: students.iter().count(),
  };
  Ok(e)
}

#[get("/by_cycle/<cycle>")]
pub async fn eval_stats_by_cycle(
  db: db::Db,
  token: jwt::JwtToken,
  cycle: &str,
) -> Result<Json<EvalStatsByCycle>, Status> {
  let cycle = Cycle::from_str(cycle)
    .ok_or(eyre!("Invalid cycle : {}", cycle))
    .map_err(|_err| Status::InternalServerError)?;
  let group_id = token.claim.user_group.parse::<i64>().unwrap();
  let e = db
    .run(move |client| _eval_stats_by_cycle(client, &group_id, &cycle))
    .await
    .wrap_err("eval_stats_by_cycle error")
    .map_err(|_err| Status::InternalServerError)?;
  Ok(Json(e))
}

#[derive(Debug, Serialize)]
pub struct EvalStatsSummaryByCycle {
  pub student_count: usize,
  pub competencies_count: usize,
  pub comment_count: usize,
  pub comment_total: usize,
  pub eval_count: usize,
  pub eval_total: usize,
}

#[derive(Debug, Serialize)]
pub struct EvalStatsSummary {
  pub c1: EvalStatsSummaryByCycle,
  pub c2: EvalStatsSummaryByCycle,
  pub c3: EvalStatsSummaryByCycle,
  pub c4: EvalStatsSummaryByCycle,
}

fn _summary(e: EvalStatsByCycle) -> EvalStatsSummaryByCycle {
  let student_count = e.total;
  let competencies_count = e.competencies.iter().count();
  let comment_count = e.comment_count;
  let comment_total = e.total;
  let eval_count = e
    .competencies
    .iter()
    .map(|x| x.count)
    .reduce(|acc, e| acc + e)
    .unwrap_or(0);
  let eval_total = competencies_count * e.total;
  EvalStatsSummaryByCycle {
    student_count,
    competencies_count,
    comment_count,
    comment_total,
    eval_count,
    eval_total,
  }
}

#[get("/summary")]
pub async fn summary(db: db::Db, token: jwt::JwtToken) -> Result<Json<EvalStatsSummary>, Status> {
  let group_id = token.claim.user_group.parse::<i64>().unwrap();
  let c1 = _summary(
    db.run(move |client| _eval_stats_by_cycle(client, &group_id, &Cycle::C1))
      .await
      .wrap_err("eval_stats_by_cycle error")
      .map_err(|_err| Status::InternalServerError)?,
  );
  let c2 = _summary(
    db.run(move |client| _eval_stats_by_cycle(client, &group_id, &Cycle::C2))
      .await
      .wrap_err("eval_stats_by_cycle error")
      .map_err(|_err| Status::InternalServerError)?,
  );
  let c3 = _summary(
    db.run(move |client| _eval_stats_by_cycle(client, &group_id, &Cycle::C3))
      .await
      .wrap_err("eval_stats_by_cycle error")
      .map_err(|_err| Status::InternalServerError)?,
  );
  let c4 = _summary(
    db.run(move |client| _eval_stats_by_cycle(client, &group_id, &Cycle::C4))
      .await
      .wrap_err("eval_stats_by_cycle error")
      .map_err(|_err| Status::InternalServerError)?,
  );
  let e = EvalStatsSummary { c1, c2, c3, c4 };
  Ok(Json(e))
}
