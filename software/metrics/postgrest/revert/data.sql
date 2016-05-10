-- Revert shortbus-postgrest:data from pg

BEGIN;

DROP TABLE data;

COMMIT;
