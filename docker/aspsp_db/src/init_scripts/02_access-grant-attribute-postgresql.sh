#!/usr/bin/env ash
PGPASSWORD=password psql -v ON_ERROR_STOP=1 --username aspsp --dbname aspsp <<-EOSQL
CREATE TABLE pingfederate_access_grant_attr(
    grant_guid           VARCHAR(32) NOT NULL,
    source_type          SMALLINT,
    name                 VARCHAR(256) NOT NULL,
    value                VARCHAR(2048),
    masked               BOOLEAN,
    encrypted            BOOLEAN,
    CONSTRAINT fk_grant_guid
        FOREIGN KEY (grant_guid)
            REFERENCES pingfederate_access_grant(guid)
            ON DELETE CASCADE
);
CREATE INDEX IDX_GRANT_GUID ON pingfederate_access_grant_attr(grant_guid);
EOSQL