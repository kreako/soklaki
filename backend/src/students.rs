use chrono::NaiveDate;
use rocket::http::Status;
use rocket::serde::json::Json;
use serde::Serialize;

use super::cycle::{self, estimate_cycle};
use super::db;
use super::jwt;
use super::period;

#[derive(Debug, Serialize)]
pub struct Student {
    pub id: i64,
    pub firstname: Option<String>,
    pub lastname: Option<String>,
}

pub fn students_by_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
    cycle: &cycle::Cycle,
) -> Result<Vec<Student>, postgres::error::Error> {
    let mut students = vec![];
    for row in client.query(
        "
SELECT birthdate, id, firstname, lastname FROM student
	WHERE group_id = $1
		AND school_entry <= $2
		AND (
			(school_exit is null)
			OR
			(school_exit >= $2)
		)
    ORDER BY firstname, lastname
	",
        &[group_id, date],
    )? {
        let birthdate = row.get(0);
        if &estimate_cycle(&date, &birthdate) == cycle {
            let id = row.get(1);
            let firstname = row.get(2);
            let lastname = row.get(3);
            students.push(Student {
                id: id,
                firstname: firstname,
                lastname: lastname,
            });
        }
    }
    Ok(students)
}

#[derive(Debug, Serialize)]
pub struct StudentFull {
    pub id: i64,
    pub firstname: String,
    pub lastname: String,
    pub birthdate: NaiveDate,
    pub school_entry: NaiveDate,
    pub school_exit: Option<NaiveDate>,
    pub cycle: cycle::Cycle,
}

pub fn filter_students_by_active(
    client: &mut postgres::Client,
    group_id: &i64,
    active: bool,
) -> Result<Vec<StudentFull>, postgres::error::Error> {
    let today = chrono::Local::today().naive_local();
    let mut students = vec![];
    for row in client.query(
        "
SELECT id, firstname, lastname, birthdate, school_entry, school_exit FROM student
	WHERE group_id = $1
        AND active = $2
    ORDER BY firstname, lastname
	",
        &[group_id, &active],
    )? {
        let id = row.get(0);
        let firstname = row.get(1);
        let lastname = row.get(2);
        let birthdate = row.get(3);
        let school_entry = row.get(4);
        let school_exit = row.get(5);
        let cycle = estimate_cycle(&today, &birthdate);
        students.push(StudentFull {
            id: id,
            firstname: firstname,
            lastname: lastname,
            birthdate: birthdate,
            school_entry: school_entry,
            school_exit: school_exit,
            cycle: cycle,
        });
    }
    Ok(students)
}

pub fn filter_students_by_period(
    students: Vec<StudentFull>,
    period: period::Period,
) -> Vec<StudentFull> {
    students
        .into_iter()
        .filter(|s| {
            s.school_entry <= period.end
                && (s.school_exit.is_none() || (s.school_exit.unwrap() >= period.start))
        })
        .collect()
}

pub fn filter_students_by_cycle(
    students: Vec<StudentFull>,
    cycle: cycle::Cycle,
) -> Vec<StudentFull> {
    students.into_iter().filter(|s| s.cycle == cycle).collect()
}

#[get("/?<period>&<cycle>")]
pub async fn students(
    db: db::Db,
    token: jwt::JwtToken,
    period: Option<i32>,
    cycle: Option<&str>,
) -> Result<Json<Vec<StudentFull>>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    let mut students = db
        .run(move |client| filter_students_by_active(client, &group_id, true))
        .await
        .map_err(|_err| Status::InternalServerError)?;
    if let Some(period_id) = period {
        let p = db
            .run(move |client| period::period_by_id(client, &group_id, &period_id))
            .await
            .map_err(|_err| Status::InternalServerError)?;
        students = filter_students_by_period(students, p);
    }
    if let Some(cycle_str) = cycle {
        if let Some(c) = cycle::Cycle::from_str(cycle_str) {
            students = filter_students_by_cycle(students, c);
        }
    }
    Ok(Json(students))
}
