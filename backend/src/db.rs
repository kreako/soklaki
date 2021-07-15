use rocket_sync_db_pools::database;
use rocket_sync_db_pools::postgres;

#[database("postgres")]
pub struct Db(postgres::Client);
