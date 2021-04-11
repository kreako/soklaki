alter table "public"."report" alter column "start" drop not null;
alter table "public"."report" add column "start" date;
