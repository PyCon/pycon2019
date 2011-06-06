### New Model: admin.LogEntry
CREATE TABLE "django_admin_log" (
    "id" serial NOT NULL PRIMARY KEY,
    "action_time" timestamp with time zone NOT NULL,
    "user_id" integer NOT NULL,
    "content_type_id" integer,
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint CHECK ("action_flag" >= 0) NOT NULL,
    "change_message" text NOT NULL
)
;
### New Model: auth.Permission
CREATE TABLE "auth_permission" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
)
;
### New Model: auth.Group_permissions
CREATE TABLE "auth_group_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("group_id", "permission_id")
)
;
### New Model: auth.Group
CREATE TABLE "auth_group" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
)
;
ALTER TABLE "auth_group_permissions" ADD CONSTRAINT "group_id_refs_id_3cea63fe" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: auth.User_user_permissions
CREATE TABLE "auth_user_user_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "permission_id")
)
;
### New Model: auth.User_groups
CREATE TABLE "auth_user_groups" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "group_id")
)
;
### New Model: auth.User
CREATE TABLE "auth_user" (
    "id" serial NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" boolean NOT NULL,
    "is_active" boolean NOT NULL,
    "is_superuser" boolean NOT NULL,
    "last_login" timestamp with time zone NOT NULL,
    "date_joined" timestamp with time zone NOT NULL
)
;
ALTER TABLE "django_admin_log" ADD CONSTRAINT "user_id_refs_id_c8665aa" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_user_user_permissions" ADD CONSTRAINT "user_id_refs_id_f2045483" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_user_groups" ADD CONSTRAINT "user_id_refs_id_831107f1" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: auth.Message
CREATE TABLE "auth_message" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "message" text NOT NULL
)
;
### New Model: contenttypes.ContentType
CREATE TABLE "django_content_type" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
)
;
ALTER TABLE "django_admin_log" ADD CONSTRAINT "content_type_id_refs_id_288599e6" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_permission" ADD CONSTRAINT "content_type_id_refs_id_728de91f" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: sessions.Session
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" timestamp with time zone NOT NULL
)
;
### New Model: sites.Site
CREATE TABLE "django_site" (
    "id" serial NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
)
;
### New Model: mailer.Message
CREATE TABLE "mailer_message" (
    "id" serial NOT NULL PRIMARY KEY,
    "message_data" text NOT NULL,
    "when_added" timestamp with time zone NOT NULL,
    "priority" varchar(1) NOT NULL
)
;
### New Model: mailer.DontSendEntry
CREATE TABLE "mailer_dontsendentry" (
    "id" serial NOT NULL PRIMARY KEY,
    "to_address" varchar(75) NOT NULL,
    "when_added" timestamp with time zone NOT NULL
)
;
### New Model: mailer.MessageLog
CREATE TABLE "mailer_messagelog" (
    "id" serial NOT NULL PRIMARY KEY,
    "message_data" text NOT NULL,
    "when_added" timestamp with time zone NOT NULL,
    "priority" varchar(1) NOT NULL,
    "when_attempted" timestamp with time zone NOT NULL,
    "result" varchar(1) NOT NULL,
    "log_message" text NOT NULL
)
;
### New Model: emailconfirmation.EmailAddress
CREATE TABLE "emailconfirmation_emailaddress" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL,
    "verified" boolean NOT NULL,
    "primary" boolean NOT NULL,
    UNIQUE ("user_id", "email")
)
;
### New Model: emailconfirmation.EmailConfirmation
CREATE TABLE "emailconfirmation_emailconfirmation" (
    "id" serial NOT NULL PRIMARY KEY,
    "email_address_id" integer NOT NULL REFERENCES "emailconfirmation_emailaddress" ("id") DEFERRABLE INITIALLY DEFERRED,
    "sent" timestamp with time zone NOT NULL,
    "confirmation_key" varchar(40) NOT NULL
)
;
### New Model: wakawaka.WikiPage
CREATE TABLE "wakawaka_wikipage" (
    "id" serial NOT NULL PRIMARY KEY,
    "slug" varchar(255) NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "content_type_id" integer REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" integer CHECK ("object_id" >= 0)
)
;
### New Model: wakawaka.Revision
CREATE TABLE "wakawaka_revision" (
    "id" serial NOT NULL PRIMARY KEY,
    "page_id" integer NOT NULL REFERENCES "wakawaka_wikipage" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content" text NOT NULL,
    "message" text NOT NULL,
    "creator_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "creator_ip" inet NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL
)
;
### New Model: biblion.Post
CREATE TABLE "biblion_post" (
    "id" serial NOT NULL PRIMARY KEY,
    "section" integer NOT NULL,
    "title" varchar(90) NOT NULL,
    "slug" varchar(50) NOT NULL,
    "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "teaser_html" text NOT NULL,
    "content_html" text NOT NULL,
    "tweet_text" varchar(140) NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone,
    "published" timestamp with time zone,
    "view_count" integer NOT NULL
)
;
### New Model: biblion.Revision
CREATE TABLE "biblion_revision" (
    "id" serial NOT NULL PRIMARY KEY,
    "post_id" integer NOT NULL REFERENCES "biblion_post" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(90) NOT NULL,
    "teaser" text NOT NULL,
    "content" text NOT NULL,
    "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "updated" timestamp with time zone NOT NULL,
    "published" timestamp with time zone,
    "view_count" integer NOT NULL
)
;
### New Model: biblion.Image
CREATE TABLE "biblion_image" (
    "id" serial NOT NULL PRIMARY KEY,
    "post_id" integer NOT NULL REFERENCES "biblion_post" ("id") DEFERRABLE INITIALLY DEFERRED,
    "image_path" varchar(100) NOT NULL,
    "url" varchar(150) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL
)
;
### New Model: biblion.FeedHit
CREATE TABLE "biblion_feedhit" (
    "id" serial NOT NULL PRIMARY KEY,
    "request_data" text NOT NULL,
    "created" timestamp with time zone NOT NULL
)
;
### New Model: waitinglist.WaitingListEntry
CREATE TABLE "waitinglist_waitinglistentry" (
    "id" serial NOT NULL PRIMARY KEY,
    "email" varchar(75) NOT NULL UNIQUE,
    "created" timestamp with time zone NOT NULL
)
;
### New Model: account.Account
CREATE TABLE "account_account" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timezone" varchar(100) NOT NULL,
    "language" varchar(10) NOT NULL
)
;
### New Model: account.OtherServiceInfo
CREATE TABLE "account_otherserviceinfo" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "key" varchar(50) NOT NULL,
    "value" text NOT NULL,
    UNIQUE ("user_id", "key")
)
;
### New Model: account.PasswordReset
CREATE TABLE "account_passwordreset" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "temp_key" varchar(100) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    "reset" boolean NOT NULL
)
;
### New Model: speakers.Speaker
CREATE TABLE "speakers_speaker" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(100) NOT NULL,
    "biography" text NOT NULL,
    "biography_html" text NOT NULL,
    "photo" varchar(100) NOT NULL,
    "twitter_username" varchar(15) NOT NULL,
    "annotation" text NOT NULL,
    "invite_email" varchar(200) UNIQUE,
    "invite_token" varchar(40) NOT NULL,
    "created" timestamp with time zone NOT NULL
)
;
### New Model: proposals.ProposalSessionType
CREATE TABLE "proposals_proposalsessiontype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "start" timestamp with time zone,
    "end" timestamp with time zone,
    "closed" boolean
)
;
### New Model: proposals.Proposal_additional_speakers
CREATE TABLE "proposals_proposal_additional_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("proposal_id", "speaker_id")
)
;
### New Model: proposals.Proposal
CREATE TABLE "proposals_proposal" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "session_type" integer NOT NULL,
    "classification" integer NOT NULL,
    "abstract" text NOT NULL,
    "abstract_html" text NOT NULL,
    "audience_level" integer NOT NULL,
    "additional_notes" text NOT NULL,
    "submitted" timestamp with time zone NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cancelled" boolean NOT NULL,
    "recording" boolean NOT NULL,
    "opt_out_ads" boolean,
    "extreme_pycon" boolean NOT NULL,
    "invited" boolean NOT NULL
)
;
ALTER TABLE "proposals_proposal_additional_speakers" ADD CONSTRAINT "proposal_id_refs_id_7972021a" FOREIGN KEY ("proposal_id") REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: sponsors.SponsorLevel
CREATE TABLE "sponsors_sponsorlevel" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "order" integer NOT NULL,
    "cost" integer CHECK ("cost" >= 0) NOT NULL,
    "description" text NOT NULL
)
;
### New Model: sponsors.Sponsor
CREATE TABLE "sponsors_sponsor" (
    "id" serial NOT NULL PRIMARY KEY,
    "applicant_id" integer UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(100) NOT NULL,
    "external_url" varchar(200) NOT NULL,
    "annotation" text NOT NULL,
    "contact_name" varchar(100) NOT NULL,
    "contact_email" varchar(75) NOT NULL,
    "level_id" integer REFERENCES "sponsors_sponsorlevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "added" timestamp with time zone NOT NULL,
    "active" boolean
)
;
### New Model: sponsors.Benefit
CREATE TABLE "sponsors_benefit" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "type" varchar(10) NOT NULL
)
;
### New Model: sponsors.BenefitLevel
CREATE TABLE "sponsors_benefitlevel" (
    "id" serial NOT NULL PRIMARY KEY,
    "benefit_id" integer NOT NULL REFERENCES "sponsors_benefit" ("id") DEFERRABLE INITIALLY DEFERRED,
    "level_id" integer NOT NULL REFERENCES "sponsors_sponsorlevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "max_words" integer CHECK ("max_words" >= 0),
    "other_limits" varchar(200) NOT NULL
)
;
### New Model: sponsors.SponsorBenefit
CREATE TABLE "sponsors_sponsorbenefit" (
    "id" serial NOT NULL PRIMARY KEY,
    "sponsor_id" integer NOT NULL REFERENCES "sponsors_sponsor" ("id") DEFERRABLE INITIALLY DEFERRED,
    "benefit_id" integer NOT NULL REFERENCES "sponsors_benefit" ("id") DEFERRABLE INITIALLY DEFERRED,
    "active" boolean NOT NULL,
    "max_words" integer CHECK ("max_words" >= 0),
    "other_limits" varchar(200) NOT NULL,
    "text" text NOT NULL,
    "upload" varchar(100) NOT NULL
)
;
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
    "message_html" text NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL
)
;
### New Model: review.Review
CREATE TABLE "review_review" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "vote" varchar(2) NOT NULL,
    "comment" text NOT NULL,
    "comment_html" text NOT NULL,
    "submitted_at" timestamp with time zone NOT NULL
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
    "commented_at" timestamp with time zone NOT NULL
)
;
### New Model: boxes.Box
CREATE TABLE "boxes_box" (
    "id" serial NOT NULL PRIMARY KEY,
    "label" varchar(100) NOT NULL,
    "user_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content" text NOT NULL,
    UNIQUE ("label", "user_id")
)
;
### New Model: schedule.Track
CREATE TABLE "schedule_track" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(65) NOT NULL
)
;
### New Model: schedule.Session
CREATE TABLE "schedule_session" (
    "id" serial NOT NULL PRIMARY KEY,
    "track_id" integer REFERENCES "schedule_track" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
### New Model: schedule.SessionRole
CREATE TABLE "schedule_sessionrole" (
    "id" serial NOT NULL PRIMARY KEY,
    "session_id" integer NOT NULL REFERENCES "schedule_session" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "role" integer NOT NULL,
    "status" boolean,
    "submitted" timestamp with time zone NOT NULL,
    UNIQUE ("session_id", "user_id", "role")
)
;
### New Model: schedule.Slot
CREATE TABLE "schedule_slot" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100),
    "start" timestamp with time zone NOT NULL,
    "end" timestamp with time zone NOT NULL,
    "kind_id" integer REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "track_id" integer REFERENCES "schedule_track" ("id") DEFERRABLE INITIALLY DEFERRED,
    "session_id" integer REFERENCES "schedule_session" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
### New Model: schedule.Presentation_additional_speakers
CREATE TABLE "schedule_presentation_additional_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "presentation_id" integer NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("presentation_id", "speaker_id")
)
;
### New Model: schedule.Presentation
CREATE TABLE "schedule_presentation" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "presentation_type" integer NOT NULL,
    "abstract" text NOT NULL,
    "abstract_html" text NOT NULL,
    "audience_level" integer NOT NULL,
    "submitted" timestamp with time zone NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cancelled" boolean NOT NULL,
    "extreme_pycon" boolean NOT NULL,
    "invited" boolean NOT NULL
)
;
ALTER TABLE "schedule_presentation_additional_speakers" ADD CONSTRAINT "presentation_id_refs_id_87e9a6e4" FOREIGN KEY ("presentation_id") REFERENCES "schedule_presentation" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: schedule.Plenary_additional_speakers
CREATE TABLE "schedule_plenary_additional_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "plenary_id" integer NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("plenary_id", "speaker_id")
)
;
### New Model: schedule.Plenary
CREATE TABLE "schedule_plenary" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "speaker_id" integer REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "description" text NOT NULL
)
;
ALTER TABLE "schedule_plenary_additional_speakers" ADD CONSTRAINT "plenary_id_refs_id_e737e1c0" FOREIGN KEY ("plenary_id") REFERENCES "schedule_plenary" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: schedule.Recess
CREATE TABLE "schedule_recess" (
    "id" serial NOT NULL PRIMARY KEY,
    "slot_id" integer UNIQUE REFERENCES "schedule_slot" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL
)
;
### New Model: schedule.UserBookmark
CREATE TABLE "schedule_userbookmark" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "presentation_id" integer NOT NULL REFERENCES "schedule_presentation" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "presentation_id")
)
;
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
### New Model: django_openid.Nonce
CREATE TABLE "django_openid_nonce" (
    "id" serial NOT NULL PRIMARY KEY,
    "server_url" varchar(255) NOT NULL,
    "timestamp" integer NOT NULL,
    "salt" varchar(40) NOT NULL
)
;
### New Model: django_openid.Association
CREATE TABLE "django_openid_association" (
    "id" serial NOT NULL PRIMARY KEY,
    "server_url" text NOT NULL,
    "handle" varchar(255) NOT NULL,
    "secret" text NOT NULL,
    "issued" integer NOT NULL,
    "lifetime" integer NOT NULL,
    "assoc_type" text NOT NULL
)
;
### New Model: django_openid.UserOpenidAssociation
CREATE TABLE "django_openid_useropenidassociation" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "openid" varchar(255) NOT NULL,
    "created" timestamp with time zone NOT NULL
)
;
CREATE INDEX "django_admin_log_user_id" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_content_type_id" ON "django_admin_log" ("content_type_id");
CREATE INDEX "auth_permission_content_type_id" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_group_permissions_group_id" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_user_user_permissions_user_id" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_permission_id" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_groups_user_id" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_group_id" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_message_user_id" ON "auth_message" ("user_id");
CREATE INDEX "emailconfirmation_emailaddress_user_id" ON "emailconfirmation_emailaddress" ("user_id");
CREATE INDEX "emailconfirmation_emailconfirmation_email_address_id" ON "emailconfirmation_emailconfirmation" ("email_address_id");
CREATE INDEX "wakawaka_wikipage_content_type_id" ON "wakawaka_wikipage" ("content_type_id");
CREATE INDEX "wakawaka_revision_page_id" ON "wakawaka_revision" ("page_id");
CREATE INDEX "wakawaka_revision_creator_id" ON "wakawaka_revision" ("creator_id");
CREATE INDEX "biblion_post_slug" ON "biblion_post" ("slug");
CREATE INDEX "biblion_post_slug_like" ON "biblion_post" ("slug" varchar_pattern_ops);
CREATE INDEX "biblion_post_author_id" ON "biblion_post" ("author_id");
CREATE INDEX "biblion_revision_post_id" ON "biblion_revision" ("post_id");
CREATE INDEX "biblion_revision_author_id" ON "biblion_revision" ("author_id");
CREATE INDEX "biblion_image_post_id" ON "biblion_image" ("post_id");
CREATE INDEX "account_otherserviceinfo_user_id" ON "account_otherserviceinfo" ("user_id");
CREATE INDEX "account_passwordreset_user_id" ON "account_passwordreset" ("user_id");
CREATE INDEX "speakers_speaker_invite_token" ON "speakers_speaker" ("invite_token");
CREATE INDEX "speakers_speaker_invite_token_like" ON "speakers_speaker" ("invite_token" varchar_pattern_ops);
CREATE INDEX "proposals_proposal_additional_speakers_proposal_id" ON "proposals_proposal_additional_speakers" ("proposal_id");
CREATE INDEX "proposals_proposal_additional_speakers_speaker_id" ON "proposals_proposal_additional_speakers" ("speaker_id");
CREATE INDEX "proposals_proposal_speaker_id" ON "proposals_proposal" ("speaker_id");
CREATE INDEX "sponsors_sponsor_level_id" ON "sponsors_sponsor" ("level_id");
CREATE INDEX "sponsors_benefitlevel_benefit_id" ON "sponsors_benefitlevel" ("benefit_id");
CREATE INDEX "sponsors_benefitlevel_level_id" ON "sponsors_benefitlevel" ("level_id");
CREATE INDEX "sponsors_sponsorbenefit_sponsor_id" ON "sponsors_sponsorbenefit" ("sponsor_id");
CREATE INDEX "sponsors_sponsorbenefit_benefit_id" ON "sponsors_sponsorbenefit" ("benefit_id");
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
CREATE INDEX "boxes_box_label" ON "boxes_box" ("label");
CREATE INDEX "boxes_box_label_like" ON "boxes_box" ("label" varchar_pattern_ops);
CREATE INDEX "boxes_box_user_id" ON "boxes_box" ("user_id");
CREATE INDEX "schedule_session_track_id" ON "schedule_session" ("track_id");
CREATE INDEX "schedule_sessionrole_session_id" ON "schedule_sessionrole" ("session_id");
CREATE INDEX "schedule_sessionrole_user_id" ON "schedule_sessionrole" ("user_id");
CREATE INDEX "schedule_slot_kind_id" ON "schedule_slot" ("kind_id");
CREATE INDEX "schedule_slot_track_id" ON "schedule_slot" ("track_id");
CREATE INDEX "schedule_slot_session_id" ON "schedule_slot" ("session_id");
CREATE INDEX "schedule_presentation_additional_speakers_presentation_id" ON "schedule_presentation_additional_speakers" ("presentation_id");
CREATE INDEX "schedule_presentation_additional_speakers_speaker_id" ON "schedule_presentation_additional_speakers" ("speaker_id");
CREATE INDEX "schedule_presentation_speaker_id" ON "schedule_presentation" ("speaker_id");
CREATE INDEX "schedule_plenary_additional_speakers_plenary_id" ON "schedule_plenary_additional_speakers" ("plenary_id");
CREATE INDEX "schedule_plenary_additional_speakers_speaker_id" ON "schedule_plenary_additional_speakers" ("speaker_id");
CREATE INDEX "schedule_plenary_speaker_id" ON "schedule_plenary" ("speaker_id");
CREATE INDEX "schedule_userbookmark_user_id" ON "schedule_userbookmark" ("user_id");
CREATE INDEX "schedule_userbookmark_presentation_id" ON "schedule_userbookmark" ("presentation_id");
CREATE INDEX "user_mailer_campaign_email_template_id" ON "user_mailer_campaign" ("email_template_id");
CREATE INDEX "django_openid_useropenidassociation_user_id" ON "django_openid_useropenidassociation" ("user_id");
