#!/usr/bin/env ash
PGPASSWORD=password psql -v ON_ERROR_STOP=1 --username aspsp --dbname aspsp <<-EOSQL
CREATE TABLE provisioner_log (
  id          SERIAL PRIMARY KEY,
  dtime       TIMESTAMP WITHOUT TIME ZONE,
  loglevel    VARCHAR(8),
  classname   VARCHAR(255),
  message     TEXT,
  channelcode VARCHAR(255)
);
EOSQL