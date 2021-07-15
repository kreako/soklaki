use chrono::naive::NaiveDate;
use rocket::serde::json::Json;
use rocket_sync_db_pools::postgres;
use serde::Serialize;

use super::db;
use super::jwt;

#[derive(Debug, Serialize)]
struct CurrentTotal {
    total: i32,
    current: i32,
}

#[derive(Debug, Serialize)]
struct StatsSummaryByCycle {
    students_count: i32,
    competencies_count: i32,
    comments: CurrentTotal,
    observations: CurrentTotal,
    evaluations: CurrentTotal,
}

#[derive(Debug, Serialize)]
struct WeekCount {
    user: i32,
    observations: i32,
    evaluations: i32,
}

#[derive(Debug, Serialize)]
struct StatsWeek {
    week_start: NaiveDate,
    observations: i32,
    evaluations: i32,
    counts: Vec<WeekCount>,
}

#[derive(Debug, Serialize)]
pub struct StatsSummary {
    incomplete_observations_count: i32,
    c1: StatsSummaryByCycle,
    c2: StatsSummaryByCycle,
    c3: StatsSummaryByCycle,
    c4: StatsSummaryByCycle,
    weeks: Vec<StatsWeek>,
}

fn current_period_id(
    client: &mut postgres::Client,
    group_id: i64,
) -> Result<i32, postgres::error::Error> {
    let row = client.query_one(
        "
SELECT eval_period.id
	FROM eval_period_current
	JOIN eval_period
		ON eval_period_current.id = eval_period.id
	WHERE eval_period.group_id = $1
	",
        &[&group_id],
    )?;
    Ok(row.get(0))
}

fn count_incomplete_observations(
    client: &mut postgres::Client,
    period_id: i32,
) -> Result<i32, postgres::error::Error> {
    // No need to filter by group_id here
    // because eval_observation_period view definition
    // contains :
    //  JOIN "user" ON eval_period.group_id = "user".group_id
    //  JOIN eval_observation ON eval_observation.user_id = "user".id
    let row = client.query_one(
        "
SELECT COUNT(eval_observation.id)::int
	FROM eval_observation
	JOIN eval_observation_complete
        ON eval_observation.id = eval_observation_complete.observation_id
    JOIN eval_observation_period
        ON eval_observation_period.observation_id = eval_observation_complete.observation_id
    WHERE eval_observation_complete.complete = false
        AND eval_observation_period.eval_period_id = $1
        AND eval_observation.active = true
",
        &[&period_id],
    )?;

    Ok(row.get(0))
}

struct CountByCycle {
    c1: i32,
    c2: i32,
    c3: i32,
    c4: i32,
}

fn students_count_by_cycle(
    client: &mut postgres::Client,
    period_id: i32,
) -> Result<CountByCycle, postgres::error::Error> {
    let mut count = CountByCycle {
        c1: 0,
        c2: 0,
        c3: 0,
        c4: 0,
    };
    for row in client.query(
        "
SELECT COUNT(student.id)::int, student_current_cycle.current_cycle
    FROM student
    JOIN student_current_cycle
        ON student_current_cycle.student_id = student.id
    JOIN eval_period_student
        ON eval_period_student.student_id = student_current_cycle.student_id
    WHERE eval_period_id = $1
    GROUP BY student_current_cycle.current_cycle
",
        &[&period_id],
    )? {
        let c = row.get(0);
        let cycle: &str = row.get(1);
        match cycle {
            "c1" => {
                count.c1 = c;
            }
            "c2" => {
                count.c2 = c;
            }
            "c3" => {
                count.c3 = c;
            }
            "c4" => {
                count.c4 = c;
            }
            _ => panic!("Unknown cycle"),
        }
    }
    Ok(count)
}

fn competencies_count_by_cycle(
    client: &mut postgres::Client,
    group_id: i64,
) -> Result<CountByCycle, postgres::error::Error> {
    let mut count = CountByCycle {
        c1: 0,
        c2: 0,
        c3: 0,
        c4: 0,
    };
    for row in client.query(
        "
SELECT COUNT(id)::int, cycle::text
    FROM socle_competency
    WHERE group_id = $1
        AND active = true
    GROUP BY cycle
",
        &[&group_id],
    )? {
        let c = row.get(0);
        let cycle: &str = row.get(1);
        match cycle {
            "c1" => {
                count.c1 = c;
            }
            "c2" => {
                count.c2 = c;
            }
            "c3" => {
                count.c3 = c;
            }
            "c4" => {
                count.c4 = c;
            }
            _ => panic!("Unknown cycle"),
        }
    }
    Ok(count)
}

struct CurrentTotalByCycle {
    c1: CurrentTotal,
    c2: CurrentTotal,
    c3: CurrentTotal,
    c4: CurrentTotal,
}

fn comments_count_by_cycle(
    client: &mut postgres::Client,
    period_id: i32,
) -> Result<CurrentTotalByCycle, postgres::error::Error> {
    let mut count = CurrentTotalByCycle {
        c1: CurrentTotal {
            current: 0,
            total: 0,
        },
        c2: CurrentTotal {
            current: 0,
            total: 0,
        },
        c3: CurrentTotal {
            current: 0,
            total: 0,
        },
        c4: CurrentTotal {
            current: 0,
            total: 0,
        },
    };
    for row in client.query(
        "
SELECT cycle::text, total::int, comments::int
    FROM eval_comment_stats_summary
    WHERE period_id = $1
",
        &[&period_id],
    )? {
        let cycle: &str = row.get(0);
        let total = row.get(1);
        let comments = row.get(2);
        match cycle {
            "c1" => {
                count.c1.current = comments;
                count.c1.total = total;
            }
            "c2" => {
                count.c2.current = comments;
                count.c2.total = total;
            }
            "c3" => {
                count.c3.current = comments;
                count.c3.total = total;
            }
            "c4" => {
                count.c4.current = comments;
                count.c4.total = total;
            }
            _ => panic!("Unknown cycle"),
        }
    }
    Ok(count)
}

struct EvalCount {
    total: i32,
    observations: i32,
    evaluations: i32,
}

struct EvalByCycle {
    c1: EvalCount,
    c2: EvalCount,
    c3: EvalCount,
    c4: EvalCount,
}

fn eval_count_by_cycle(
    client: &mut postgres::Client,
    period_id: i32,
) -> Result<EvalByCycle, postgres::error::Error> {
    let mut count = EvalByCycle {
        c1: EvalCount {
            observations: 0,
            evaluations: 0,
            total: 0,
        },
        c2: EvalCount {
            observations: 0,
            evaluations: 0,
            total: 0,
        },
        c3: EvalCount {
            observations: 0,
            evaluations: 0,
            total: 0,
        },
        c4: EvalCount {
            observations: 0,
            evaluations: 0,
            total: 0,
        },
    };
    for row in client.query(
        "
SELECT cycle::text, total::int, observations::int, evaluations::int
    FROM eval_stats_summary
    WHERE period_id = $1
",
        &[&period_id],
    )? {
        let cycle: &str = row.get(0);
        let total = row.get(1);
        let observations = row.get(2);
        let evaluations = row.get(3);
        match cycle {
            "c1" => {
                count.c1.observations = observations;
                count.c1.evaluations = evaluations;
                count.c1.total = total;
            }
            "c2" => {
                count.c2.observations = observations;
                count.c2.evaluations = evaluations;
                count.c2.total = total;
            }
            "c3" => {
                count.c3.observations = observations;
                count.c3.evaluations = evaluations;
                count.c3.total = total;
            }
            "c4" => {
                count.c4.observations = observations;
                count.c4.evaluations = evaluations;
                count.c4.total = total;
            }
            _ => panic!("Unknown cycle"),
        }
    }
    Ok(count)
}

fn weeks_stats(
    client: &mut postgres::Client,
    period_id: i32,
) -> Result<Vec<StatsWeek>, postgres::error::Error> {
    let week_starts: Vec<NaiveDate> = client
        .query(
            "
SELECT week_start::date
    FROM eval_period_weeks
    WHERE eval_period_id = $1 AND week_start <= CURRENT_DATE
    ORDER BY week_start DESC
    LIMIT 4                     
    ",
            &[&period_id],
        )?
        .into_iter()
        .map(|x| x.get(0))
        .collect();

    let mut weeks = vec![];
    for week_start in week_starts {
        let mut counts = vec![];
        for row in client.query(
            "
SELECT user_id::int, observations_count::int
    FROM eval_observations_count_period_weeks
    WHERE eval_period_id = $1
        AND week_start::date = $2
",
            &[&period_id, &week_start],
        )? {
            let user_id = row.get(0);
            let observations_count = row.get(1);
            counts.push(WeekCount {
                user: user_id,
                observations: observations_count,
                evaluations: 0,
            })
        }
        for row in client.query(
            "
SELECT user_id::int, evaluations_count::int
    FROM eval_evaluations_count_period_weeks
    WHERE eval_period_id = $1
        AND week_start::date = $2
",
            &[&period_id, &week_start],
        )? {
            let user_id = row.get(0);
            let evaluations_count = row.get(1);
            let idx = match counts.iter().enumerate().find(|(_, e)| e.user == user_id) {
                Some((i, _)) => Some(i),
                None => None,
            };
            match idx {
                Some(i) => {
                    counts[i].evaluations = evaluations_count;
                }
                None => {
                    counts.push(WeekCount {
                        user: user_id,
                        observations: 0,
                        evaluations: evaluations_count,
                    });
                }
            }
        }
        let mut observations = 0;
        let mut evaluations = 0;
        for count in &counts {
            observations += count.observations;
            evaluations += count.evaluations;
        }
        counts.sort_by(|a, b| {
            let total_a = a.observations + a.evaluations;
            let total_b = b.observations + b.evaluations;
            total_b.cmp(&total_a)
        });
        weeks.push(StatsWeek {
            week_start: week_start.clone(),
            observations: observations,
            evaluations: evaluations,
            counts: counts,
        });
    }
    Ok(weeks)
}

#[get("/")]
pub async fn index(db: db::Db, token: jwt::JwtToken) -> Json<StatsSummary> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    let group_id1 = group_id.clone();
    let period_id = db
        .run(move |client| current_period_id(client, group_id1))
        .await
        .unwrap();
    let period_id1 = period_id.clone();
    let incomplete_observations_count = db
        .run(move |client| count_incomplete_observations(client, period_id1))
        .await
        .unwrap();
    let period_id2 = period_id.clone();
    let students_count = db
        .run(move |client| students_count_by_cycle(client, period_id2))
        .await
        .unwrap();
    let group_id2 = group_id.clone();
    let competencies_count = db
        .run(move |client| competencies_count_by_cycle(client, group_id2))
        .await
        .unwrap();
    let period_id3 = period_id.clone();
    let comments_count = db
        .run(move |client| comments_count_by_cycle(client, period_id3))
        .await
        .unwrap();
    let period_id4 = period_id.clone();
    let eval_count = db
        .run(move |client| eval_count_by_cycle(client, period_id4))
        .await
        .unwrap();
    let period_id5 = period_id.clone();
    let weeks = db
        .run(move |client| weeks_stats(client, period_id5))
        .await
        .unwrap();

    Json(StatsSummary {
        incomplete_observations_count: incomplete_observations_count,
        c1: StatsSummaryByCycle {
            students_count: students_count.c1,
            competencies_count: competencies_count.c1,
            comments: CurrentTotal {
                current: comments_count.c1.current,
                total: comments_count.c1.total,
            },
            observations: CurrentTotal {
                current: eval_count.c1.observations,
                total: eval_count.c1.total,
            },
            evaluations: CurrentTotal {
                current: eval_count.c1.evaluations,
                total: eval_count.c1.total,
            },
        },
        c2: StatsSummaryByCycle {
            students_count: students_count.c2,
            competencies_count: competencies_count.c2,
            comments: CurrentTotal {
                current: comments_count.c2.current,
                total: comments_count.c2.total,
            },
            observations: CurrentTotal {
                current: eval_count.c2.observations,
                total: eval_count.c2.total,
            },
            evaluations: CurrentTotal {
                current: eval_count.c2.evaluations,
                total: eval_count.c2.total,
            },
        },
        c3: StatsSummaryByCycle {
            students_count: students_count.c3,
            competencies_count: competencies_count.c3,
            comments: CurrentTotal {
                current: comments_count.c3.current,
                total: comments_count.c3.total,
            },
            observations: CurrentTotal {
                current: eval_count.c3.observations,
                total: eval_count.c3.total,
            },
            evaluations: CurrentTotal {
                current: eval_count.c3.evaluations,
                total: eval_count.c3.total,
            },
        },
        c4: StatsSummaryByCycle {
            students_count: students_count.c4,
            competencies_count: competencies_count.c4,
            comments: CurrentTotal {
                current: comments_count.c4.current,
                total: comments_count.c4.total,
            },
            observations: CurrentTotal {
                current: eval_count.c4.observations,
                total: eval_count.c4.total,
            },
            evaluations: CurrentTotal {
                current: eval_count.c4.evaluations,
                total: eval_count.c4.total,
            },
        },
        weeks: weeks,
    })
}
