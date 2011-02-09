### New Model: schedule.Plenary_additional_speakers
CREATE TABLE "schedule_plenary_additional_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "plenary_id" integer NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("plenary_id", "speaker_id")
)
;
### New Model: schedule.Plenary
CREATE TABLE "schedule_plenary" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "speaker_id" integer REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "description" text NOT NULL
)
;
ALTER TABLE "schedule_plenary_additional_speakers" ADD CONSTRAINT "plenary_id_refs_id_e737e1c0" FOREIGN KEY ("plenary_id") REFERENCES "schedule_plenary" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: schedule.Recess
CREATE TABLE "schedule_recess" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL
)
;
CREATE INDEX "schedule_plenary_additional_speakers_plenary_id" ON "schedule_plenary_additional_speakers" ("plenary_id");
CREATE INDEX "schedule_plenary_additional_speakers_speaker_id" ON "schedule_plenary_additional_speakers" ("speaker_id");
CREATE INDEX "schedule_plenary_speaker_id" ON "schedule_plenary" ("speaker_id");
