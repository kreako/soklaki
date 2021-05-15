alter table "public"."report"
  add constraint "report_eval_period_id_fkey"
  foreign key (eval_period_id)
  references "public"."eval_period"
  (id) on update cascade on delete cascade;
alter table "public"."report" alter column "eval_period_id" drop not null;
alter table "public"."report" add column "eval_period_id" int4;
