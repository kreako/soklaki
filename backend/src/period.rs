use chrono::naive::NaiveDate;
use chrono::Datelike;
use serde::Serialize;
use tracing::debug;

#[derive(Debug, PartialEq)]
pub struct DefaultPeriod {
    name: String,
    start: NaiveDate,
    end: NaiveDate,
}

pub fn default_period(date: &NaiveDate) -> DefaultPeriod {
    // default period is :
    // S1 : year-08-01 -> year+1-01-31
    // S2 : year+1-02-01 -> year+1-07-31
    let month = date.month();
    let year = date.year();
    if month >= 8 {
        DefaultPeriod {
            name: format!("{}/{} - S1", year, year + 1),
            start: NaiveDate::from_ymd(year, 8, 1),
            end: NaiveDate::from_ymd(year + 1, 1, 31),
        }
    } else if month == 1 {
        DefaultPeriod {
            name: format!("{}/{} - S1", year - 1, year),
            start: NaiveDate::from_ymd(year - 1, 8, 1),
            end: NaiveDate::from_ymd(year, 1, 31),
        }
    } else {
        DefaultPeriod {
            name: format!("{}/{} - S2", year - 1, year),
            start: NaiveDate::from_ymd(year, 2, 1),
            end: NaiveDate::from_ymd(year, 7, 31),
        }
    }
}

pub struct PeriodId {
    pub id: i32,
}

pub fn insert_default_period(
    client: &mut postgres::Client,
    group_id: &i64,
    default_period: &DefaultPeriod,
) -> Result<PeriodId, postgres::error::Error> {
    let row = client.query_one(
        "
INSERT INTO eval_period
    (start, \"end\", group_id, name)
    VALUES
    ($1, $2, $3, $4)
    RETURNING id
    ",
        &[
            &default_period.start,
            &default_period.end,
            group_id,
            &default_period.name,
        ],
    )?;
    Ok(PeriodId { id: row.get(0) })
}

pub fn search_period_or_insert(
    client: &mut postgres::Client,
    group_id: &i64,
    date: &NaiveDate,
) -> Result<PeriodId, postgres::error::Error> {
    let r = client.query_opt(
        "
SELECT eval_period.id, eval_period.end
	FROM eval_period
	WHERE eval_period.group_id = $1
        AND eval_period.start <= $2
        AND eval_period.end >= $2
	",
        &[group_id, &date],
    )?;
    match r {
        Some(row) => Ok(PeriodId { id: row.get(0) }),
        None => {
            let default_period = default_period(date);
            Ok(insert_default_period(client, group_id, &default_period)?)
        }
    }
}

pub struct PeriodEnd {
    pub id: i32,
    pub end: NaiveDate,
}

pub fn current_period_end(
    client: &mut postgres::Client,
    group_id: &i64,
) -> Result<PeriodEnd, postgres::error::Error> {
    let today = chrono::Local::today().naive_local();
    debug!(?today, "current_period_end");
    let r = client.query_opt(
        "
SELECT eval_period.id, eval_period.end
	FROM eval_period
	WHERE eval_period.group_id = $1
        AND eval_period.start <= $2
        AND eval_period.end >= $2
	",
        &[group_id, &today],
    )?;
    debug!(?r, "current_period_end");
    match r {
        Some(row) => Ok(PeriodEnd {
            id: row.get(0),
            end: row.get(1),
        }),
        None => {
            let default_period = default_period(&today);
            let period = insert_default_period(client, group_id, &default_period)?;
            Ok(PeriodEnd {
                id: period.id,
                end: default_period.end,
            })
        }
    }
}

#[derive(Debug, Serialize)]
pub struct Period {
    pub id: i32,
    pub start: NaiveDate,
    pub end: NaiveDate,
    pub name: String,
}

pub fn current_period(
    client: &mut postgres::Client,
    group_id: &i64,
) -> Result<Period, postgres::error::Error> {
    let today = chrono::Local::today().naive_local();
    let r = client.query_opt(
        "
SELECT eval_period.id, eval_period.start, eval_period.end, eval_period.name
	FROM eval_period
	WHERE eval_period.group_id = $1
        AND eval_period.start <= $2
        AND eval_period.end >= $2
	",
        &[group_id, &today],
    )?;
    match r {
        Some(row) => Ok(Period {
            id: row.get(0),
            start: row.get(1),
            end: row.get(2),
            name: row.get(3),
        }),
        None => {
            let default_period = default_period(&today);
            let period = insert_default_period(client, group_id, &default_period)?;
            Ok(Period {
                id: period.id,
                start: default_period.start,
                end: default_period.end,
                name: default_period.name,
            })
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_period() {
        assert_eq!(
            default_period(&NaiveDate::from_ymd(2021, 10, 2)),
            DefaultPeriod {
                name: String::from("2021/2022 - S1"),
                start: NaiveDate::from_ymd(2021, 8, 1),
                end: NaiveDate::from_ymd(2022, 1, 31),
            }
        );
        assert_eq!(
            default_period(&NaiveDate::from_ymd(2021, 8, 1)),
            DefaultPeriod {
                name: String::from("2021/2022 - S1"),
                start: NaiveDate::from_ymd(2021, 8, 1),
                end: NaiveDate::from_ymd(2022, 1, 31),
            }
        );
        assert_eq!(
            default_period(&NaiveDate::from_ymd(2021, 1, 31)),
            DefaultPeriod {
                name: String::from("2020/2021 - S1"),
                start: NaiveDate::from_ymd(2020, 8, 1),
                end: NaiveDate::from_ymd(2021, 1, 31),
            }
        );
        assert_eq!(
            default_period(&NaiveDate::from_ymd(2021, 2, 1)),
            DefaultPeriod {
                name: String::from("2020/2021 - S2"),
                start: NaiveDate::from_ymd(2021, 2, 1),
                end: NaiveDate::from_ymd(2021, 7, 31),
            }
        );
        assert_eq!(
            default_period(&NaiveDate::from_ymd(2021, 7, 31)),
            DefaultPeriod {
                name: String::from("2020/2021 - S2"),
                start: NaiveDate::from_ymd(2021, 2, 1),
                end: NaiveDate::from_ymd(2021, 7, 31),
            }
        );
    }
}
