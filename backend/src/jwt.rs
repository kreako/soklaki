use jsonwebtoken::errors::Result as JwtResult;
use jsonwebtoken::{Algorithm, DecodingKey, TokenData, Validation};
use rocket::http::Status;
use rocket::outcome::Outcome;
use rocket::request::{self, FromRequest, Request};
use rocket::response::status;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};
use std::env;

// Token claim is :
// {
// 	'https://hasura.io/jwt/claims': {
// 		'x-hasura-allowed-roles': ['user'],
//		'x-hasura-default-role': 'user',
//		'x-hasura-user-id': '20',
//		'x-hasura-user-group': '23'
//	}
// }

#[derive(Debug, Serialize, Deserialize)]
pub struct JwtClaim {
	#[serde(rename = "x-hasura-allowed-roles")]
	roles: Vec<String>,
	#[serde(rename = "x-hasura-default-role")]
	role: String,
	#[serde(rename = "x-hasura-user-id")]
	user_id: String,
	#[serde(rename = "x-hasura-user-group")]
	user_group: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct JwtToken {
	#[serde(rename = "https://hasura.io/jwt/claims")]
	pub claim: JwtClaim,
}

#[derive(Debug, Serialize)]
pub struct TokenResponse {
	pub invalid_token: bool,
}

#[rocket::async_trait]
impl<'r> FromRequest<'r> for JwtToken {
	type Error = status::Custom<Json<TokenResponse>>;
	async fn from_request(
		request: &'r Request<'_>,
	) -> request::Outcome<Self, status::Custom<Json<TokenResponse>>> {
		if let Some(authen_header) = request.headers().get_one("Authorization") {
			let authen_str = authen_header.to_string();
			if authen_str.starts_with("Bearer") {
				let token = authen_str[6..authen_str.len()].trim();
				if let Ok(token_data) = decode_token(token.to_string()) {
					return Outcome::Success(token_data.claims);
				}
			}
		}

		Outcome::Failure((
			Status::BadRequest,
			status::Custom(
				Status::Unauthorized,
				Json(TokenResponse {
					invalid_token: true,
				}),
			),
		))
	}
}

fn decode_token(token: String) -> JwtResult<TokenData<JwtToken>> {
	let mut validation = Validation::new(Algorithm::HS256);
	validation.validate_exp = false;
	jsonwebtoken::decode::<JwtToken>(
		&token,
		&DecodingKey::from_secret(env::var("HASURA_GRAPHQL_JWT_SECRET").unwrap().as_ref()),
		&validation,
	)
}
