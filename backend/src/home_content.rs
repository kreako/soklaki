use chrono::naive::NaiveDate;
use rocket::serde::json::Json;
use rocket_sync_db_pools::postgres;
use serde::Serialize;
use tracing::debug;

use super::cycle::Cycle;
use super::db;
use super::evaluation_status::EvaluationStatus;
use super::jwt;
use super::period;
use super::stats;

#[derive(Debug, Serialize)]
struct CurrentTotal {
    total: i32,
    current: i32,
}

#[derive(Debug, Serialize)]
struct StatsSummaryByCycle {
    progress: i32,
    students_count: i32,
    competencies_count: i32,
    comments: CurrentTotal,
    observations: CurrentTotal,
    evaluations: CurrentTotal,
}

#[derive(Debug, Serialize)]
struct User {
    id: i32,
    firstname: Option<String>,
    lastname: Option<String>,
}

#[derive(Debug, Serialize)]
struct WeekCount {
    user: User,
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
    progress: i32,
    c1: StatsSummaryByCycle,
    c2: StatsSummaryByCycle,
    c3: StatsSummaryByCycle,
    c4: StatsSummaryByCycle,
    weeks: Vec<StatsWeek>,
}

fn count_incomplete_observations(
    client: &mut postgres::Client,
    period_id: &i32,
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
        &[period_id],
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
    period_id: &i32,
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
        &[period_id],
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
    group_id: &i64,
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
        &[group_id],
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
    period_id: &i32,
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
        &[period_id],
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

fn weeks_stats(
    client: &mut postgres::Client,
    period_id: &i32,
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
SELECT public.user.id::int, observations_count::int, public.user.firstname, public.user.lastname
    FROM eval_observations_count_period_weeks
    JOIN public.user
        ON public.user.id = eval_observations_count_period_weeks.user_id
    WHERE eval_period_id = $1
        AND week_start::date = $2
",
            &[&period_id, &week_start],
        )? {
            let user_id = row.get(0);
            let observations_count = row.get(1);
            let user_firstname = row.get(2);
            let user_lastname = row.get(3);
            counts.push(WeekCount {
                user: User {
                    id: user_id,
                    firstname: user_firstname,
                    lastname: user_lastname,
                },
                observations: observations_count,
                evaluations: 0,
            })
        }
        for row in client.query(
            "
SELECT user_id::int, evaluations_count::int, public.user.firstname, public.user.lastname
    FROM eval_evaluations_count_period_weeks
    JOIN public.user
        ON public.user.id = eval_evaluations_count_period_weeks.user_id
    WHERE eval_period_id = $1
        AND week_start::date = $2
",
            &[&period_id, &week_start],
        )? {
            let user_id = row.get(0);
            let evaluations_count = row.get(1);
            let user_firstname = row.get(2);
            let user_lastname = row.get(3);
            let idx = match counts
                .iter()
                .enumerate()
                .find(|(_, e)| e.user.id == user_id)
            {
                Some((i, _)) => Some(i),
                None => None,
            };
            match idx {
                Some(i) => {
                    counts[i].evaluations = evaluations_count;
                }
                None => {
                    counts.push(WeekCount {
                        user: User {
                            id: user_id,
                            firstname: user_firstname,
                            lastname: user_lastname,
                        },
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

fn eval_stats_summary_by_cycle(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
    cycle: &Cycle,
    stats: &mut EvalSingleSummary,
) -> Result<(), postgres::error::Error> {
    let e = stats::eval_stats_by_cycle(client, group_id, date, cycle)?;
    stats.total = e.students.len() as i32 * e.stats.len() as i32;
    stats.observations = e.stats.iter().fold(0, |acc1, stat| {
        acc1 + stat.by_students.iter().fold(0, |acc2, student| {
            if student.observations > 0 {
                acc2 + 1
            } else {
                acc2
            }
        })
    });
    stats.evaluations = e.stats.iter().fold(0, |acc1, stat| {
        acc1 + stat.by_students.iter().fold(0, |acc2, student| {
            if student.evaluation != EvaluationStatus::Empty {
                acc2 + 1
            } else {
                acc2
            }
        })
    });
    Ok(())
}

pub fn eval_stats_summary(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
) -> Result<EvalStatsSummary, postgres::error::Error> {
    let mut s = EvalStatsSummary::new();
    eval_stats_summary_by_cycle(client, group_id, date, &Cycle::C1, &mut s.c1)?;
    eval_stats_summary_by_cycle(client, group_id, date, &Cycle::C2, &mut s.c2)?;
    eval_stats_summary_by_cycle(client, group_id, date, &Cycle::C3, &mut s.c3)?;
    eval_stats_summary_by_cycle(client, group_id, date, &Cycle::C4, &mut s.c4)?;
    Ok(s)
}

#[get("/")]
pub async fn index(db: db::Db, token: jwt::JwtToken) -> Json<StatsSummary> {
    let group_id = token.claim.user_group.parse::<i64>().unwrap();
    debug!("home_content current_period");
    let group_id1 = group_id.clone();
    let period = db
        .run(move |client| period::current_period_end(client, &group_id1))
        .await
        .unwrap();
    debug!("home_content count_incomplete_observations");
    let period_id1 = period.id.clone();
    let incomplete_observations_count = db
        .run(move |client| count_incomplete_observations(client, &period_id1))
        .await
        .unwrap();
    debug!("home_content students_count_by_cycle");
    let period_id2 = period.id.clone();
    let students_count = db
        .run(move |client| students_count_by_cycle(client, &period_id2))
        .await
        .unwrap();
    debug!("home_content competencies_count_by_cycle");
    let group_id2 = group_id.clone();
    let competencies_count = db
        .run(move |client| competencies_count_by_cycle(client, &group_id2))
        .await
        .unwrap();
    debug!("home_content comments_count_by_cycle");
    let period_id3 = period.id.clone();
    let comments_count = db
        .run(move |client| comments_count_by_cycle(client, &period_id3))
        .await
        .unwrap();
    debug!("home_content eval_stats_summary");
    let group_id3 = group_id.clone();
    let period_end = period.end.clone();
    let stats_summary = db
        .run(move |client| eval_stats_summary(client, &group_id3, &period_end))
        .await
        .unwrap();
    debug!("home_content week_stats");
    let period_id5 = period.id.clone();
    let weeks = db
        .run(move |client| weeks_stats(client, &period_id5))
        .await
        .unwrap();

    let mut summary = StatsSummary {
        incomplete_observations_count: incomplete_observations_count,
        progress: 0,
        c1: StatsSummaryByCycle {
            progress: 0,
            students_count: students_count.c1,
            competencies_count: competencies_count.c1,
            comments: CurrentTotal {
                current: comments_count.c1.current,
                total: comments_count.c1.total,
            },
            observations: CurrentTotal {
                current: stats_summary.c1.observations,
                total: stats_summary.c1.total,
            },
            evaluations: CurrentTotal {
                current: stats_summary.c1.evaluations,
                total: stats_summary.c1.total,
            },
        },
        c2: StatsSummaryByCycle {
            progress: 0,
            students_count: students_count.c2,
            competencies_count: competencies_count.c2,
            comments: CurrentTotal {
                current: comments_count.c2.current,
                total: comments_count.c2.total,
            },
            observations: CurrentTotal {
                current: stats_summary.c2.observations,
                total: stats_summary.c2.total,
            },
            evaluations: CurrentTotal {
                current: stats_summary.c2.evaluations,
                total: stats_summary.c2.total,
            },
        },
        c3: StatsSummaryByCycle {
            progress: 0,
            students_count: students_count.c3,
            competencies_count: competencies_count.c3,
            comments: CurrentTotal {
                current: comments_count.c3.current,
                total: comments_count.c3.total,
            },
            observations: CurrentTotal {
                current: stats_summary.c3.observations,
                total: stats_summary.c3.total,
            },
            evaluations: CurrentTotal {
                current: stats_summary.c3.evaluations,
                total: stats_summary.c3.total,
            },
        },
        c4: StatsSummaryByCycle {
            progress: 0,
            students_count: students_count.c4,
            competencies_count: competencies_count.c4,
            comments: CurrentTotal {
                current: comments_count.c4.current,
                total: comments_count.c4.total,
            },
            observations: CurrentTotal {
                current: stats_summary.c4.observations,
                total: stats_summary.c4.total,
            },
            evaluations: CurrentTotal {
                current: stats_summary.c4.evaluations,
                total: stats_summary.c4.total,
            },
        },
        weeks: weeks,
    };
    summary.c1.progress = (100 as f64
        * ((summary.c1.comments.current as f64) / (summary.c1.comments.total as f64)
            + (summary.c1.observations.current as f64) / (summary.c1.observations.total as f64)
            + (summary.c1.evaluations.current as f64) / (summary.c1.evaluations.total as f64))
        / 3 as f64) as i32;
    summary.c2.progress = (100 as f64
        * ((summary.c2.comments.current as f64) / (summary.c2.comments.total as f64)
            + (summary.c2.observations.current as f64) / (summary.c2.observations.total as f64)
            + (summary.c2.evaluations.current as f64) / (summary.c2.evaluations.total as f64))
        / 3 as f64) as i32;
    summary.c3.progress = (100 as f64
        * ((summary.c3.comments.current as f64) / (summary.c3.comments.total as f64)
            + (summary.c3.observations.current as f64) / (summary.c3.observations.total as f64)
            + (summary.c3.evaluations.current as f64) / (summary.c3.evaluations.total as f64))
        / 3 as f64) as i32;
    summary.c4.progress = (100 as f64
        * ((summary.c4.comments.current as f64) / (summary.c4.comments.total as f64)
            + (summary.c4.observations.current as f64) / (summary.c4.observations.total as f64)
            + (summary.c4.evaluations.current as f64) / (summary.c4.evaluations.total as f64))
        / 3 as f64) as i32;
    summary.progress =
        (((summary.c1.progress + summary.c2.progress + summary.c3.progress + summary.c4.progress)
            as f64)
            / 4 as f64) as i32;
    Json(summary)
}
