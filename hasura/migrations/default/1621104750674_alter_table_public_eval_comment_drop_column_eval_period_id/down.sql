alter table "public"."eval_comment"
  add constraint "eval_comment_eval_period_id_fkey"
  foreign key (eval_period_id)
  references "public"."eval_period"
  (id) on update cascade on delete cascade;
alter table "public"."eval_comment" alter column "eval_period_id" drop not null;
alter table "public"."eval_comment" add column "eval_period_id" int4;
