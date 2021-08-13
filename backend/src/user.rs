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
    let f_firstname = match firstname {
        Some(ref s) => s.chars().nth(0).unwrap_or(' '),
        None => ' ',
    };
    let f_lastname = match lastname {
        Some(ref s) => s.chars().nth(0).unwrap_or(' '),
        None => ' ',
    };
    let initials = format!("{}{}", f_firstname, f_lastname);
    Ok(User {
        id: *id,
        email: email,
        group_id: group_id,
        firstname: firstname,
        lastname: lastname,
        initials: initials,
    })
}
