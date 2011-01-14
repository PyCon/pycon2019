BEGIN;

ALTER TABLE "schedule_session" ALTER COLUMN "slot_id" DROP NOT NULL;

COMMIT;
