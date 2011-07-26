### New Model: conference.PresentationKind
CREATE TABLE "conference_presentationkind" (
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
    "kind_id" integer NOT NULL REFERENCES "conference_presentationkind" ("id") DEFERRABLE INITIALLY DEFERRED,
    "abstract" text NOT NULL,
    "abstract_html" text NOT NULL,
    "audience_level" integer NOT NULL,
    "additional_notes" text NOT NULL,
    "submitted" timestamp with time zone NOT NULL,
    "speaker_id" integer NOT NULL REFERENCES "speakers_speaker" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cancelled" boolean NOT NULL
)
;
ALTER TABLE "proposals_proposal_additional_speakers" ADD CONSTRAINT "proposal_id_refs_id_7972021a" FOREIGN KEY ("proposal_id") REFERENCES "proposals_proposal" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "proposals_proposal_additional_speakers_proposal_id" ON "proposals_proposal_additional_speakers" ("proposal_id");
CREATE INDEX "proposals_proposal_additional_speakers_speaker_id" ON "proposals_proposal_additional_speakers" ("speaker_id");
CREATE INDEX "proposals_proposal_kind_id" ON "proposals_proposal" ("kind_id");
CREATE INDEX "proposals_proposal_speaker_id" ON "proposals_proposal" ("speaker_id");
