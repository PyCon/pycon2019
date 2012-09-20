CREATE TABLE "constance_config" (
    "id" serial NOT NULL PRIMARY KEY,
    "key" varchar(255) NOT NULL UNIQUE,
    "value" text NOT NULL
)
;
