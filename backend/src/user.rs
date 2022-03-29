use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct User {
    pub id: i64,
    pub email: String,
    pub group_id: i64,
    pub firstname: Option<String>,
    pub lastname: Option<String>,
    pub initials: String,
}

impl User {
    pub fn new(
        id: i64,
        group_id: i64,
        email: String,
        firstname: Option<String>,
        lastname: Option<String>,
    ) -> Self {
        let f_firstname = match firstname {
            Some(ref s) => s.chars().nth(0).unwrap_or(' '),
            None => ' ',
        };
        let f_lastname = match lastname {
            Some(ref s) => s.chars().nth(0).unwrap_or(' '),
            None => ' ',
        };
        let initials = format!("{}{}", f_firstname, f_lastname);
        User {
            id,
            email,
            group_id,
            firstname,
            lastname,
            initials,
        }
    }
}

pub fn user(client: &mut postgres::Client, id: &i64) -> Result<User, postgres::error::Error> {
    let row = client.query_one(
        "
SELECT email, group_id, firstname, lastname
    FROM public.user
    WHERE id = $1
",
        &[id],
    )?;
    let email = row.get(0);
    let group_id = row.get(1);
    let firstname: Option<String> = row.get(2);
    let lastname: Option<String> = row.get(3);
    Ok(User::new(*id, group_id, email, firstname, lastname))
}
