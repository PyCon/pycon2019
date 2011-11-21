CREATE TABLE "schedule_track" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(65) NOT NULL
)
;
CREATE TABLE "schedule_session" (
    "id" serial NOT NULL PRIMARY KEY,
    "track_id" integer REFERENCES "schedule_track" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
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
CREATE TABLE "schedule_slot" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100),
    "start" timestamp with time zone NOT NULL,
    "end" timestamp with time zone NOT NULL,
    "kind_id" integer REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "track_id" integer REFERENCES "schedule_track" ("id") DEFERRABLE INITIALLY DEFERRED,
    "session_id" integer REFERENCES "schedule_session" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "schedule_presentation_additional_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "presentation_id" integer NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("presentation_id", "speaker_id")
)
;
CREATE TABLE "schedule_presentation" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "kind_id" integer NOT NULL REFERENCES "conference_presentationkind" ("id") DEFERRABLE INITIALLY DEFERRED,
    "category_id" integer NOT NULL REFERENCES "conference_presentationcategory" ("id") DEFERRABLE INITIALLY DEFERRED,
    "abstract" text NOT NULL,
    "audience_level" integer NOT NULL,
    "duration" integer NOT NULL,
    "submitted" timestamp with time zone NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cancelled" boolean NOT NULL,
    "extreme_pycon" boolean NOT NULL,
    "invited" boolean NOT NULL,
    "_abstract_rendered" text NOT NULL
)
;
ALTER TABLE "schedule_presentation_additional_speakers" ADD CONSTRAINT "presentation_id_refs_id_87e9a6e4" FOREIGN KEY ("presentation_id") REFERENCES "schedule_presentation" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "schedule_plenary_additional_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "plenary_id" integer NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("plenary_id", "speaker_id")
)
;
CREATE TABLE "schedule_plenary" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "speaker_id" integer REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "description" text NOT NULL
)
;
ALTER TABLE "schedule_plenary_additional_speakers" ADD CONSTRAINT "plenary_id_refs_id_e737e1c0" FOREIGN KEY ("plenary_id") REFERENCES "schedule_plenary" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "schedule_recess" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL
)
;
CREATE TABLE "schedule_userbookmark" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "presentation_id" integer NOT NULL REFERENCES "schedule_presentation" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "presentation_id")
)
;
CREATE INDEX "schedule_session_track_id" ON "schedule_session" ("track_id");
CREATE INDEX "schedule_sessionrole_session_id" ON "schedule_sessionrole" ("session_id");
CREATE INDEX "schedule_sessionrole_user_id" ON "schedule_sessionrole" ("user_id");
CREATE INDEX "schedule_slot_kind_id" ON "schedule_slot" ("kind_id");
CREATE INDEX "schedule_slot_track_id" ON "schedule_slot" ("track_id");
CREATE INDEX "schedule_slot_session_id" ON "schedule_slot" ("session_id");
CREATE INDEX "schedule_presentation_kind_id" ON "schedule_presentation" ("kind_id");
CREATE INDEX "schedule_presentation_category_id" ON "schedule_presentation" ("category_id");
CREATE INDEX "schedule_presentation_speaker_id" ON "schedule_presentation" ("speaker_id");
CREATE INDEX "schedule_plenary_speaker_id" ON "schedule_plenary" ("speaker_id");
CREATE INDEX "schedule_userbookmark_user_id" ON "schedule_userbookmark" ("user_id");
CREATE INDEX "schedule_userbookmark_presentation_id" ON "schedule_userbookmark" ("presentation_id");
