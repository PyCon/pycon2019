BEGIN;

ALTER TABLE "schedule_session" ADD COLUMN "extreme_pycon" BOOLEAN NOT NULL DEFAULT 'f';
ALTER TABLE "schedule_session" ADD COLUMN "invited" BOOLEAN NOT NULL DEFAULT 'f';

COMMIT;