### New Model: schedule.Plenary
CREATE TABLE "schedule_plenary" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL
)
;
### New Model: schedule.Recess
CREATE TABLE "schedule_recess" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL
)
;