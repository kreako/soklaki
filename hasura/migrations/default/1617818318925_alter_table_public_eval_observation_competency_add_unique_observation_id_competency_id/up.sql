alter table "public"."eval_observation_competency" add constraint "eval_observation_competency_observation_id_competency_id_key" unique ("observation_id", "competency_id");
