ALTER TABLE "schedule_presentation" ADD COLUMN "last_updated" timestamp with time zone NOT NULL DEFAULT NOW();
ALTER TABLE "schedule_plenary" ADD COLUMN "last_updated" timestamp with time zone NOT NULL DEFAULT NOW();
