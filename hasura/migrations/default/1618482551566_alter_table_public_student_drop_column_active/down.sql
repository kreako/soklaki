alter table "public"."student" alter column "active" set default true;
alter table "public"."student" alter column "active" drop not null;
alter table "public"."student" add column "active" bool;
