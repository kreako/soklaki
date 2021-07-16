// Search for authorization header
// And check this starts with Bearer
// But do not validate the token : return as raw String
// Leave the validation to hasura

use rocket::http::Status;
use rocket::outcome::Outcome;
use rocket::request::{self, FromRequest, Request};
use rocket::response::status;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct AuthHeader {
    pub raw: String,
}

#[derive(Debug, Serialize)]
pub struct AuthHeaderResponse {
    pub absent_auth_header: bool,
}

#[rocket::async_trait]
impl<'r> FromRequest<'r> for AuthHeader {
    type Error = status::Custom<Json<AuthHeaderResponse>>;
    async fn from_request(
        request: &'r Request<'_>,
    ) -> request::Outcome<Self, status::Custom<Json<AuthHeaderResponse>>> {
        if let Some(authen_header) = request.headers().get_one("Authorization") {
            let authen_str = authen_header.to_string();
            if authen_str.starts_with("Bearer") {
                return Outcome::Success(AuthHeader { raw: authen_str });
            }
        }

        Outcome::Failure((
            Status::BadRequest,
            status::Custom(
                Status::Unauthorized,
                Json(AuthHeaderResponse {
                    absent_auth_header: true,
                }),
            ),
        ))
    }
}
