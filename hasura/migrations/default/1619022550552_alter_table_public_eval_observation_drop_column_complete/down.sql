alter table "public"."eval_observation" alter column "complete" set default false;
alter table "public"."eval_observation" alter column "complete" drop not null;
alter table "public"."eval_observation" add column "complete" bool;
