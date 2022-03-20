use rocket::serde::json::Json;
use serde::Serialize;

use super::cycle;
use super::db;
use super::jwt;

pub fn sorted_competencies_by_cycle(
  client: &mut postgres::Client,
  group_id: &i64,
  cycle: &cycle::Cycle,
) -> Result<Vec<i32>, postgres::error::Error> {
  return Ok(
    client
      .query(
        "
SELECT id
    FROM socle_competency
WHERE group_id = $1
    AND active = true
    AND cycle::text = $2
ORDER BY alpha_full_rank
",
        &[group_id, &cycle.to_str()],
      )?
      .into_iter()
      .map(|x| x.get(0))
      .collect(),
  );
}

#[derive(Debug, Serialize, Clone)]
pub struct SortedCompetencies {
  pub c1: Vec<i32>,
  pub c2: Vec<i32>,
  pub c3: Vec<i32>,
  pub c4: Vec<i32>,
}

#[get("/sorted")]
pub async fn sorted(db: db::Db, token: jwt::JwtToken) -> Json<SortedCompetencies> {
  let group_id = token.claim.user_group.parse::<i64>().unwrap();
  let c1 = db
    .run(move |client| sorted_competencies_by_cycle(client, &group_id.clone(), &cycle::Cycle::C1))
    .await
    .unwrap();
  let c2 = db
    .run(move |client| sorted_competencies_by_cycle(client, &group_id.clone(), &cycle::Cycle::C2))
    .await
    .unwrap();
  let c3 = db
    .run(move |client| sorted_competencies_by_cycle(client, &group_id.clone(), &cycle::Cycle::C3))
    .await
    .unwrap();
  let c4 = db
    .run(move |client| sorted_competencies_by_cycle(client, &group_id.clone(), &cycle::Cycle::C4))
    .await
    .unwrap();
  let sorted = SortedCompetencies { c1, c2, c3, c4 };
  Json(sorted)
}
