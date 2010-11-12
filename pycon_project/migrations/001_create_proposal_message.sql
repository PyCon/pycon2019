BEGIN;
### New Model: review.ProposalMessage
CREATE TABLE "review_proposalmessage" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "message" text NOT NULL,
    "message_html" text NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL
)
;
CREATE INDEX "review_proposalmessage_proposal_id" ON "review_proposalmessage" ("proposal_id");
CREATE INDEX "review_proposalmessage_user_id" ON "review_proposalmessage" ("user_id");
COMMIT;
