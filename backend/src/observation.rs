use chrono::NaiveDate;
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct SingleObservation {
    pub id: i64,
    pub text: String,
    pub date: NaiveDate,
}

pub fn single_competency_observations(
    client: &mut postgres::Client,
    competency_id: &i32,
    student_id: &i64,
) -> Result<Vec<SingleObservation>, postgres::error::Error> {
    Ok(client
        .query(
            "
SELECT eval_observation.id, eval_observation.text, eval_observation.date
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
        .map(|row| SingleObservation {
            id: row.get(0),
            text: row.get(1),
            date: row.get(2),
        })
        .collect())
}
