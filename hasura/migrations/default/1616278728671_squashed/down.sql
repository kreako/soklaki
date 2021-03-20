
alter table "public"."eval_observation_competency" alter column "updated_at" set default now();
alter table "public"."eval_observation_competency" alter column "updated_at" drop not null;
alter table "public"."eval_observation_competency" add column "updated_at" timestamptz;

alter table "public"."eval_observation_competency" alter column "created_at" set default now();
alter table "public"."eval_observation_competency" alter column "created_at" drop not null;
alter table "public"."eval_observation_competency" add column "created_at" timestamptz;

alter table "public"."eval_observation_student" alter column "updated_at" set default now();
alter table "public"."eval_observation_student" alter column "updated_at" drop not null;
alter table "public"."eval_observation_student" add column "updated_at" timestamptz;

alter table "public"."eval_observation_student" alter column "created_at" set default now();
alter table "public"."eval_observation_student" alter column "created_at" drop not null;
alter table "public"."eval_observation_student" add column "created_at" timestamptz;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."eval_observation_student" add column "updated_at" timestamptz
 not null default now();

CREATE OR REPLACE FUNCTION "public"."set_current_timestamp_updated_at"()
RETURNS TRIGGER AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER "set_public_eval_observation_student_updated_at"
BEFORE UPDATE ON "public"."eval_observation_student"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_eval_observation_student_updated_at" ON "public"."eval_observation_student" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."eval_observation_student" add column "created_at" timestamptz
 not null default now();

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."eval_observation_competency" add column "updated_at" timestamptz
 not null default now();

CREATE OR REPLACE FUNCTION "public"."set_current_timestamp_updated_at"()
RETURNS TRIGGER AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER "set_public_eval_observation_competency_updated_at"
BEFORE UPDATE ON "public"."eval_observation_competency"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_eval_observation_competency_updated_at" ON "public"."eval_observation_competency" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."eval_observation_competency" add column "created_at" timestamptz
 not null default now();

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."eval_evaluation" add column "updated_at" timestamptz
 not null default now();

CREATE OR REPLACE FUNCTION "public"."set_current_timestamp_updated_at"()
RETURNS TRIGGER AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER "set_public_eval_evaluation_updated_at"
BEFORE UPDATE ON "public"."eval_evaluation"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_eval_evaluation_updated_at" ON "public"."eval_evaluation" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."eval_evaluation" add column "created_at" timestamptz
 not null default now();


alter table "public"."group" rename column "payment_ok" to "paid";

DROP TABLE "public"."group_pricing";

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."group" add column "paid" boolean
 not null;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE VIEW user_manager AS
  SELECT id, name, active, manager, email, group_id
    FROM public.user;

alter table "public"."user" rename column "group_id" to "user_group_id";

alter table "public"."student" rename column "group_id" to "user_group_id";

alter table "public"."group" rename to "user_group";

DROP TABLE "public"."pricing_detail";

DELETE FROM "public"."pricing_plan" WHERE "id" = 'individual_backup';

DELETE FROM "public"."pricing_plan" WHERE "id" = 'individual_month';

DELETE FROM "public"."pricing_plan" WHERE "id" = 'individual_year';

DELETE FROM "public"."pricing_plan" WHERE "id" = 'school_year';

DROP TABLE "public"."pricing_plan";

DROP TABLE "public"."eval_observation_template_competency";

DROP TABLE "public"."eval_observation_template";

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE VIEW user_manager AS
  SELECT id, name, active, manager, email, user_group_id
    FROM public.user;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE VIEW user_manager AS
  SELECT id, name, active, manager, email
    FROM public.user;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."user" add column "manager" boolean
 not null;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."user_group" add column "is_school" boolean
 not null;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."user" add column "email_confirmed" boolean
 not null;

DROP TABLE "public"."report";

DROP TABLE "public"."eval_observation_competency";

DROP TABLE "public"."eval_observation_student";

DROP TABLE "public"."eval_observation";

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."user" add column "active" boolean
 not null;

DROP TABLE "public"."eval_evaluation";

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE TYPE eval_status AS ENUM ('Empty', 'InProgress', 'Acquired', 'NotAcquired');

alter table "public"."eval_comment" drop constraint "eval_comment_student_id_fkey";

alter table "public"."eval_comment" drop constraint "eval_comment_user_id_fkey";

DROP TABLE "public"."eval_comment";

alter table "public"."student" drop constraint "student_user_group_id_fkey";

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."student" add column "user_group_id" bigint
 not null;

DROP TABLE "public"."student";

alter table "public"."socle_subject" rename to "subject";

alter table "public"."socle_domain" rename to "domain";

alter table "public"."socle_component" rename to "component";

alter table "public"."socle_competency_subject" rename to "competency_subject";

alter table "public"."socle_competency" rename to "competency";

alter table "public"."user" drop constraint "user_user_group_id_fkey";

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."user" add column "name" text
 not null;

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- alter table "public"."user" add column "user_group_id" bigint
 not null;

DROP TABLE "public"."user_group";

DROP TABLE "public"."competency_subject";

DROP TABLE "public"."subject";

DROP TABLE "public"."competency";

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- DROP table "public"."competency";

-- Could not auto-generate a down migration.
-- Please write an appropriate down migration for the SQL below:
-- CREATE TYPE cycle AS ENUM ('c1', 'c2', 'c3', 'c4');

DROP TABLE "public"."competency";

DROP TABLE "public"."component";

DROP TABLE "public"."domain";

ALTER TABLE "public"."user_login" ALTER COLUMN "user_id" TYPE integer;

ALTER TABLE "public"."user_login" ALTER COLUMN "id" TYPE integer;

ALTER TABLE "public"."user" ALTER COLUMN "id" TYPE integer;

DROP TABLE "public"."user_navigation";

DROP TABLE "public"."user_login";

DROP TABLE "public"."user";
