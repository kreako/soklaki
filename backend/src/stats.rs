use chrono::NaiveDate;
use postgres_types::FromSql;
use rocket_sync_db_pools::postgres;
use std::collections::HashMap;
use std::vec::Vec;

use super::cycle::{estimate_cycle, Cycle};

fn competencies_from_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    cycle: &str,
) -> Result<Vec<i32>, postgres::error::Error> {
    Ok(client
        .query(
            "
SELECT id
    FROM socle_competency
    WHERE group_id = $1
        AND active = true
		AND cycle::text = $2
	ORDER BY alpha_full_rank
",
            &[group_id, &cycle],
        )?
        .iter()
        .map(|row| row.get(0))
        .collect())
}

#[derive(Debug)]
pub struct CompetenciesByCycle {
    pub c1: Vec<i32>,
    pub c2: Vec<i32>,
    pub c3: Vec<i32>,
    pub c4: Vec<i32>,
}

fn competencies_by_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
) -> Result<CompetenciesByCycle, postgres::error::Error> {
    Ok(CompetenciesByCycle {
        c1: competencies_from_cycle(client, group_id, Cycle::C1.to_str())?,
        c2: competencies_from_cycle(client, group_id, Cycle::C2.to_str())?,
        c3: competencies_from_cycle(client, group_id, Cycle::C3.to_str())?,
        c4: competencies_from_cycle(client, group_id, Cycle::C4.to_str())?,
    })
}

#[derive(Debug)]
pub struct StudentsByCycle {
    pub c1: Vec<i64>,
    pub c2: Vec<i64>,
    pub c3: Vec<i64>,
    pub c4: Vec<i64>,
}

fn students_by_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
) -> Result<StudentsByCycle, postgres::error::Error> {
    let mut c = StudentsByCycle {
        c1: vec![],
        c2: vec![],
        c3: vec![],
        c4: vec![],
    };
    for row in client.query(
        "
SELECT id, birthdate FROM student
	WHERE group_id = $1
		AND school_entry <= $2
		AND (
			(school_exit is null)
			OR
			(school_exit >= $2)
		)
	",
        &[group_id, date],
    )? {
        let id = row.get(0);
        let birthdate = row.get(1);
        match estimate_cycle(&date, &birthdate) {
            Cycle::C1 => c.c1.push(id),
            Cycle::C2 => c.c2.push(id),
            Cycle::C3 => c.c3.push(id),
            Cycle::C4 => c.c4.push(id),
        };
    }
    Ok(c)
}

#[derive(PartialEq, Debug, FromSql)]
#[postgres(name = "eval_status")]
pub enum EvaluationStatus {
    Empty,
    NotAcquired,
    InProgress,
    Acquired,
    TipTop,
}

#[derive(Debug)]
pub struct EvalSingle {
    observations: i32,
    evaluation: EvaluationStatus,
}

impl EvalSingle {
    fn new() -> Self {
        EvalSingle {
            observations: 0,
            evaluation: EvaluationStatus::Empty,
        }
    }
}

#[derive(Debug)]
pub struct EvalStats {
    // competency id -> student id -> EvalSingle
    c1: HashMap<i32, HashMap<i64, EvalSingle>>,
    c2: HashMap<i32, HashMap<i64, EvalSingle>>,
    c3: HashMap<i32, HashMap<i64, EvalSingle>>,
    c4: HashMap<i32, HashMap<i64, EvalSingle>>,
}

pub fn eval_stats(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
) -> Result<EvalStats, postgres::error::Error> {
    let mut e = EvalStats {
        c1: HashMap::new(),
        c2: HashMap::new(),
        c3: HashMap::new(),
        c4: HashMap::new(),
    };
    let competencies = competencies_by_cycle(client, &group_id)?;
    let students = students_by_cycle(client, group_id, date)?;
    for competency in &competencies.c1 {
        let mut h = HashMap::new();
        for student in &students.c1 {
            h.insert(*student, EvalSingle::new());
        }
        e.c1.insert(*competency, h);
    }
    for competency in &competencies.c2 {
        let mut h = HashMap::new();
        for student in &students.c2 {
            h.insert(*student, EvalSingle::new());
        }
        e.c2.insert(*competency, h);
    }
    for competency in &competencies.c3 {
        let mut h = HashMap::new();
        for student in &students.c3 {
            h.insert(*student, EvalSingle::new());
        }
        e.c3.insert(*competency, h);
    }
    for competency in &competencies.c4 {
        let mut h = HashMap::new();
        for student in &students.c4 {
            h.insert(*student, EvalSingle::new());
        }
        e.c4.insert(*competency, h);
    }
    eval_evaluation_stats_by_cycle(client, group_id, date, Cycle::C1.to_str(), &mut e.c1)?;
    eval_evaluation_stats_by_cycle(client, group_id, date, Cycle::C2.to_str(), &mut e.c2)?;
    eval_evaluation_stats_by_cycle(client, group_id, date, Cycle::C3.to_str(), &mut e.c3)?;
    eval_evaluation_stats_by_cycle(client, group_id, date, Cycle::C4.to_str(), &mut e.c4)?;

    eval_observation_stats(client, group_id, date, &mut e)?;

    Ok(e)
}

#[derive(Debug)]
pub struct EvalSingleSummary {
    pub total: i32,
    pub observations: i32,
    pub evaluations: i32,
}

impl EvalSingleSummary {
    fn new() -> Self {
        EvalSingleSummary {
            total: 0,
            observations: 0,
            evaluations: 0,
        }
    }
}

#[derive(Debug)]
pub struct EvalStatsSummary {
    pub c1: EvalSingleSummary,
    pub c2: EvalSingleSummary,
    pub c3: EvalSingleSummary,
    pub c4: EvalSingleSummary,
}

impl EvalStatsSummary {
    fn new() -> Self {
        EvalStatsSummary {
            c1: EvalSingleSummary::new(),
            c2: EvalSingleSummary::new(),
            c3: EvalSingleSummary::new(),
            c4: EvalSingleSummary::new(),
        }
    }
}

pub fn eval_stats_summary(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
) -> Result<EvalStatsSummary, postgres::error::Error> {
    let e = eval_stats(client, group_id, date)?;
    let mut s = EvalStatsSummary::new();
    eval_stats_summary_by_cycle(&e.c1, &mut s.c1);
    eval_stats_summary_by_cycle(&e.c2, &mut s.c2);
    eval_stats_summary_by_cycle(&e.c3, &mut s.c3);
    eval_stats_summary_by_cycle(&e.c4, &mut s.c4);
    Ok(s)
}

pub fn eval_stats_summary_by_cycle(
    e: &HashMap<i32, HashMap<i64, EvalSingle>>,
    s: &mut EvalSingleSummary,
) {
    for (_competency_id, by_students) in e {
        for (_student_id, eval_single) in by_students {
            s.total += 1;
            if eval_single.observations > 0 {
                s.observations += 1;
            }
            if eval_single.evaluation != EvaluationStatus::Empty {
                s.evaluations += 1;
            }
        }
    }
}

fn eval_evaluation_stats_by_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
    cycle: &'static str,
    h: &mut HashMap<i32, HashMap<i64, EvalSingle>>,
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
        &[group_id, date, &cycle],
    )? {
        let competency_id = row.get(0);
        let student_id = row.get(1);
        let status = row.get(2);
        if let Some(h2) = h.get_mut(&competency_id) {
            if let Some(e) = h2.get_mut(&student_id) {
                if e.evaluation == EvaluationStatus::Empty {
                    e.evaluation = status;
                }
            }
        }
    }
    Ok(())
}

fn eval_observation_stats(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
    e: &mut EvalStats,
) -> Result<(), postgres::error::Error> {
    for row in client.query(
        "
SELECT
	eval_observation_competency.competency_id,
	eval_observation_student.student_id,
	socle_competency.cycle::text
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
        &[group_id, date],
    )? {
        let competency_id = row.get(0);
        let student_id = row.get(1);
        let cycle = row.get(2);
        let h = match cycle {
            "c1" => &mut e.c1,
            "c2" => &mut e.c2,
            "c3" => &mut e.c3,
            "c4" => &mut e.c4,
            _ => panic!("Unknown cycle ?"),
        };
        if let Some(h2) = h.get_mut(&competency_id) {
            if let Some(s) = h2.get_mut(&student_id) {
                s.observations += 1;
            }
        }
    }

    Ok(())
}
