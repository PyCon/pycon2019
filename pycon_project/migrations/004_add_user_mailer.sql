BEGIN;
### New Model: user_mailer.EmailTemplate
CREATE TABLE "user_mailer_emailtemplate" (
    "id" serial NOT NULL PRIMARY KEY,
    "label" varchar(100) NOT NULL,
    "subject" text NOT NULL,
    "body" text NOT NULL
)
;
### New Model: user_mailer.Campaign
CREATE TABLE "user_mailer_campaign" (
    "id" serial NOT NULL PRIMARY KEY,
    "from_address" varchar(150) NOT NULL,
    "email_template_id" integer NOT NULL REFERENCES "user_mailer_emailtemplate" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_list" varchar(50) NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "sent" timestamp with time zone
)
;
COMMIT;
CREATE INDEX "user_mailer_campaign_email_template_id" ON "user_mailer_campaign" ("email_template_id");
COMMIT;