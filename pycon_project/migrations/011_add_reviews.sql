### New Model: review.ReviewAssignment
CREATE TABLE "review_reviewassignment" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "origin" integer NOT NULL,
    "assigned_at" timestamp with time zone NOT NULL,
    "opted_out" boolean NOT NULL
)
;
### New Model: review.ProposalMessage
CREATE TABLE "review_proposalmessage" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "message" text NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL,
    "_message_rendered" text NOT NULL
)
;
### New Model: review.Review
CREATE TABLE "review_review" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "vote" varchar(2) NOT NULL,
    "comment" text NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL,
    "_comment_rendered" text NOT NULL
)
;
### New Model: review.LatestVote
CREATE TABLE "review_latestvote" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "vote" varchar(2) NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL,
    UNIQUE ("proposal_id", "user_id")
)
;
### New Model: review.ProposalResult
CREATE TABLE "review_proposalresult" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL UNIQUE REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "score" numeric(5, 2) NOT NULL,
    "comment_count" integer CHECK ("comment_count" >= 0) NOT NULL,
    "vote_count" integer CHECK ("vote_count" >= 0) NOT NULL,
    "plus_one" integer CHECK ("plus_one" >= 0) NOT NULL,
    "plus_zero" integer CHECK ("plus_zero" >= 0) NOT NULL,
    "minus_zero" integer CHECK ("minus_zero" >= 0) NOT NULL,
    "minus_one" integer CHECK ("minus_one" >= 0) NOT NULL,
    "accepted" boolean
)
;
### New Model: review.Comment
CREATE TABLE "review_comment" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "commenter_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "text" text NOT NULL,
    "public" boolean NOT NULL,
    "commented_at" timestamp with time zone NOT NULL,
    "_text_rendered" text NOT NULL
)
;
CREATE INDEX "review_reviewassignment_proposal_id" ON "review_reviewassignment" ("proposal_id");
CREATE INDEX "review_reviewassignment_user_id" ON "review_reviewassignment" ("user_id");
CREATE INDEX "review_proposalmessage_proposal_id" ON "review_proposalmessage" ("proposal_id");
CREATE INDEX "review_proposalmessage_user_id" ON "review_proposalmessage" ("user_id");
CREATE INDEX "review_review_proposal_id" ON "review_review" ("proposal_id");
CREATE INDEX "review_review_user_id" ON "review_review" ("user_id");
CREATE INDEX "review_latestvote_proposal_id" ON "review_latestvote" ("proposal_id");
CREATE INDEX "review_latestvote_user_id" ON "review_latestvote" ("user_id");
CREATE INDEX "review_comment_proposal_id" ON "review_comment" ("proposal_id");
CREATE INDEX "review_comment_commenter_id" ON "review_comment" ("commenter_id");
