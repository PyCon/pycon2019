BEGIN;

CREATE TABLE "proposals_proposalsessiontype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "start" timestamp with time zone,
    "end" timestamp with time zone,
    "closed" boolean
);

COMMIT;