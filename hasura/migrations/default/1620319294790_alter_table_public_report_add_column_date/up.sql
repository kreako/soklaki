alter table "public"."report" add column "date" date
 not null default now();
