alter table "public"."eval_observation" add column "date" date
 not null default current_date;
