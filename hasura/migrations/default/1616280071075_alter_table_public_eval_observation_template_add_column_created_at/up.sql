alter table "public"."eval_observation_template" add column "created_at" timestamptz
 not null default now();
