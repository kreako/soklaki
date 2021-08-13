use chrono::{Datelike, NaiveDate};
use postgres_types::{FromSql, ToSql};
use serde::Serialize;

#[derive(PartialEq, Debug, FromSql, ToSql, Clone, Serialize)]
#[postgres(name = "eval_status")]
pub enum Cycle {
    #[postgres(name = "c1")]
    #[serde(rename = "c1")]
    C1,
    #[postgres(name = "c2")]
    #[serde(rename = "c2")]
    C2,
    #[postgres(name = "c3")]
    #[serde(rename = "c3")]
    C3,
    #[postgres(name = "c4")]
    #[serde(rename = "c4")]
    C4,
}

impl Cycle {
    pub fn to_str(&self) -> &'static str {
        match self {
            Cycle::C1 => "c1",
            Cycle::C2 => "c2",
            Cycle::C3 => "c3",
            Cycle::C4 => "c4",
        }
    }
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "c1" => Some(Cycle::C1),
            "c2" => Some(Cycle::C2),
            "c3" => Some(Cycle::C3),
            "c4" => Some(Cycle::C4),
            _ => None,
        }
    }
}

pub fn estimate_cycle(observation_date: &NaiveDate, birthdate: &NaiveDate) -> Cycle {
    let month = observation_date.month();
    let mut scholar_year = observation_date.year();
    if month <= 7 {
        // scholar year begins last year
        scholar_year -= 1;
    }

    let birth_year = birthdate.year();

    let age = scholar_year - birth_year;

    if age < 6 {
        Cycle::C1
    } else if age < 9 {
        Cycle::C2
    } else if age < 12 {
        Cycle::C3
    } else {
        Cycle::C4
    }
}
