BEGIN;
ALTER TABLE "schedule_slot" DROP COLUMN "event_id";
DROP TABLE "schedule_event";
COMMIT;