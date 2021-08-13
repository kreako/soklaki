use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct Done {
    pub done: bool,
}

impl Done {
    pub fn done() -> Self {
        Done { done: true }
    }
}
