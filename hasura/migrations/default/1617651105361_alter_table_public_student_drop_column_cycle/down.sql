alter table "public"."student" alter column "cycle" drop not null;
alter table "public"."student" add column "cycle" cycle;
