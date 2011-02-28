### New Model: schedule.UserBookmark
CREATE TABLE "schedule_userbookmark" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "presentation_id" integer NOT NULL REFERENCES "schedule_presentation" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "presentation_id")
)
;
CREATE INDEX "schedule_userbookmark_user_id" ON "schedule_userbookmark" ("user_id");
CREATE INDEX "schedule_userbookmark_presentation_id" ON "schedule_userbookmark" ("presentation_id");
