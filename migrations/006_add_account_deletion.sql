### New Model: account.AccountDeletion
CREATE TABLE "account_accountdeletion" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL,
    "date_requested" timestamp with time zone NOT NULL,
    "date_expunged" timestamp with time zone
)
;
CREATE INDEX "account_accountdeletion_user_id" ON "account_accountdeletion" ("user_id");
