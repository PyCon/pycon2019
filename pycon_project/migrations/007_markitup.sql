-- Proposals
ALTER TABLE "proposals_proposal" DROP COLUMN "abstract_html";
ALTER TABLE "proposals_proposal" ADD COLUMN "_abstract_rendered" text;
ALTER TABLE "proposals_proposal" ADD COLUMN "_additional_notes_rendered" text;

-- Speakers
ALTER TABLE "speakers_speaker" DROP COLUMN "biography_html";
ALTER TABLE "speakers_speaker" ADD COLUMN "_biography_rendered" text;
