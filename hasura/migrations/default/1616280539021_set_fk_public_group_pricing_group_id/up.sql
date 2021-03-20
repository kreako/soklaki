alter table "public"."group_pricing"
  add constraint "group_pricing_group_id_fkey"
  foreign key ("group_id")
  references "public"."group"
  ("id") on update cascade on delete cascade;
