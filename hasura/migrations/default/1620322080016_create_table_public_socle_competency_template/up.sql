CREATE TABLE "public"."socle_competency_template" ("id" serial NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), "text" text NOT NULL, "competency_id" integer NOT NULL, "active" boolean NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("competency_id") REFERENCES "public"."socle_competency"("id") ON UPDATE cascade ON DELETE cascade);
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
CREATE TRIGGER "set_public_socle_competency_template_updated_at"
BEFORE UPDATE ON "public"."socle_competency_template"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_socle_competency_template_updated_at" ON "public"."socle_competency_template" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';
