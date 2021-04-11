alter table "public"."eval_comment" add column "date" Date
 not null default CURRENT_DATE;
