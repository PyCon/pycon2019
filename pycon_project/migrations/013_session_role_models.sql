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
CREATE INDEX "schedule_sessionrole_session_id" ON "schedule_sessionrole" ("session_id");
CREATE INDEX "schedule_sessionrole_user_id" ON "schedule_sessionrole" ("user_id");
