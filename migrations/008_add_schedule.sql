### New Model: schedule.Schedule
CREATE TABLE "schedule_schedule" (
    "id" serial NOT NULL PRIMARY KEY,
    "section_id" integer NOT NULL UNIQUE REFERENCES "conference_section" ("id") DEFERRABLE INITIALLY DEFERRED,
    "slug" varchar(50) NOT NULL UNIQUE
)
;
### New Model: schedule.Day
CREATE TABLE "schedule_day" (
    "id" serial NOT NULL PRIMARY KEY,
    "schedule_id" integer NOT NULL REFERENCES "schedule_schedule" ("id") DEFERRABLE INITIALLY DEFERRED,
    "date" date NOT NULL,
    UNIQUE ("schedule_id", "date")
)
;
### New Model: schedule.Room
CREATE TABLE "schedule_room" (
    "id" serial NOT NULL PRIMARY KEY,
    "schedule_id" integer NOT NULL REFERENCES "schedule_schedule" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(65) NOT NULL,
    "order" integer CHECK ("order" >= 0) NOT NULL
)
;
### New Model: schedule.SlotKind
CREATE TABLE "schedule_slotkind" (
    "id" serial NOT NULL PRIMARY KEY,
    "schedule_id" integer NOT NULL REFERENCES "schedule_schedule" ("id") DEFERRABLE INITIALLY DEFERRED,
    "label" varchar(50) NOT NULL
)
;
### New Model: schedule.Slot
CREATE TABLE "schedule_slot" (
    "id" serial NOT NULL PRIMARY KEY,
    "day_id" integer NOT NULL REFERENCES "schedule_day" ("id") DEFERRABLE INITIALLY DEFERRED,
    "kind_id" integer NOT NULL REFERENCES "schedule_slotkind" ("id") DEFERRABLE INITIALLY DEFERRED,
    "start" time NOT NULL,
    "end" time NOT NULL
)
;
### New Model: schedule.SlotRoom
CREATE TABLE "schedule_slotroom" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer NOT NULL REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "room_id" integer NOT NULL REFERENCES "schedule_room" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("slot_id", "room_id")
)
;
### New Model: schedule.Presentation_additional_speakers
CREATE TABLE "schedule_presentation_additional_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "presentation_id" integer NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("presentation_id", "speaker_id")
)
;
### New Model: schedule.Presentation
CREATE TABLE "schedule_presentation" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "abstract" text NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cancelled" boolean NOT NULL,
    "_proposal_id" integer NOT NULL UNIQUE REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "section_id" integer NOT NULL REFERENCES "conference_section" ("id") DEFERRABLE INITIALLY DEFERRED,
    "_description_rendered" text NOT NULL,
    "_abstract_rendered" text NOT NULL
)
;
ALTER TABLE "schedule_presentation_additional_speakers" ADD CONSTRAINT "presentation_id_refs_id_87e9a6e4" FOREIGN KEY ("presentation_id") REFERENCES "schedule_presentation" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "schedule_day_schedule_id" ON "schedule_day" ("schedule_id");
CREATE INDEX "schedule_room_schedule_id" ON "schedule_room" ("schedule_id");
CREATE INDEX "schedule_slotkind_schedule_id" ON "schedule_slotkind" ("schedule_id");
CREATE INDEX "schedule_slot_day_id" ON "schedule_slot" ("day_id");
CREATE INDEX "schedule_slot_kind_id" ON "schedule_slot" ("kind_id");
CREATE INDEX "schedule_slotroom_slot_id" ON "schedule_slotroom" ("slot_id");
CREATE INDEX "schedule_slotroom_room_id" ON "schedule_slotroom" ("room_id");
CREATE INDEX "schedule_presentation_additional_speakers_presentation_id" ON "schedule_presentation_additional_speakers" ("presentation_id");
CREATE INDEX "schedule_presentation_additional_speakers_speaker_id" ON "schedule_presentation_additional_speakers" ("speaker_id");
CREATE INDEX "schedule_presentation_speaker_id" ON "schedule_presentation" ("speaker_id");
CREATE INDEX "schedule_presentation_section_id" ON "schedule_presentation" ("section_id");
