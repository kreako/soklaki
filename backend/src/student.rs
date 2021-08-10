use chrono::NaiveDate;
use eyre::WrapErr;
use rocket::http::Status;
use rocket::serde::json::Json;
use serde::Serialize;

use super::db;
use super::jwt;

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

fn _student_by_id(
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

#[get("/<id>")]
pub async fn student_by_id(
    db: db::Db,
    token: jwt::JwtToken,
    id: i64,
) -> Result<Json<Student>, Status> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    let student = db
        .run(move |client| _student_by_id(client, &id))
        .await
        .wrap_err("student_by_id error")
        .map_err(|_err| Status::InternalServerError)?;
    if student.group_id != group_id {
        return Err(Status::NotFound);
    }
    Ok(Json(student))
}
