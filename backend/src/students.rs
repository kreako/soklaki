use chrono::NaiveDate;
use serde::Serialize;

use super::cycle::{self, estimate_cycle};

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
