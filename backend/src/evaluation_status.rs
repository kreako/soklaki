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
