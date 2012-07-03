### New Model: proposals.SupportingDocument
CREATE TABLE "proposals_supportingdocument" (
    "id" serial NOT NULL PRIMARY KEY,
    "proposal_id" integer NOT NULL REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "uploaded_by_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_at" timestamp with time zone NOT NULL,
    "file" varchar(100) NOT NULL,
    "description" varchar(140) NOT NULL
)
;
CREATE INDEX "proposals_supportingdocument_proposal_id" ON "proposals_supportingdocument" ("proposal_id");
CREATE INDEX "proposals_supportingdocument_uploaded_by_id" ON "proposals_supportingdocument" ("uploaded_by_id");
