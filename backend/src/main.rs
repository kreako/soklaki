#[macro_use]
extern crate rocket;

use dotenv::dotenv;

mod db;
mod home_content;
mod jwt;

#[get("/")]
async fn index(db: db::Db, token: jwt::JwtToken) -> &'static str {
    println!("token: {:?}", token);
    db.run(|client| {
        for row in client
            .query(
                "SELECT id, firstname FROM public.user WHERE firstname is not null",
                &[],
            )
            .unwrap()
        {
            let id: i64 = row.get(0);
            let name: &str = row.get(1);
            println!("{} : {}", id, name);
        }
    })
    .await;
    "Hello, world!"
}

#[launch]
fn rocket() -> _ {
    dotenv().ok();
    rocket::build()
        .attach(db::Db::fairing())
        .mount("/home_content", routes![home_content::index])
        .mount("/", routes![index])
}
