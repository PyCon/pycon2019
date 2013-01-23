### New Model: pycon.PyConSponsorTutorialProposal
CREATE TABLE "pycon_pyconsponsortutorialproposal" (
    "proposalbase_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED,
    "category_id" integer NOT NULL REFERENCES "pycon_pyconproposalcategory" ("id") DEFERRABLE INITIALLY DEFERRED,
    "audience_level" integer NOT NULL,
    "recording_release" boolean NOT NULL
)
;
CREATE INDEX "pycon_pyconsponsortutorialproposal_category_id" ON "pycon_pyconsponsortutorialproposal" ("category_id");
