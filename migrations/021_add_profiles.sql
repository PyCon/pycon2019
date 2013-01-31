### New Model: profile.Profile
CREATE TABLE "profile_profile" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "first_name" varchar(50),
    "last_name" varchar(50),
    "phone" varchar(20)
)
;
