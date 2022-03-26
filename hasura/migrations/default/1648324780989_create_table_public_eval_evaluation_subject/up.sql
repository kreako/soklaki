CREATE TABLE "public"."eval_evaluation_subject" ("id" serial NOT NULL, "user_id" bigint NOT NULL, "student_id" bigint NOT NULL, "subject_id" integer NOT NULL, "comment" text, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), "date" date NOT NULL, "active" boolean NOT NULL DEFAULT true, "level" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON UPDATE restrict ON DELETE restrict, FOREIGN KEY ("student_id") REFERENCES "public"."student"("id") ON UPDATE restrict ON DELETE restrict, FOREIGN KEY ("subject_id") REFERENCES "public"."socle_subject"("id") ON UPDATE restrict ON DELETE restrict);
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
CREATE TRIGGER "set_public_eval_evaluation_subject_updated_at"
BEFORE UPDATE ON "public"."eval_evaluation_subject"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_eval_evaluation_subject_updated_at" ON "public"."eval_evaluation_subject" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';
