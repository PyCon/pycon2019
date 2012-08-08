### New Model: reviews.ReviewAssignment
CREATE TABLE "reviews_reviewassignment" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "origin" integer NOT NULL,
    "assigned_at" timestamp with time zone NOT NULL,
    "opted_out" boolean NOT NULL
)
;
### New Model: reviews.ProposalMessage
CREATE TABLE "reviews_proposalmessage" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "message" text NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL,
    "_message_rendered" text NOT NULL
)
;
### New Model: reviews.Review
CREATE TABLE "reviews_review" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "vote" varchar(2) NOT NULL,
    "comment" text NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL,
    "_comment_rendered" text NOT NULL
)
;
### New Model: reviews.LatestVote
CREATE TABLE "reviews_latestvote" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "vote" varchar(2) NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL,
    UNIQUE ("proposal_id", "user_id")
)
;
### New Model: reviews.ProposalResult
CREATE TABLE "reviews_proposalresult" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL UNIQUE REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
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
### New Model: reviews.Comment
CREATE TABLE "reviews_comment" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "commenter_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "text" text NOT NULL,
    "public" boolean NOT NULL,
    "commented_at" timestamp with time zone NOT NULL,
    "_text_rendered" text NOT NULL
)
;
### New Model: teams.Team_manager_permissions
CREATE TABLE "teams_team_manager_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "team_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("team_id", "permission_id")
)
;
### New Model: teams.Team_permissions
CREATE TABLE "teams_team_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "team_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("team_id", "permission_id")
)
;
### New Model: teams.Team
CREATE TABLE "teams_team" (
    "id" serial NOT NULL PRIMARY KEY,
    "slug" varchar(50) NOT NULL UNIQUE,
    "name" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "access" varchar(20) NOT NULL,
    "created" timestamp with time zone NOT NULL
)
;
ALTER TABLE "teams_team_manager_permissions" ADD CONSTRAINT "team_id_refs_id_630768a2" FOREIGN KEY ("team_id") REFERENCES "teams_team" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "teams_team_permissions" ADD CONSTRAINT "team_id_refs_id_b3c1a9fe" FOREIGN KEY ("team_id") REFERENCES "teams_team" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: teams.Membership
CREATE TABLE "teams_membership" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "team_id" integer NOT NULL REFERENCES "teams_team" ("id") DEFERRABLE INITIALLY DEFERRED,
    "state" varchar(20) NOT NULL,
    "message" text NOT NULL
)
;
CREATE INDEX "reviews_reviewassignment_proposal_id" ON "reviews_reviewassignment" ("proposal_id");
CREATE INDEX "reviews_reviewassignment_user_id" ON "reviews_reviewassignment" ("user_id");
CREATE INDEX "reviews_proposalmessage_proposal_id" ON "reviews_proposalmessage" ("proposal_id");
CREATE INDEX "reviews_proposalmessage_user_id" ON "reviews_proposalmessage" ("user_id");
CREATE INDEX "reviews_review_proposal_id" ON "reviews_review" ("proposal_id");
CREATE INDEX "reviews_review_user_id" ON "reviews_review" ("user_id");
CREATE INDEX "reviews_latestvote_proposal_id" ON "reviews_latestvote" ("proposal_id");
CREATE INDEX "reviews_latestvote_user_id" ON "reviews_latestvote" ("user_id");
CREATE INDEX "reviews_comment_proposal_id" ON "reviews_comment" ("proposal_id");
CREATE INDEX "reviews_comment_commenter_id" ON "reviews_comment" ("commenter_id");
CREATE INDEX "teams_team_manager_permissions_team_id" ON "teams_team_manager_permissions" ("team_id");
CREATE INDEX "teams_team_manager_permissions_permission_id" ON "teams_team_manager_permissions" ("permission_id");
CREATE INDEX "teams_team_permissions_team_id" ON "teams_team_permissions" ("team_id");
CREATE INDEX "teams_team_permissions_permission_id" ON "teams_team_permissions" ("permission_id");
CREATE INDEX "teams_membership_user_id" ON "teams_membership" ("user_id");
CREATE INDEX "teams_membership_team_id" ON "teams_membership" ("team_id");
