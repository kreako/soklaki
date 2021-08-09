use serde::Serialize;

use super::cycle;

#[derive(Debug, Serialize, Clone)]
pub struct Competency {
    pub id: i32,
    pub full_rank: String,
}

impl Competency {
    fn new(id: i32, full_rank: String) -> Self {
        Competency {
            id: id,
            full_rank: full_rank,
        }
    }
}

pub fn competencies_from_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    cycle: &cycle::Cycle,
) -> Result<Vec<Competency>, postgres::error::Error> {
    Ok(client
        .query(
            "
SELECT id, full_rank
    FROM socle_competency
    WHERE group_id = $1
        AND active = true
		AND cycle::text = $2
	ORDER BY alpha_full_rank
",
            &[group_id, &cycle.to_str()],
        )?
        .iter()
        .map(|row| Competency::new(row.get(0), row.get(1)))
        .collect())
}
