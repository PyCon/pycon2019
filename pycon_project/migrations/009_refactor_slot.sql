DROP TABLE "schedule_slot" CASCADE;

### New Model: schedule.Track
CREATE TABLE "schedule_track" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(65) NOT NULL
);
### New Model: schedule.Slot
CREATE TABLE "schedule_slot" (
    "id" serial NOT NULL PRIMARY KEY,
    "start" timestamp with time zone NOT NULL,
    "end" timestamp with time zone NOT NULL,
    "kind_id" integer REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "track_id" integer NOT NULL REFERENCES "schedule_track" ("id") DEFERRABLE INITIALLY DEFERRED
);

UPDATE "schedule_session" SET "slot_id" = NULL;

ALTER TABLE "schedule_session" ADD CONSTRAINT "schedule_session_slot_id_fkey" FOREIGN KEY ("slot_id")
    REFERENCES "schedule_slot" ("id") MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;