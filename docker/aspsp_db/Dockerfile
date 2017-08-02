ARG POSTGRES_VERSION
FROM postgres:${POSTGRES_VERSION}-alpine

# Add any initialization scripts necessary to the
# /docker-entrypoint-initdb.d folder. The startup
# script will ensure they are executed on first run.
# The scripts are run in sorted order.
COPY .tmp/init_scripts/*.sql /docker-entrypoint-initdb.d/
