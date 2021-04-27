alter table "public"."socle_container"
  add constraint "socle_container_group_id_fkey"
  foreign key ("group_id")
  references "public"."group"
  ("id") on update cascade on delete cascade;
