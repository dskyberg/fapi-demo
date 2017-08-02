#!/usr/bin/env bash
HOSTNAME=
set -ex
psql -h "${POSTGRES_HOSTNAME}" -U postgres -c '\x' -f pingfederate.sql