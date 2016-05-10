-- Deploy shortbus-postgrest:data to pg

BEGIN;

CREATE TABLE data (
  id      SERIAL,
  time    timestamp NOT NULL,
  name    varchar(250) NOT NULL,
  value   real
);

ALTER TABLE data OWNER to anonymous;

COMMIT;
