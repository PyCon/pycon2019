ALTER TABLE "schedule_session_additional_speakers" RENAME TO "schedule_presentation_additional_speakers";
ALTER TABLE "schedule_session" RENAME TO "schedule_presentation";

ALTER INDEX "schedule_session_additional_speakers_session_id_key" RENAME TO "schedule_presentation_additional_speakers_presentation_id_key";
ALTER INDEX "schedule_session_additional_speakers_id_seq" RENAME TO "schedule_presentation_additional_speakers_id_seq";
ALTER INDEX "schedule_session_id_seq" RENAME TO "schedule_presentation_id_seq";
ALTER INDEX "schedule_session_additional_speakers_pkey" RENAME TO "schedule_presentation_additional_speakers_pkey";
ALTER INDEX "schedule_session_pkey" RENAME TO "schedule_presentation_pkey";
ALTER INDEX "schedule_session_additional_speakers_session_id" RENAME TO "schedule_presentation_additional_speakers_session_id";

ALTER TABLE "schedule_presentation" RENAME COLUMN "session_type" TO "presentation_type";
ALTER TABLE "schedule_presentation_additional_speakers" RENAME COLUMN "session_id" TO "presentation_id";

ALTER TABLE "schedule_presentation_additional_speakers" ADD CONSTRAINT "presentation_id_refs_id_87e9a6e4" FOREIGN KEY ("presentation_id") REFERENCES "schedule_presentation" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "schedule_presentation_additional_speakers_presentation_id" ON "schedule_presentation_additional_speakers" ("presentation_id");
CREATE INDEX "schedule_presentation_additional_speakers_speaker_id" ON "schedule_presentation_additional_speakers" ("speaker_id");
CREATE INDEX "schedule_presentation_slot_id" ON "schedule_presentation" ("slot_id");
CREATE INDEX "schedule_presentation_speaker_id" ON "schedule_presentation" ("speaker_id");

CREATE TABLE "schedule_session" (
    "id" serial NOT NULL PRIMARY KEY,
    "track_id" integer REFERENCES "schedule_track" ("id") DEFERRABLE INITIALLY DEFERRED
)
;

ALTER TABLE "schedule_slot" ALTER COLUMN "track_id" DROP NOT NULL;
ALTER TABLE "schedule_slot" ADD COLUMN "session_id" integer REFERENCES "schedule_session" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "schedule_slot" ADD COLUMN "title" varchar(100);