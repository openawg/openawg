-- Verify shortbus-postgrest:data on pg

BEGIN;

SELECT time
     , name
     , value
  FROM data
 WHERE FALSE;

ROLLBACK;
