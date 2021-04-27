CREATE TABLE "public"."default_socle_competency" ("id" serial NOT NULL, "rank" integer NOT NULL, "text" text NOT NULL, "container_id" integer NOT NULL, "cycle" cycle NOT NULL, "full_rank" text NOT NULL, "alpha_full_rank" text NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("container_id") REFERENCES "public"."default_socle_container"("id") ON UPDATE cascade ON DELETE cascade);
