#[macro_use]
extern crate rocket;

use dotenv::dotenv;
use eyre::{self, WrapErr};
use reqwest;
use rocket::data::ByteUnit;
use rocket::response::content;
use rocket::response::status::BadRequest;
use rocket::Data;
use std::path::PathBuf;
use tracing::info;
use tracing_subscriber::EnvFilter;

mod auth_header;
mod competencies;
mod competency;
mod cycle;
mod db;
mod done;
mod eval_stats;
mod evaluation;
mod evaluation_status;
mod home_content;
mod jwt;
mod observation;
mod period;
mod stats;
mod student;
mod students;
mod subject;
mod user;

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

async fn forward_unauthentified_to_hasura(
    data: Data<'_>,
    api_end: &'static str,
) -> Result<content::Json<String>, BadRequest<String>> {
    // Try to forward request to hasura
    let body = data
        .open(ByteUnit::Megabyte(5))
        .into_bytes()
        .await
        .map_err(|e| BadRequest(Some(e.to_string())))?;
    let client = reqwest::Client::new();
    let mut hasura_path = PathBuf::from("http://localhost:8080/api/rest/");
    hasura_path.push(api_end);
    let res = client
        .post(hasura_path.to_string_lossy().to_string())
        .body(body.into_inner())
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

#[post("/ping", data = "<data>")]
async fn forward_ping_to_hasura(
    data: Data<'_>,
) -> Result<content::Json<String>, BadRequest<String>> {
    forward_unauthentified_to_hasura(data, "ping").await
}

#[post("/login", data = "<data>")]
async fn forward_login_to_hasura(
    data: Data<'_>,
) -> Result<content::Json<String>, BadRequest<String>> {
    forward_unauthentified_to_hasura(data, "login").await
}

#[post("/signup", data = "<data>")]
async fn forward_signup_to_hasura(
    data: Data<'_>,
) -> Result<content::Json<String>, BadRequest<String>> {
    forward_unauthentified_to_hasura(data, "signup").await
}

#[post("/invitation-verify-token", data = "<data>")]
async fn forward_invitation_verify_token_to_hasura(
    data: Data<'_>,
) -> Result<content::Json<String>, BadRequest<String>> {
    forward_unauthentified_to_hasura(data, "invitation-verify-token").await
}

#[post("/invitation-signup-token", data = "<data>")]
async fn forward_invitation_signup_token_to_hasura(
    data: Data<'_>,
) -> Result<content::Json<String>, BadRequest<String>> {
    forward_unauthentified_to_hasura(data, "invitation-signup-token").await
}

fn setup() -> eyre::Result<()> {
    dotenv().wrap_err("Unable to initialize dotenv :(")?;

    if std::env::var("RUST_LIB_BACKTRACE").is_err() {
        std::env::set_var("RUST_LIB_BACKTRACE", "1")
    }
    color_eyre::install().wrap_err("Unable to install color_eyre :(")?;

    if std::env::var("RUST_LOG").is_err() {
        std::env::set_var("RUST_LOG", "info")
    }
    tracing_subscriber::fmt::fmt()
        .with_env_filter(EnvFilter::from_default_env())
        .init();

    info!("Setup done successfully !");
    Ok(())
}

#[launch]
fn rocket() -> _ {
    setup().unwrap();
    rocket::build()
        .attach(db::Db::fairing())
        .mount(
            "/eval_stats",
            routes![eval_stats::eval_stats_by_cycle, eval_stats::summary],
        )
        .mount("/home_content", routes![home_content::index])
        .mount("/stats", routes![stats::stats_by_cycle])
        .mount(
            "/student",
            routes![
                student::student_by_id,
                student::lastname,
                student::firstname,
                student::birthdate,
                student::school_entry,
                student::school_exit,
                student::active,
            ],
        )
        .mount("/students", routes![students::students,])
        .mount(
            "/evaluation",
            routes![
                evaluation::evaluation_single,
                evaluation::evaluation_multi,
                evaluation::new_evaluation
            ],
        )
        .mount(
            "/observation",
            routes![
                observation::prefill,
                observation::new_prefill,
                observation::single,
                observation::single_text,
                observation::single_date,
                observation::single_add_student,
                observation::single_delete_student
            ],
        )
        .mount("/competencies", routes![competencies::sorted])
        .mount(
            "/",
            routes![
                forward_ping_to_hasura,
                forward_login_to_hasura,
                forward_signup_to_hasura,
                forward_invitation_signup_token_to_hasura,
                forward_invitation_verify_token_to_hasura,
                forward_to_hasura
            ],
        )
}
