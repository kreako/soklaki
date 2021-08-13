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

#[derive(Debug, Serialize)]
pub struct Container {
    pub id: i32,
    pub rank: i32,
    pub text: String,
    pub parent: Box<Option<Container>>,
    pub cycle: cycle::Cycle,
    pub full_rank: String,
    pub group_id: i64,
    pub active: bool,
}

pub fn container(
    client: &mut postgres::Client,
    id: &i32,
) -> Result<Container, postgres::error::Error> {
    let row = client.query_one(
        "
SELECT rank, text, container_id, cycle::text, full_rank, group_id, active
    FROM socle_container
    WHERE id = $1
",
        &[id],
    )?;
    let rank = row.get(0);
    let text = row.get(1);
    let container_id: Option<i32> = row.get(2);
    let cycle = cycle::Cycle::from_str(row.get(3)).unwrap();
    let full_rank = row.get(4);
    let group_id = row.get(5);
    let active = row.get(6);

    let parent = match container_id {
        Some(c) => Some(container(client, &c)?),
        None => None,
    };

    Ok(Container {
        id: *id,
        rank: rank,
        text: text,
        parent: Box::new(parent),
        cycle: cycle,
        full_rank: full_rank,
        group_id: group_id,
        active: active,
    })
}

#[derive(Debug, Serialize)]
pub struct SingleCompetency {
    pub id: i32,
    pub rank: i32,
    pub text: String,
    pub parent: Container,
    pub cycle: cycle::Cycle,
    pub full_rank: String,
    pub group_id: i64,
    pub active: bool,
    pub previous: Option<Competency>,
    pub next: Option<Competency>,
}

pub fn single_competency(
    client: &mut postgres::Client,
    id: &i32,
) -> Result<SingleCompetency, postgres::error::Error> {
    let row = client.query_one(
        "
SELECT rank, text, container_id, cycle::text, full_rank, group_id, active
    FROM socle_competency
    WHERE id = $1
",
        &[id],
    )?;
    let rank = row.get(0);
    let text = row.get(1);
    let container_id = row.get(2);
    let cycle = cycle::Cycle::from_str(row.get(3)).unwrap();
    let full_rank = row.get(4);
    let group_id = row.get(5);
    let active = row.get(6);

    let container = container(client, &container_id)?;

    let (previous, next) = previous_next_competency(client, id, &group_id, &cycle)?;

    Ok(SingleCompetency {
        id: *id,
        rank: rank,
        text: text,
        parent: container,
        cycle: cycle,
        full_rank: full_rank,
        group_id: group_id,
        active: active,
        previous: previous,
        next: next,
    })
}

pub fn previous_next_competency(
    client: &mut postgres::Client,
    competency_id: &i32,
    group_id: &i64,
    cycle: &cycle::Cycle,
) -> Result<(Option<Competency>, Option<Competency>), postgres::error::Error> {
    let mut found = false;
    let mut previous = None;
    for row in client.query(
        "
SELECT id, full_rank
    FROM socle_competency
WHERE group_id = $1
    AND active = true
    AND cycle::text = $2
ORDER BY alpha_full_rank
",
        &[group_id, &cycle.to_str()],
    )? {
        let id = row.get(0);
        let full_rank = row.get(1);
        if found {
            return Ok((
                previous,
                Some(Competency {
                    id: id,
                    full_rank: full_rank,
                }),
            ));
        } else {
            if id == *competency_id {
                found = true;
            } else {
                previous = Some(Competency {
                    id: id,
                    full_rank: full_rank,
                });
            }
        }
    }
    if found {
        // I'm here because there is no next competency
        return Ok((previous, None));
    } else {
        unreachable!();
    }
}
