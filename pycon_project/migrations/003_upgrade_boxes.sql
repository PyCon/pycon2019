TRUNCATE TABLE "boxes_box";

ALTER TABLE "boxes_box" ADD COLUMN "created_by_id" integer REFERENCES "auth_user" ("id") NOT NULL;
ALTER TABLE "boxes_box" ADD COLUMN "last_updated_by_id" integer REFERENCES "auth_user" ("id") NOT NULL;
ALTER TABLE "boxes_box" DROP COLUMN "user_id";