CREATE TABLE "public"."default_socle_container" ("id" serial NOT NULL, "rank" integer NOT NULL, "text" text NOT NULL, "container_id" integer, "cycle" cycle NOT NULL, "full_rank" text NOT NULL, "alpha_full_rank" text NOT NULL, PRIMARY KEY ("cycle") );