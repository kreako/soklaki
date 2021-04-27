alter table "public"."default_socle_container"
  add constraint "default_socle_container_container_id_fkey"
  foreign key ("container_id")
  references "public"."default_socle_container"
  ("id") on update cascade on delete cascade;
