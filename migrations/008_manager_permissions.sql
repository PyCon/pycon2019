
CREATE TABLE "teams_team_manager_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "team_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("team_id", "permission_id")
)
;
ALTER TABLE "teams_team_manager_permissions" ADD CONSTRAINT "team_id_refs_id_630768a2" FOREIGN KEY ("team_id") REFERENCES "teams_team" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "teams_team_mananger_permissions_team_id" ON "teams_team_manager_permissions" ("team_id");
CREATE INDEX "teams_team_manager_permissions_permission_id" ON "teams_team_manager_permissions" ("permission_id");
