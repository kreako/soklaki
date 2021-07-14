#[macro_use]
extern crate rocket;

use rocket_sync_db_pools::database;
use rocket_sync_db_pools::postgres;

#[database("postgres")]
struct Db(postgres::Client);

#[get("/")]
async fn index(db: Db) -> &'static str {
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
    rocket::build()
        .attach(Db::fairing())
        .mount("/", routes![index])
}
