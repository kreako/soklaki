

CREATE TABLE "public"."user" ("id" serial NOT NULL, "email" text NOT NULL, "hash" text NOT NULL, PRIMARY KEY ("id") , UNIQUE ("email"));

CREATE TABLE "public"."user_login" ("id" serial NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "user_id" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON UPDATE cascade ON DELETE cascade);

CREATE TABLE "public"."user_navigation" ("id" bigserial NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "user_id" bigint NOT NULL, "path" text NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON UPDATE cascade ON DELETE cascade);

ALTER TABLE "public"."user" ALTER COLUMN "id" TYPE int8;

ALTER TABLE "public"."user_login" ALTER COLUMN "id" TYPE int8;

ALTER TABLE "public"."user_login" ALTER COLUMN "user_id" TYPE int8;

CREATE TABLE "public"."domain" ("id" serial NOT NULL, "rank" integer NOT NULL, "title" text NOT NULL, PRIMARY KEY ("id") );

CREATE TABLE "public"."component" ("id" serial NOT NULL, "rank" integer NOT NULL, "title" text NOT NULL, "domain_id" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("domain_id") REFERENCES "public"."domain"("id") ON UPDATE cascade ON DELETE cascade);

CREATE TABLE "public"."competency" ("id" serial NOT NULL, "rank" integer NOT NULL, "text" text NOT NULL, "component_id" integer NOT NULL, "cycle" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("component_id") REFERENCES "public"."component"("id") ON UPDATE cascade ON DELETE cascade);

CREATE TYPE cycle AS ENUM ('c1', 'c2', 'c3', 'c4');

DROP table "public"."competency";

CREATE TABLE "public"."competency" ("id" serial NOT NULL, "rank" integer NOT NULL, "text" text NOT NULL, "component_id" integer NOT NULL, "cycle" cycle NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("component_id") REFERENCES "public"."component"("id") ON UPDATE cascade ON DELETE cascade);

CREATE TABLE "public"."subject" ("id" serial NOT NULL, "title" text NOT NULL, PRIMARY KEY ("id") );

CREATE TABLE "public"."competency_subject" ("id" serial NOT NULL, "competency_id" integer NOT NULL, "subject_id" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("competency_id") REFERENCES "public"."competency"("id") ON UPDATE cascade ON DELETE cascade, FOREIGN KEY ("subject_id") REFERENCES "public"."subject"("id") ON UPDATE cascade ON DELETE cascade, UNIQUE ("competency_id", "subject_id"));

CREATE TABLE "public"."user_group" ("id" bigserial NOT NULL, "name" text NOT NULL, PRIMARY KEY ("id") );

alter table "public"."user" add column "user_group_id" bigint
 not null;

alter table "public"."user" add column "name" text
 not null;

alter table "public"."user"
  add constraint "user_user_group_id_fkey"
  foreign key ("user_group_id")
  references "public"."user_group"
  ("id") on update cascade on delete cascade;

alter table "public"."competency" rename to "socle_competency";

alter table "public"."competency_subject" rename to "socle_competency_subject";

alter table "public"."component" rename to "socle_component";

alter table "public"."domain" rename to "socle_domain";

alter table "public"."subject" rename to "socle_subject";

CREATE TABLE "public"."student" ("id" bigserial NOT NULL, "firstname" text NOT NULL, "lastname" text NOT NULL, "birthdate" date NOT NULL, "school_entry" date, "cycle" cycle NOT NULL, "active" boolean NOT NULL DEFAULT true, PRIMARY KEY ("id") );

alter table "public"."student" add column "user_group_id" bigint
 not null;

alter table "public"."student"
  add constraint "student_user_group_id_fkey"
  foreign key ("user_group_id")
  references "public"."user_group"
  ("id") on update cascade on delete cascade;

CREATE TABLE "public"."eval_comment" ("id" bigserial NOT NULL, "user_id" bigint NOT NULL, "student_id" bigint NOT NULL, "text" text NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), PRIMARY KEY ("id") );
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
CREATE TRIGGER "set_public_eval_comment_updated_at"
BEFORE UPDATE ON "public"."eval_comment"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_eval_comment_updated_at" ON "public"."eval_comment" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';

alter table "public"."eval_comment"
  add constraint "eval_comment_user_id_fkey"
  foreign key ("user_id")
  references "public"."user"
  ("id") on update cascade on delete cascade;

alter table "public"."eval_comment"
  add constraint "eval_comment_student_id_fkey"
  foreign key ("student_id")
  references "public"."student"
  ("id") on update cascade on delete cascade;

CREATE TYPE eval_status AS ENUM ('Empty', 'InProgress', 'Acquired', 'NotAcquired');

CREATE TABLE "public"."eval_evaluation" ("id" bigserial NOT NULL, "user_id" bigint NOT NULL, "student_id" bigint NOT NULL, "competency_id" integer NOT NULL, "status" eval_status NOT NULL, "comment" text NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON UPDATE cascade ON DELETE cascade, FOREIGN KEY ("student_id") REFERENCES "public"."student"("id") ON UPDATE cascade ON DELETE cascade, FOREIGN KEY ("competency_id") REFERENCES "public"."socle_competency"("id") ON UPDATE cascade ON DELETE cascade);

alter table "public"."user" add column "active" boolean
 not null;

CREATE TABLE "public"."eval_observation" ("id" bigserial NOT NULL, "text" text NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), PRIMARY KEY ("id") );
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
CREATE TRIGGER "set_public_eval_observation_updated_at"
BEFORE UPDATE ON "public"."eval_observation"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_eval_observation_updated_at" ON "public"."eval_observation" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';

CREATE TABLE "public"."eval_observation_student" ("id" bigserial NOT NULL, "observation_id" bigint NOT NULL, "student_id" bigint NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("observation_id") REFERENCES "public"."eval_observation"("id") ON UPDATE cascade ON DELETE cascade, FOREIGN KEY ("student_id") REFERENCES "public"."student"("id") ON UPDATE cascade ON DELETE cascade);

CREATE TABLE "public"."eval_observation_competency" ("id" bigserial NOT NULL, "observation_id" bigint NOT NULL, "competency_id" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("observation_id") REFERENCES "public"."eval_observation"("id") ON UPDATE cascade ON DELETE cascade, FOREIGN KEY ("competency_id") REFERENCES "public"."socle_competency"("id") ON UPDATE cascade ON DELETE cascade);

CREATE TABLE "public"."report" ("id" serial NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "start" date NOT NULL, "end" date NOT NULL, "cycle" cycle NOT NULL, "json_path" text NOT NULL, "pdf_path" text NOT NULL, "student_id" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("student_id") REFERENCES "public"."student"("id") ON UPDATE cascade ON DELETE cascade);

alter table "public"."user" add column "email_confirmed" boolean
 not null;

alter table "public"."user_group" add column "is_school" boolean
 not null;

alter table "public"."user" add column "manager" boolean
 not null;


CREATE TABLE "public"."eval_observation_template" ("id" serial NOT NULL, "text" text NOT NULL, PRIMARY KEY ("id") );

CREATE TABLE "public"."eval_observation_template_competency" ("id" serial NOT NULL, "template_id" integer NOT NULL, "competency_id" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("template_id") REFERENCES "public"."eval_observation_template"("id") ON UPDATE cascade ON DELETE cascade, FOREIGN KEY ("competency_id") REFERENCES "public"."socle_competency"("id") ON UPDATE cascade ON DELETE cascade);

CREATE TABLE "public"."pricing_plan" ("id" text NOT NULL, PRIMARY KEY ("id") , UNIQUE ("id"));

INSERT INTO "public"."pricing_plan"("id") VALUES ('school_year');

INSERT INTO "public"."pricing_plan"("id") VALUES ('individual_year');

INSERT INTO "public"."pricing_plan"("id") VALUES ('individual_month');

INSERT INTO "public"."pricing_plan"("id") VALUES ('individual_backup');

CREATE TABLE "public"."pricing_detail" ("id" serial NOT NULL, "plan" text NOT NULL, "price_cent" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("plan") REFERENCES "public"."pricing_plan"("id") ON UPDATE cascade ON DELETE cascade, UNIQUE ("plan"));

alter table "public"."user_group" rename to "group";

alter table "public"."student" rename column "user_group_id" to "group_id";

alter table "public"."user" rename column "user_group_id" to "group_id";

CREATE OR REPLACE VIEW user_manager AS
  SELECT id, name, active, manager, email, group_id
    FROM public.user;

alter table "public"."group" add column "paid" boolean
 not null;

CREATE TABLE "public"."group_pricing" ("id" serial NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "start" date NOT NULL, "end" date NOT NULL, "plan" text NOT NULL, "price_cent" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("plan") REFERENCES "public"."pricing_plan"("id") ON UPDATE cascade ON DELETE cascade);

alter table "public"."group" rename column "paid" to "payment_ok";

alter table "public"."eval_evaluation" add column "created_at" timestamptz
 not null default now();

alter table "public"."eval_evaluation" add column "updated_at" timestamptz
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
