### New Model: reviews.NotificationTemplate
CREATE TABLE "reviews_notificationtemplate" (
    "id" serial NOT NULL PRIMARY KEY,
    "label" varchar(100) NOT NULL,
    "subject" varchar(100) NOT NULL,
    "body" text NOT NULL
)
;
### New Model: reviews.ResultNotification
CREATE TABLE "reviews_resultnotification" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "template_id" integer REFERENCES "reviews_notificationtemplate" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timestamp" timestamp with time zone NOT NULL,
    "to_address" varchar(75) NOT NULL,
    "from_address" varchar(75) NOT NULL,
    "subject" varchar(100) NOT NULL,
    "body" text NOT NULL
)
;
CREATE INDEX "reviews_resultnotification_proposal_id" ON "reviews_resultnotification" ("proposal_id");
CREATE INDEX "reviews_resultnotification_template_id" ON "reviews_resultnotification" ("template_id");
