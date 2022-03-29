use postgres_types::{FromSql, ToSql};
use serde::{Deserialize, Serialize};

#[derive(PartialEq, Debug, FromSql, ToSql, Serialize, Deserialize)]
#[postgres(name = "eval_status")]
pub enum EvaluationStatus {
    Empty,
    NotAcquired,
    InProgress,
    Acquired,
    TipTop,
}

impl EvaluationStatus {
    pub fn from_level(level: i32) -> Self {
        if level < 25 {
            EvaluationStatus::NotAcquired
        } else if level < 50 {
            EvaluationStatus::InProgress
        } else if level < 75 {
            EvaluationStatus::Acquired
        } else {
            EvaluationStatus::TipTop
        }
    }

    /* pub fn to_level(&self) -> i32 {
        match self {
            EvaluationStatus::Empty => 0,
            EvaluationStatus::NotAcquired => 13,
            EvaluationStatus::InProgress => 38,
            EvaluationStatus::Acquired => 63,
            EvaluationStatus::TipTop => 88,
        }
    } */
}
