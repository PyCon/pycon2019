### New Model: schedule.Session_slots
CREATE TABLE "schedule_session_slots" (
    "id" serial NOT NULL PRIMARY KEY,
    "session_id" integer NOT NULL,
    "slot_id" integer NOT NULL REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("session_id", "slot_id")
)
;
### New Model: schedule.Session
CREATE TABLE "schedule_session" (
    "id" serial NOT NULL PRIMARY KEY,
    "day_id" integer NOT NULL REFERENCES "schedule_day" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
ALTER TABLE "schedule_session_slots" ADD CONSTRAINT "session_id_refs_id_7ca2a701" FOREIGN KEY ("session_id") REFERENCES "schedule_session" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: schedule.SessionRole
CREATE TABLE "schedule_sessionrole" (
    "id" serial NOT NULL PRIMARY KEY,
    "session_id" integer NOT NULL REFERENCES "schedule_session" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "role" integer NOT NULL,
    "status" boolean,
    "submitted" timestamp with time zone NOT NULL,
    UNIQUE ("session_id", "user_id", "role")
)
;
CREATE INDEX "schedule_session_slots_session_id" ON "schedule_session_slots" ("session_id");
CREATE INDEX "schedule_session_slots_slot_id" ON "schedule_session_slots" ("slot_id");
CREATE INDEX "schedule_session_day_id" ON "schedule_session" ("day_id");
CREATE INDEX "schedule_sessionrole_session_id" ON "schedule_sessionrole" ("session_id");
CREATE INDEX "schedule_sessionrole_user_id" ON "schedule_sessionrole" ("user_id");
