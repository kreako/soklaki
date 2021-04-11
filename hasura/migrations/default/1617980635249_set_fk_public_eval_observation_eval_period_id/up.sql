alter table "public"."eval_observation"
  add constraint "eval_observation_eval_period_id_fkey"
  foreign key ("eval_period_id")
  references "public"."eval_period"
  ("id") on update cascade on delete cascade;
