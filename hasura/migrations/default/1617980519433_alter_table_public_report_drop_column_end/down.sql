alter table "public"."report" alter column "end" drop not null;
alter table "public"."report" add column "end" date;
