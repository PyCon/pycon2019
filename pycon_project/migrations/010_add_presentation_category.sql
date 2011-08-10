CREATE TABLE "conference_presentationcategory" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "slug" varchar(50) NOT NULL
);
CREATE INDEX "conference_presentationcategory_slug" ON "conference_presentationcategory" ("slug");
CREATE INDEX "conference_presentationcategory_slug_like" ON "conference_presentationcategory" ("slug" varchar_pattern_ops);

ALTER TABLE "proposals_proposal" ADD COLUMN "category_id" integer NOT NULL REFERENCES "conference_presentationkind" ("id") DEFERRABLE INITIALLY DEFERRED;