use chrono::NaiveDate;
use rocket::http::Status;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use super::competency;
use super::cycle;
use super::db;
use super::evaluation_status;
use super::jwt;
use super::period;
use super::student;
use super::students;
use super::subject;
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

#[derive(Debug, Serialize)]
pub struct CompetencyEvaluation {
    pub status: evaluation_status::EvaluationStatus,
    pub level: i32,
    pub comment: Option<String>,
    pub date: NaiveDate,
    pub from_current_period: bool,
}

#[derive(Debug, Serialize)]
pub struct Competency {
    pub id: i32,
    pub text: String,
    pub full_rank: String,
    // student id -> Evaluation
    pub evaluations: HashMap<i64, CompetencyEvaluation>,
}

#[derive(Debug, Serialize)]
pub struct SingleCycle {
    // student id list
    pub students: Vec<i64>,
    pub competencies: Vec<Competency>,
}

#[derive(Debug, Serialize)]
pub struct Cycles {
    pub c1: SingleCycle,
    pub c2: SingleCycle,
    pub c3: SingleCycle,
    pub c4: SingleCycle,
}

#[derive(Debug, Serialize)]
pub struct SubjectEvaluation {
    pub status: evaluation_status::EvaluationStatus,
    pub level: i32,
    pub comment: Option<String>,
    pub date: NaiveDate,
    pub from_current_period: bool,
}

#[derive(Debug, Serialize)]
pub struct SelectedSubjects {
    pub subject: subject::Subject,
    // student id -> Evaluation
    pub evaluations: HashMap<i64, SubjectEvaluation>,
}

#[derive(Debug, Serialize)]
pub struct CompleteObservation {
    pub id: i64,
    pub text: String,
    pub date: NaiveDate,
    pub complete: bool,
    pub user: user::User,
    pub period: period::Period,
    pub students: HashMap<i64, students::Student>,
    pub cycles: Cycles,
    pub subjects: Vec<SelectedSubjects>,
}

pub fn _complete_observation(
    client: &mut postgres::Client,
    observation_id: &i64,
    group_id: &i64,
) -> Result<CompleteObservation, postgres::error::Error> {
    // 01. let's get observation main field values
    let observation = client.query_one(
        "
SELECT  eval_observation.id,
        eval_observation.text,
        eval_observation.date,
        eval_observation_complete.complete,
        eval_observation.user_id,
        public.user.email,
        public.user.firstname,
        public.user.lastname,
        eval_period.id,
        eval_period.start,
        eval_period.end,
        eval_period.name
    FROM eval_observation
    JOIN eval_observation_complete
        ON eval_observation.id = eval_observation_complete.observation_id
    JOIN public.user
        ON eval_observation.user_id = public.user.id
    JOIN eval_observation_period
        ON eval_observation.id = eval_observation_period.observation_id
    JOIN eval_period
        ON eval_observation_period.eval_period_id = eval_period.id
    WHERE eval_observation.id = $1
    ",
        &[observation_id],
    )?;
    let id = observation.get(0);

    let user_id = observation.get(4);
    let email = observation.get(5);
    let firstname = observation.get(6);
    let lastname = observation.get(7);
    let user = user::User::new(user_id, *group_id, email, firstname, lastname);

    let period = period::Period {
        id: observation.get(8),
        start: observation.get(9),
        end: observation.get(10),
        name: observation.get(11),
    };

    // 02. Now gather all linked students
    let mut students = HashMap::new();
    let mut c1_students = Vec::new();
    let mut c2_students = Vec::new();
    let mut c3_students = Vec::new();
    let mut c4_students = Vec::new();

    for student in client.query("
SELECT  eval_observation_student.student_id,                                                                                                                                                                                                 
        student.firstname,                                                                                                                                                                                                                   
        student.lastname,                                                                                                                                                                                                                    
        student_current_cycle.current_cycle                                                                                                                                                                                                  
    FROM eval_observation_student                                                                                                                                                                                                              
    JOIN student                                                                                                                                                                                                                               
        ON student.id = eval_observation_student.student_id                                                                                                                                                                                      
    JOIN student_current_cycle                                                                                                                                                                                                                 
        ON student_current_cycle.student_id = student.id                                                                                                                                                                                         
    WHERE observation_id = $1  
    ", &[observation_id] )? {
        let student_id = student.get(0);
        let firstname = student.get(1);
        let lastname = student.get(2);
        let cycle = student.get(3);
        let obj = students::Student {
            id: student_id,
            firstname,
            lastname,
        };
        students.insert(student_id, obj);
        match cycle {
            "c1" => c1_students.push(student_id),
            "c2" => c2_students.push(student_id),
            "c3" => c3_students.push(student_id),
            "c4" => c4_students.push(student_id),
            _ => panic!("Unexpected cycle")
        };
    }

    // 03. All linked competencies with associated last evaluations
    let mut c1_competencies = Vec::new();
    let mut c2_competencies = Vec::new();
    let mut c3_competencies = Vec::new();
    let mut c4_competencies = Vec::new();

    for competency in client.query(
        "
SELECT  eval_observation_competency.competency_id,
        socle_competency.cycle,
        socle_competency.text,
        socle_competency.full_rank
    FROM eval_observation_competency
    JOIN socle_competency
        ON socle_competency.id = eval_observation_competency.competency_id
    WHERE observation_id = $1  
        ",
        &[observation_id],
    )? {
        let competency_id = competency.get(0);
        let cycle = competency.get(1);
        let text = competency.get(2);
        let full_rank = competency.get(3);

        let mut evaluations = HashMap::new();
        let student_ids = match cycle {
            cycle::Cycle::C1 => &c1_students,
            cycle::Cycle::C2 => &c2_students,
            cycle::Cycle::C3 => &c3_students,
            cycle::Cycle::C4 => &c4_students,
        };

        for student_id in student_ids {
            let last_eval = client.query_opt(
                "
SELECT level, comment, date FROM eval_evaluation
  WHERE student_id = $1 AND competency_id = $2
  ORDER BY date DESC LIMIT 1;
            ",
                &[&student_id, &competency_id],
            )?;
            if let Some(l) = last_eval {
                let level = l.get(0);
                let comment = l.get(1);
                let date = l.get(2);
                evaluations.insert(
                    *student_id,
                    CompetencyEvaluation {
                        status: evaluation_status::EvaluationStatus::from_level(level),
                        level,
                        comment,
                        date,
                        from_current_period: period.contains(&date),
                    },
                );
            }
        }

        let obj = Competency {
            id: competency_id,
            text,
            full_rank,
            evaluations,
        };

        match cycle {
            cycle::Cycle::C1 => c1_competencies.push(obj),
            cycle::Cycle::C2 => c2_competencies.push(obj),
            cycle::Cycle::C3 => c3_competencies.push(obj),
            cycle::Cycle::C4 => c4_competencies.push(obj),
        };
    }

    // 04. Every linked subjects with last evaluation
    let mut subjects = Vec::new();

    let student_ids = students.keys().collect::<Vec<&i64>>();
    for subject in client.query(
        "

    SELECT  eval_observation_subject.subject_id,
    socle_subject.title
FROM eval_observation_subject
JOIN socle_subject
ON eval_observation_subject.subject_id = socle_subject.id
WHERE observation_id = $1     
    ",
        &[observation_id],
    )? {
        let subject_id = subject.get(0);
        let subject_title = subject.get(1);

        let mut evaluations = HashMap::new();
        for student in &student_ids {
            let last_eval = client.query_opt(
                "
SELECT level, comment, date
    FROM eval_evaluation_subject 
    WHERE subject_id = $1 and student_id = $2
    ORDER BY date DESC LIMIT 1;
",
                &[&subject_id, student],
            )?;
            if let Some(l) = last_eval {
                let level = l.get(0);
                let comment = l.get(1);
                let date = l.get(2);
                evaluations.insert(
                    **student,
                    SubjectEvaluation {
                        status: evaluation_status::EvaluationStatus::from_level(level),
                        level,
                        comment,
                        date,
                        from_current_period: period.contains(&date),
                    },
                );
            }
        }

        subjects.push(SelectedSubjects {
            subject: subject::Subject {
                id: subject_id,
                title: subject_title,
            },
            evaluations,
        })
    }

    // 05. Now merge everything together
    let c1 = SingleCycle {
        students: c1_students,
        competencies: c1_competencies,
    };
    let c2 = SingleCycle {
        students: c2_students,
        competencies: c2_competencies,
    };
    let c3 = SingleCycle {
        students: c3_students,
        competencies: c3_competencies,
    };
    let c4 = SingleCycle {
        students: c4_students,
        competencies: c4_competencies,
    };

    let cycles = Cycles { c1, c2, c3, c4 };

    Ok(CompleteObservation {
        id: id,
        text: observation.get(1),
        date: observation.get(2),
        complete: observation.get(3),
        user,
        period,
        students,
        cycles,
        subjects,
    })
}

#[get("/single/<observation_id>")]
pub async fn single(
    db: db::Db,
    token: jwt::JwtToken,
    observation_id: i64,
) -> Result<Json<CompleteObservation>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    let observation = db
        .run(move |client| _complete_observation(client, &observation_id, &group_id))
        .await
        .map_err(|_err| Status::InternalServerError)?;
    Ok(Json(observation))
}
