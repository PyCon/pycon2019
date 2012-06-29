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
### New Model: easy_thumbnails.Source
CREATE TABLE "easy_thumbnails_source" (
    "id" serial NOT NULL PRIMARY KEY,
    "storage_hash" varchar(40) NOT NULL,
    "name" varchar(255) NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    UNIQUE ("storage_hash", "name")
)
;
### New Model: easy_thumbnails.Thumbnail
CREATE TABLE "easy_thumbnails_thumbnail" (
    "id" serial NOT NULL PRIMARY KEY,
    "storage_hash" varchar(40) NOT NULL,
    "name" varchar(255) NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "source_id" integer NOT NULL REFERENCES "easy_thumbnails_source" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("storage_hash", "name", "source_id")
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
### New Model: account.SignupCode
CREATE TABLE "account_signupcode" (
    "id" serial NOT NULL PRIMARY KEY,
    "code" varchar(64) NOT NULL UNIQUE,
    "max_uses" integer CHECK ("max_uses" >= 0) NOT NULL,
    "expiry" timestamp with time zone,
    "inviter_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL,
    "notes" text NOT NULL,
    "sent" timestamp with time zone,
    "created" timestamp with time zone NOT NULL,
    "use_count" integer CHECK ("use_count" >= 0) NOT NULL
)
;
### New Model: account.SignupCodeResult
CREATE TABLE "account_signupcoderesult" (
    "id" serial NOT NULL PRIMARY KEY,
    "signup_code_id" integer NOT NULL REFERENCES "account_signupcode" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timestamp" timestamp with time zone NOT NULL
)
;
### New Model: account.EmailAddress
CREATE TABLE "account_emailaddress" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL UNIQUE,
    "verified" boolean NOT NULL,
    "primary" boolean NOT NULL
)
;
### New Model: account.EmailConfirmation
CREATE TABLE "account_emailconfirmation" (
    "id" serial NOT NULL PRIMARY KEY,
    "email_address_id" integer NOT NULL REFERENCES "account_emailaddress" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created" timestamp with time zone NOT NULL,
    "sent" timestamp with time zone,
    "key" varchar(64) NOT NULL UNIQUE
)
;
### New Model: sitetree.Tree
CREATE TABLE "sitetree_tree" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "alias" varchar(80) NOT NULL UNIQUE
)
;
### New Model: sitetree.TreeItem_access_permissions
CREATE TABLE "sitetree_treeitem_access_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "treeitem_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("treeitem_id", "permission_id")
)
;
### New Model: sitetree.TreeItem
CREATE TABLE "sitetree_treeitem" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "hint" varchar(200) NOT NULL,
    "url" varchar(200) NOT NULL,
    "urlaspattern" boolean NOT NULL,
    "tree_id" integer NOT NULL REFERENCES "sitetree_tree" ("id") DEFERRABLE INITIALLY DEFERRED,
    "hidden" boolean NOT NULL,
    "alias" varchar(80),
    "description" text NOT NULL,
    "inmenu" boolean NOT NULL,
    "inbreadcrumbs" boolean NOT NULL,
    "insitetree" boolean NOT NULL,
    "access_loggedin" boolean NOT NULL,
    "access_restricted" boolean NOT NULL,
    "access_perm_type" integer NOT NULL,
    "parent_id" integer,
    "sort_order" integer NOT NULL,
    UNIQUE ("tree_id", "alias")
)
;
ALTER TABLE "sitetree_treeitem_access_permissions" ADD CONSTRAINT "treeitem_id_refs_id_606a90e8" FOREIGN KEY ("treeitem_id") REFERENCES "sitetree_treeitem" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "sitetree_treeitem" ADD CONSTRAINT "parent_id_refs_id_d31ebb6b" FOREIGN KEY ("parent_id") REFERENCES "sitetree_treeitem" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: taggit.Tag
CREATE TABLE "taggit_tag" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "slug" varchar(100) NOT NULL UNIQUE
)
;
### New Model: taggit.TaggedItem
CREATE TABLE "taggit_taggeditem" (
    "id" serial NOT NULL PRIMARY KEY,
    "tag_id" integer NOT NULL REFERENCES "taggit_tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" integer NOT NULL,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
### New Model: reversion.Revision
CREATE TABLE "reversion_revision" (
    "id" serial NOT NULL PRIMARY KEY,
    "manager_slug" varchar(200) NOT NULL,
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
    "object_id_int" integer,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "format" varchar(255) NOT NULL,
    "serialized_data" text NOT NULL,
    "object_repr" text NOT NULL,
    "type" smallint CHECK ("type" >= 0) NOT NULL
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
### New Model: social_auth.UserSocialAuth
CREATE TABLE "social_auth_usersocialauth" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "provider" varchar(32) NOT NULL,
    "uid" varchar(255) NOT NULL,
    "extra_data" text NOT NULL,
    UNIQUE ("provider", "uid")
)
;
### New Model: social_auth.Nonce
CREATE TABLE "social_auth_nonce" (
    "id" serial NOT NULL PRIMARY KEY,
    "server_url" varchar(255) NOT NULL,
    "timestamp" integer NOT NULL,
    "salt" varchar(40) NOT NULL
)
;
### New Model: social_auth.Association
CREATE TABLE "social_auth_association" (
    "id" serial NOT NULL PRIMARY KEY,
    "server_url" varchar(255) NOT NULL,
    "handle" varchar(255) NOT NULL,
    "secret" varchar(255) NOT NULL,
    "issued" integer NOT NULL,
    "lifetime" integer NOT NULL,
    "assoc_type" varchar(64) NOT NULL
)
;
### New Model: conference.Conference
CREATE TABLE "conference_conference" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "start_date" date,
    "end_date" date,
    "timezone" varchar(100) NOT NULL
)
;
### New Model: conference.Section
CREATE TABLE "conference_section" (
    "id" serial NOT NULL PRIMARY KEY,
    "conference_id" integer NOT NULL REFERENCES "conference_conference" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(100) NOT NULL,
    "slug" varchar(50) NOT NULL,
    "start_date" date,
    "end_date" date
)
;
### New Model: cms.Page
CREATE TABLE "cms_page" (
    "id" serial NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "path" varchar(100) NOT NULL UNIQUE,
    "body" text NOT NULL,
    "status" integer NOT NULL,
    "publish_date" timestamp with time zone NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone NOT NULL,
    "_body_rendered" text NOT NULL
)
;
### New Model: boxes.Box
CREATE TABLE "boxes_box" (
    "id" serial NOT NULL PRIMARY KEY,
    "label" varchar(100) NOT NULL,
    "content" text NOT NULL,
    "created_by_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "last_updated_by_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "_content_rendered" text NOT NULL
)
;
### New Model: speakers.Speaker
CREATE TABLE "speakers_speaker" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(100) NOT NULL,
    "biography" text NOT NULL,
    "photo" varchar(100) NOT NULL,
    "twitter_username" varchar(15) NOT NULL,
    "annotation" text NOT NULL,
    "invite_email" varchar(200) UNIQUE,
    "invite_token" varchar(40) NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "sessions_preference" integer,
    "_biography_rendered" text NOT NULL
)
;
### New Model: proposals.ProposalSection
CREATE TABLE "proposals_proposalsection" (
    "id" serial NOT NULL PRIMARY KEY,
    "section_id" integer NOT NULL UNIQUE REFERENCES "conference_section" ("id") DEFERRABLE INITIALLY DEFERRED,
    "start" timestamp with time zone,
    "end" timestamp with time zone,
    "closed" boolean,
    "published" boolean
)
;
### New Model: proposals.ProposalKind
CREATE TABLE "proposals_proposalkind" (
    "id" serial NOT NULL PRIMARY KEY,
    "section_id" integer NOT NULL REFERENCES "conference_section" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(100) NOT NULL,
    "slug" varchar(50) NOT NULL
)
;
### New Model: proposals.ProposalBase_additional_speakers
CREATE TABLE "proposals_proposalbase_additional_speakers" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposalbase_id" integer NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("proposalbase_id", "speaker_id")
)
;
### New Model: proposals.ProposalBase
CREATE TABLE "proposals_proposalbase" (
    "id" serial NOT NULL PRIMARY KEY,
    "kind_id" integer NOT NULL REFERENCES "proposals_proposalkind" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "abstract" text NOT NULL,
    "additional_notes" text NOT NULL,
    "submitted" timestamp with time zone NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cancelled" boolean NOT NULL,
    "_abstract_rendered" text NOT NULL,
    "_additional_notes_rendered" text NOT NULL
)
;
ALTER TABLE "proposals_proposalbase_additional_speakers" ADD CONSTRAINT "proposalbase_id_refs_id_1f7fb018" FOREIGN KEY ("proposalbase_id") REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: pycon.PyConProposalCategory
CREATE TABLE "pycon_pyconproposalcategory" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "slug" varchar(50) NOT NULL
)
;
### New Model: pycon.PyConTalkProposal
CREATE TABLE "pycon_pycontalkproposal" (
    "proposalbase_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "category_id" integer NOT NULL REFERENCES "pycon_pyconproposalcategory" ("id") DEFERRABLE INITIALLY DEFERRED,
    "audience_level" integer NOT NULL,
    "extreme" boolean NOT NULL,
    "duration" integer NOT NULL
)
;
### New Model: pycon.PyConTutorialProposal
CREATE TABLE "pycon_pycontutorialproposal" (
    "proposalbase_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "category_id" integer NOT NULL REFERENCES "pycon_pyconproposalcategory" ("id") DEFERRABLE INITIALLY DEFERRED,
    "audience_level" integer NOT NULL
)
;
### New Model: pycon.PyConPosterProposal
CREATE TABLE "pycon_pyconposterproposal" (
    "proposalbase_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "category_id" integer NOT NULL REFERENCES "pycon_pyconproposalcategory" ("id") DEFERRABLE INITIALLY DEFERRED,
    "audience_level" integer NOT NULL
)
;
### New Model: sponsorship.SponsorLevel
CREATE TABLE "sponsorship_sponsorlevel" (
    "id" serial NOT NULL PRIMARY KEY,
    "conference_id" integer NOT NULL REFERENCES "conference_conference" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(100) NOT NULL,
    "order" integer NOT NULL,
    "cost" integer CHECK ("cost" >= 0) NOT NULL,
    "description" text NOT NULL
)
;
### New Model: sponsorship.Sponsor
CREATE TABLE "sponsorship_sponsor" (
    "id" serial NOT NULL PRIMARY KEY,
    "applicant_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(100) NOT NULL,
    "external_url" varchar(200) NOT NULL,
    "annotation" text NOT NULL,
    "contact_name" varchar(100) NOT NULL,
    "contact_email" varchar(75) NOT NULL,
    "level_id" integer NOT NULL REFERENCES "sponsorship_sponsorlevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "added" timestamp with time zone NOT NULL,
    "active" boolean NOT NULL,
    "sponsor_logo_id" integer
)
;
### New Model: sponsorship.Benefit
CREATE TABLE "sponsorship_benefit" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "type" varchar(10) NOT NULL
)
;
### New Model: sponsorship.BenefitLevel
CREATE TABLE "sponsorship_benefitlevel" (
    "id" serial NOT NULL PRIMARY KEY,
    "benefit_id" integer NOT NULL REFERENCES "sponsorship_benefit" ("id") DEFERRABLE INITIALLY DEFERRED,
    "level_id" integer NOT NULL REFERENCES "sponsorship_sponsorlevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "max_words" integer CHECK ("max_words" >= 0),
    "other_limits" varchar(200) NOT NULL
)
;
### New Model: sponsorship.SponsorBenefit
CREATE TABLE "sponsorship_sponsorbenefit" (
    "id" serial NOT NULL PRIMARY KEY,
    "sponsor_id" integer NOT NULL REFERENCES "sponsorship_sponsor" ("id") DEFERRABLE INITIALLY DEFERRED,
    "benefit_id" integer NOT NULL REFERENCES "sponsorship_benefit" ("id") DEFERRABLE INITIALLY DEFERRED,
    "active" boolean NOT NULL,
    "max_words" integer CHECK ("max_words" >= 0),
    "other_limits" varchar(200) NOT NULL,
    "text" text NOT NULL,
    "upload" varchar(100) NOT NULL
)
;
ALTER TABLE "sponsorship_sponsor" ADD CONSTRAINT "sponsor_logo_id_refs_id_4309b6bb" FOREIGN KEY ("sponsor_logo_id") REFERENCES "sponsorship_sponsorbenefit" ("id") DEFERRABLE INITIALLY DEFERRED;
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
CREATE INDEX "django_session_expire_date" ON "django_session" ("expire_date");
CREATE INDEX "easy_thumbnails_source_storage_hash" ON "easy_thumbnails_source" ("storage_hash");
CREATE INDEX "easy_thumbnails_source_storage_hash_like" ON "easy_thumbnails_source" ("storage_hash" varchar_pattern_ops);
CREATE INDEX "easy_thumbnails_source_name" ON "easy_thumbnails_source" ("name");
CREATE INDEX "easy_thumbnails_source_name_like" ON "easy_thumbnails_source" ("name" varchar_pattern_ops);
CREATE INDEX "easy_thumbnails_thumbnail_storage_hash" ON "easy_thumbnails_thumbnail" ("storage_hash");
CREATE INDEX "easy_thumbnails_thumbnail_storage_hash_like" ON "easy_thumbnails_thumbnail" ("storage_hash" varchar_pattern_ops);
CREATE INDEX "easy_thumbnails_thumbnail_name" ON "easy_thumbnails_thumbnail" ("name");
CREATE INDEX "easy_thumbnails_thumbnail_name_like" ON "easy_thumbnails_thumbnail" ("name" varchar_pattern_ops);
CREATE INDEX "easy_thumbnails_thumbnail_source_id" ON "easy_thumbnails_thumbnail" ("source_id");
CREATE INDEX "account_signupcode_inviter_id" ON "account_signupcode" ("inviter_id");
CREATE INDEX "account_signupcoderesult_signup_code_id" ON "account_signupcoderesult" ("signup_code_id");
CREATE INDEX "account_signupcoderesult_user_id" ON "account_signupcoderesult" ("user_id");
CREATE INDEX "account_emailaddress_user_id" ON "account_emailaddress" ("user_id");
CREATE INDEX "account_emailconfirmation_email_address_id" ON "account_emailconfirmation" ("email_address_id");
CREATE INDEX "sitetree_treeitem_access_permissions_treeitem_id" ON "sitetree_treeitem_access_permissions" ("treeitem_id");
CREATE INDEX "sitetree_treeitem_access_permissions_permission_id" ON "sitetree_treeitem_access_permissions" ("permission_id");
CREATE INDEX "sitetree_treeitem_url" ON "sitetree_treeitem" ("url");
CREATE INDEX "sitetree_treeitem_url_like" ON "sitetree_treeitem" ("url" varchar_pattern_ops);
CREATE INDEX "sitetree_treeitem_urlaspattern" ON "sitetree_treeitem" ("urlaspattern");
CREATE INDEX "sitetree_treeitem_tree_id" ON "sitetree_treeitem" ("tree_id");
CREATE INDEX "sitetree_treeitem_hidden" ON "sitetree_treeitem" ("hidden");
CREATE INDEX "sitetree_treeitem_alias" ON "sitetree_treeitem" ("alias");
CREATE INDEX "sitetree_treeitem_alias_like" ON "sitetree_treeitem" ("alias" varchar_pattern_ops);
CREATE INDEX "sitetree_treeitem_inmenu" ON "sitetree_treeitem" ("inmenu");
CREATE INDEX "sitetree_treeitem_inbreadcrumbs" ON "sitetree_treeitem" ("inbreadcrumbs");
CREATE INDEX "sitetree_treeitem_insitetree" ON "sitetree_treeitem" ("insitetree");
CREATE INDEX "sitetree_treeitem_access_loggedin" ON "sitetree_treeitem" ("access_loggedin");
CREATE INDEX "sitetree_treeitem_access_restricted" ON "sitetree_treeitem" ("access_restricted");
CREATE INDEX "sitetree_treeitem_parent_id" ON "sitetree_treeitem" ("parent_id");
CREATE INDEX "sitetree_treeitem_sort_order" ON "sitetree_treeitem" ("sort_order");
CREATE INDEX "taggit_taggeditem_tag_id" ON "taggit_taggeditem" ("tag_id");
CREATE INDEX "taggit_taggeditem_object_id" ON "taggit_taggeditem" ("object_id");
CREATE INDEX "taggit_taggeditem_content_type_id" ON "taggit_taggeditem" ("content_type_id");
CREATE INDEX "reversion_revision_manager_slug" ON "reversion_revision" ("manager_slug");
CREATE INDEX "reversion_revision_manager_slug_like" ON "reversion_revision" ("manager_slug" varchar_pattern_ops);
CREATE INDEX "reversion_revision_user_id" ON "reversion_revision" ("user_id");
CREATE INDEX "reversion_version_revision_id" ON "reversion_version" ("revision_id");
CREATE INDEX "reversion_version_object_id_int" ON "reversion_version" ("object_id_int");
CREATE INDEX "reversion_version_content_type_id" ON "reversion_version" ("content_type_id");
CREATE INDEX "reversion_version_type" ON "reversion_version" ("type");
CREATE INDEX "biblion_post_slug" ON "biblion_post" ("slug");
CREATE INDEX "biblion_post_slug_like" ON "biblion_post" ("slug" varchar_pattern_ops);
CREATE INDEX "biblion_post_author_id" ON "biblion_post" ("author_id");
CREATE INDEX "biblion_revision_post_id" ON "biblion_revision" ("post_id");
CREATE INDEX "biblion_revision_author_id" ON "biblion_revision" ("author_id");
CREATE INDEX "biblion_image_post_id" ON "biblion_image" ("post_id");
CREATE INDEX "social_auth_usersocialauth_user_id" ON "social_auth_usersocialauth" ("user_id");
CREATE INDEX "conference_section_conference_id" ON "conference_section" ("conference_id");
CREATE INDEX "conference_section_slug" ON "conference_section" ("slug");
CREATE INDEX "conference_section_slug_like" ON "conference_section" ("slug" varchar_pattern_ops);
CREATE INDEX "boxes_box_label" ON "boxes_box" ("label");
CREATE INDEX "boxes_box_label_like" ON "boxes_box" ("label" varchar_pattern_ops);
CREATE INDEX "boxes_box_created_by_id" ON "boxes_box" ("created_by_id");
CREATE INDEX "boxes_box_last_updated_by_id" ON "boxes_box" ("last_updated_by_id");
CREATE INDEX "speakers_speaker_invite_token" ON "speakers_speaker" ("invite_token");
CREATE INDEX "speakers_speaker_invite_token_like" ON "speakers_speaker" ("invite_token" varchar_pattern_ops);
CREATE INDEX "proposals_proposalkind_section_id" ON "proposals_proposalkind" ("section_id");
CREATE INDEX "proposals_proposalkind_slug" ON "proposals_proposalkind" ("slug");
CREATE INDEX "proposals_proposalkind_slug_like" ON "proposals_proposalkind" ("slug" varchar_pattern_ops);
CREATE INDEX "proposals_proposalbase_additional_speakers_proposalbase_id" ON "proposals_proposalbase_additional_speakers" ("proposalbase_id");
CREATE INDEX "proposals_proposalbase_additional_speakers_speaker_id" ON "proposals_proposalbase_additional_speakers" ("speaker_id");
CREATE INDEX "proposals_proposalbase_kind_id" ON "proposals_proposalbase" ("kind_id");
CREATE INDEX "proposals_proposalbase_speaker_id" ON "proposals_proposalbase" ("speaker_id");
CREATE INDEX "pycon_pyconproposalcategory_slug" ON "pycon_pyconproposalcategory" ("slug");
CREATE INDEX "pycon_pyconproposalcategory_slug_like" ON "pycon_pyconproposalcategory" ("slug" varchar_pattern_ops);
CREATE INDEX "pycon_pycontalkproposal_category_id" ON "pycon_pycontalkproposal" ("category_id");
CREATE INDEX "pycon_pycontutorialproposal_category_id" ON "pycon_pycontutorialproposal" ("category_id");
CREATE INDEX "pycon_pyconposterproposal_category_id" ON "pycon_pyconposterproposal" ("category_id");
CREATE INDEX "sponsorship_sponsorlevel_conference_id" ON "sponsorship_sponsorlevel" ("conference_id");
CREATE INDEX "sponsorship_sponsor_applicant_id" ON "sponsorship_sponsor" ("applicant_id");
CREATE INDEX "sponsorship_sponsor_level_id" ON "sponsorship_sponsor" ("level_id");
CREATE INDEX "sponsorship_sponsor_sponsor_logo_id" ON "sponsorship_sponsor" ("sponsor_logo_id");
CREATE INDEX "sponsorship_benefitlevel_benefit_id" ON "sponsorship_benefitlevel" ("benefit_id");
CREATE INDEX "sponsorship_benefitlevel_level_id" ON "sponsorship_benefitlevel" ("level_id");
CREATE INDEX "sponsorship_sponsorbenefit_sponsor_id" ON "sponsorship_sponsorbenefit" ("sponsor_id");
CREATE INDEX "sponsorship_sponsorbenefit_benefit_id" ON "sponsorship_sponsorbenefit" ("benefit_id");
CREATE INDEX "django_openid_useropenidassociation_user_id" ON "django_openid_useropenidassociation" ("user_id");
