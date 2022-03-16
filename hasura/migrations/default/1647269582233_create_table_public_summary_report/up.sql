CREATE TABLE "public"."summary_report" ("id" serial NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "cycle" cycle NOT NULL, "json_path" text NOT NULL, "pdf_path" text NOT NULL, "student_id" integer NOT NULL, "active" boolean NOT NULL DEFAULT true, "date" date NOT NULL DEFAULT now(), PRIMARY KEY ("id") );