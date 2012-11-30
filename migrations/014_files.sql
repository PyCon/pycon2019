### New Model: cms.File
CREATE TABLE "cms_file" (
    "id" serial NOT NULL PRIMARY KEY,
    "file" varchar(100) NOT NULL,
    "created" timestamp with time zone NOT NULL
)
;
