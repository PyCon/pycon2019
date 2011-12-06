ALTER TABLE "sponsors_pro_sponsor" ADD COLUMN "sponsor_logo_id" integer REFERENCES "sponsors_pro_sponsorbenefit" ("id") DEFERRABLE INITIALLY DEFERRED;
