#!/usr/bin/env ash
GIT_ORIGIN="https://github.com/dskyberg/aspsp_api.git"
GIT_DIR="node_server"
echo "Starting Alpine Node Container"
cd $APP_HOME


if [ ! -d "${GIT_DIR}" ]; then
    echo "First time run.  Cloning the repo to ${APP_HOME}/${GIT_DIR}"
    git clone "$GIT_ORIGIN" "${GIT_DIR}"
fi;

cd ${GIT_DIR}
yarn install
exec "$@"