#!/usr/bin/env ash
PGPASSWORD=password psql -v ON_ERROR_STOP=1 --username aspsp --dbname aspsp <<-EOSQL
CREATE TABLE pingfederate_oauth_clients(
  client_id 		VARCHAR(256) NOT NULL,
  name 		VARCHAR(128) NOT NULL,
  refresh_rolling 	SMALLINT,
  logo 		VARCHAR(1024),
  hashed_secret 	VARCHAR(64),
  description 	VARCHAR(2048),
  persistent_grant_exp_time SMALLINT,
  persistent_grant_exp_time_unit VARCHAR(1),
  bypass_approval_page	BOOLEAN,
  PRIMARY KEY(client_id),
  CHECK (refresh_rolling in(0,1))
);

CREATE TABLE pingfederate_oauth_clients_ext(
  client_id VARCHAR(256) NOT NULL,
  name VARCHAR(128) NOT NULL,
  value VARCHAR(1024),
  CONSTRAINT fk_client_id
  FOREIGN KEY (client_id)
  REFERENCES pingfederate_oauth_clients(client_id)
  ON DELETE CASCADE
);

CREATE INDEX IDX_CLIENT_ID ON pingfederate_oauth_clients_ext(client_id);
CREATE INDEX IDX_FIELD_NAME ON pingfederate_oauth_clients_ext(name, value);
EOSQL
