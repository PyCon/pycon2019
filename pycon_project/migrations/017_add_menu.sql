BEGIN;
CREATE TABLE "menu_menuitem" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL UNIQUE,
    "slug" varchar(50) NOT NULL,
    "parent_id" integer,
    "url" varchar(200) NOT NULL,
    "published" boolean NOT NULL,
    "login_required" boolean NOT NULL,
    "lft" integer CHECK ("lft" >= 0) NOT NULL,
    "rght" integer CHECK ("rght" >= 0) NOT NULL,
    "tree_id" integer CHECK ("tree_id" >= 0) NOT NULL,
    "level" integer CHECK ("level" >= 0) NOT NULL
)
;
ALTER TABLE "menu_menuitem" ADD CONSTRAINT "parent_id_refs_id_7697191b" FOREIGN KEY ("parent_id") REFERENCES "menu_menuitem" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "menu_menuitem_slug" ON "menu_menuitem" ("slug");
CREATE INDEX "menu_menuitem_slug_like" ON "menu_menuitem" ("slug" varchar_pattern_ops);
CREATE INDEX "menu_menuitem_parent_id" ON "menu_menuitem" ("parent_id");
CREATE INDEX "menu_menuitem_lft" ON "menu_menuitem" ("lft");
CREATE INDEX "menu_menuitem_rght" ON "menu_menuitem" ("rght");
CREATE INDEX "menu_menuitem_tree_id" ON "menu_menuitem" ("tree_id");
CREATE INDEX "menu_menuitem_level" ON "menu_menuitem" ("level");
COMMIT;
