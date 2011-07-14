### New Model: reversion.Revision
CREATE TABLE "reversion_revision" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "user_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "comment" text NOT NULL
)
;
### New Model: reversion.Version
CREATE TABLE "reversion_version" (
    "id" serial NOT NULL PRIMARY KEY,
    "revision_id" integer NOT NULL REFERENCES "reversion_revision" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" text NOT NULL,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "format" varchar(255) NOT NULL,
    "serialized_data" text NOT NULL,
    "object_repr" text NOT NULL,
    "type" smallint CHECK ("type" >= 0) NOT NULL
)
;
CREATE INDEX "reversion_revision_user_id" ON "reversion_revision" ("user_id");
CREATE INDEX "reversion_version_revision_id" ON "reversion_version" ("revision_id");
CREATE INDEX "reversion_version_content_type_id" ON "reversion_version" ("content_type_id");
CREATE INDEX "reversion_version_type" ON "reversion_version" ("type");
