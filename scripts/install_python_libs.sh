#!/usr/bin/env bash

# Do Brew based installs for OS X

# Create the local python VirtualEnv folder and activate it
usr/bin/env python3 /usr/local/lib/python3.5/site-packages/virtualenv.py venv
. ./venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install --upgrade pyopenssl
pip install --upgrade ruamel.yaml
pip install --upgrade docker
pip install --upgrade ansible
pip install --upgrade python-dateutil
pip install --upgrade pytz
pip install --upgrade psycopg2
pip install --upgrade uuid
pip install --upgrade netaddr
pip install --upgrade jmespath

echo "Everything is installed"
echo "Remember to do '. venv/bin/activate'"