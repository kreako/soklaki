alter table "public"."socle_container"
  add constraint "socle_container_container_id_fkey"
  foreign key ("container_id")
  references "public"."socle_container"
  ("id") on update cascade on delete cascade;
