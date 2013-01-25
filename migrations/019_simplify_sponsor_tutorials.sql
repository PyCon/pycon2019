DROP TABLE "pycon_pyconsponsortutorialproposal";
COMMIT;

BEGIN;
### New Model: pycon.PyConSponsorTutorialProposal
CREATE TABLE "pycon_pyconsponsortutorialproposal" (
    "proposalbase_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "proposals_proposalbase" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
