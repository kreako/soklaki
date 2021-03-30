alter table "public"."eval_observation"
  add constraint "eval_observation_user_id_fkey"
  foreign key ("user_id")
  references "public"."user"
  ("id") on update cascade on delete cascade;
