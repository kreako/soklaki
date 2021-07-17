#[macro_use]
extern crate rocket;

use dotenv::dotenv;
use reqwest;
use rocket::data::ByteUnit;
use rocket::response::content;
use rocket::response::status::BadRequest;
use rocket::Data;
use std::path::PathBuf;

mod auth_header;
mod db;
mod home_content;
mod jwt;

#[post("/<path..>", data = "<data>")]
async fn forward_to_hasura(
    auth: auth_header::AuthHeader,
    path: PathBuf,
    data: Data<'_>,
) -> Result<content::Json<String>, BadRequest<String>> {
    // Try to forward request to hasura
    let body = data
        .open(ByteUnit::Megabyte(5))
        .into_bytes()
        .await
        .map_err(|e| BadRequest(Some(e.to_string())))?;
    let client = reqwest::Client::new();
    let mut hasura_path = PathBuf::from("http://localhost:8080");
    hasura_path.push("api");
    hasura_path.push("rest");
    hasura_path.push(path.as_path().file_name().unwrap());
    let res = client
        .post(hasura_path.to_string_lossy().to_string())
        .body(body.into_inner())
        .header("Authorization", auth.raw)
        .send()
        .await
        .map_err(|e| BadRequest(Some(e.to_string())))?;
    if res.status().is_success() {
        Ok(content::Json(
            res.text()
                .await
                .map_err(|e| BadRequest(Some(e.to_string())))?,
        ))
    } else {
        Err(BadRequest(Some(
            res.text()
                .await
                .map_err(|e| BadRequest(Some(e.to_string())))?,
        )))
    }
}

#[launch]
fn rocket() -> _ {
    dotenv().ok();
    rocket::build()
        .attach(db::Db::fairing())
        .mount("/home_content", routes![home_content::index])
        .mount("/", routes![forward_to_hasura])
}
