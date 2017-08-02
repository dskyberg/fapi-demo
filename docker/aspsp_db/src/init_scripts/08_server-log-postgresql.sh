#!/usr/bin/env ash
PGPASSWORD=password psql -v ON_ERROR_STOP=1 --username aspsp --dbname aspsp <<-EOSQL
CREATE TABLE server_log (
  id         SERIAL PRIMARY KEY,
  dtime      TIMESTAMP WITHOUT TIME ZONE,
  trackingid VARCHAR(255),
  loglevel   VARCHAR(8),
  classname  VARCHAR(255),
  partnerid  VARCHAR(255),
  username   VARCHAR(255),
  message    TEXT
);
EOSQL