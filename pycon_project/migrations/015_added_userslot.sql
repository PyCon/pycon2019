### New Model: schedule.UserSlot
CREATE TABLE "schedule_userslot" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "slot_id" integer NOT NULL REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "slot_id")
)
;
CREATE INDEX "schedule_userslot_user_id" ON "schedule_userslot" ("user_id");
CREATE INDEX "schedule_userslot_slot_id" ON "schedule_userslot" ("slot_id");
