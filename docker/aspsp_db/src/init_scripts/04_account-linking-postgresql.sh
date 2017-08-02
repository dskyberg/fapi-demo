#!/usr/bin/env ash
PGPASSWORD=password psql -v ON_ERROR_STOP=1 --username aspsp --dbname aspsp <<-EOSQL
CREATE TABLE pingfederate_account_link (
  idp_entityid    VARCHAR(256),
  external_userid VARCHAR(256),
  adapter_id      VARCHAR(32),
  local_userid    VARCHAR(256),
  date_created    TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  PRIMARY KEY (idp_entityid, external_userId, adapter_id)
);

CREATE INDEX LOCALUSERIDIDX ON pingfederate_account_link(local_userid);
EOSQL