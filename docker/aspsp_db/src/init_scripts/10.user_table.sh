#!/usr/bin/env bash
function uuid() {
echo $(python - <<-EOL
import uuid
print(uuid.uuid4())
EOL
)
}
function now() {
echo $(python - <<-EOL
from datetime import datetime
import time
print(str(time.mktime(datetime.now().timetuple())))
EOL
)
}

cat <<-EOSQL
USE aspsp;
CREATE TABLE aspsp_users(
    guid                 VARCHAR(32) NOT NULL,
    first_name           VARCHAR(256),
    last_name            VARCHAR(256) NOT NULL,
    email                VARCHAR(256) NOT NULL,
    created              TIMESTAMPZ NOT NULL,
    updated              TIMESTAMPZ NOT NULL,
    PRIMARY KEY (guid)
    );
CREATE INDEX EMAILIDX ON aspsp_users(email);
EOSQL


cat <<-EOSQL
USE ASPSP;
INSERT INTO aspsp_users VALUES
    ('$(uuid)', 'Bob', 'Smith', 'bob.smith@facedin.com', '2001-01-08 04:05:06', '1999-01-08 04:05:06');
INSERT INTO aspsp_users VALUES
    ('$(uuid)', 'Mary', 'Jenkins', 'mary.jenkins@facedin.com', to_timestamp('', ''), to_timestamp($(now)));
INSERT INTO aspsp_users VALUES
    ('$(uuid)', 'Banu', 'Pahlavi', 'banu.pahlavi@facedin.com', to_timestamp($(now)), to_timestamp($(now)));
INSERT INTO aspsp_users VALUES
    ('$(uuid)', 'Farhad', 'Abbasi', 'farhad.abbasi@facedin.com', to_timestamp($(now)), to_timestamp($(now)));
INSERT INTO aspsp_users VALUES
    ('$(uuid)', 'Juan', 'Valdes', 'juan.valdes@facedin.com', to_timestamp($(now)), to_timestamp($(now)));
INSERT INTO aspsp_users VALUES
    ('$(uuid)', 'Maria', 'Santos', 'maria.santos@facedin.com', to_timestamp($(now)), to_timestamp($(now)));
INSERT INTO aspsp_users VALUES
    ('$(uuid)', 'Wei', 'Chen', 'wei.chen@facedin.com', to_timestamp($(now)), to_timestamp($(now)));
INSERT INTO aspsp_users VALUES
    ('$(uuid)', 'Min', 'Liu', 'min.liu@facedin.com', to_timestamp($(now)), to_timestamp($(now)));
EOSQL