alter table "public"."default_socle_container" drop constraint "default_socle_container_pkey";
alter table "public"."default_socle_container"
    add constraint "default_socle_container_pkey"
    primary key ("id");
