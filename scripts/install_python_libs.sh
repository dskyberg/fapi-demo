#!/usr/bin/env bash

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
