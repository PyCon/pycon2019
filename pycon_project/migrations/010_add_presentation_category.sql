CREATE TABLE "conference_presentationcategory" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "slug" varchar(50) NOT NULL
);
CREATE INDEX "conference_presentationcategory_slug" ON "conference_presentationcategory" ("slug");
CREATE INDEX "conference_presentationcategory_slug_like" ON "conference_presentationcategory" ("slug" varchar_pattern_ops);


CREATE TABLE "proposals_proposal_categories" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "presentationcategory_id" integer NOT NULL REFERENCES "conference_presentationcategory" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("proposal_id", "presentationcategory_id")
);
