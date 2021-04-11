alter table "public"."eval_evaluation" add column "date" date
 not null default CURRENT_DATE;
