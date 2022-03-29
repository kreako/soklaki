use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct Subject {
    pub id: i32,
    pub title: String,
}
