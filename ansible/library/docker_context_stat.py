#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2017, David Skyberg <davidskyberg@gmail.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: docker_context_stat
author: "David Skyberg <davidskyberg@gmail.com>"
version_added: "2.3"
short_description: Test if the docker build context is newer than the image
description:
    - "This module allows you to check the last modified times (stat.st_mtime) of files
       in the context directory for a Docker build, and compare them against a
       given timestamp, such as from docker_image_facts. Thus, the contents of
       the context become a dependency for re-building Docker images "
requirements:
    - python-dateutil
options:
    path:
        required: true
        description:
            - Name of the Docker build context folder. This should be the same as the path option for docker_image.
    base_time
        required: true
        description:
            - The timestamp to compare against. This should come from docker_image_facts.
            - The value can be a str, float, or int.  If it is an str, it is parsed
              using dateutil.parser.
    excludes
        required: false
        description:
            - List of files or folders to exclude.

'''

EXAMPLES = '''
# Test with a time string
- docker_context_stat:
    path: "{{ path_to_yur_build_context }}"
    base_time: "2017-01-01T01:01:01.11111111Z"

# Test with an epoch float value
- docker_context_stat:
    path: "{{ path_to_yur_build_context }}"
    base_time: 1500038682.0

# Test with an epoch int value
- docker_context_stat:
    path: "{{ path_to_yur_build_context }}"
    base_time: 1500038682

# Test with an epoch float value as a string
- docker_context_stat:
    path: "{{ path_to_yur_build_context }}"
    base_time: '1500038682.0'

# Exclude files and folders from test
- docker_context_stat:
    path: "{{ path_to_yur_build_context }}"
    base_time: 1500038682.0
    exclude: ['file.txt', 'subfolder']

# Test a context against an image creation date
- name: "Get Docker image facts"
  docker_image_facts:
    name: "{{ some_image }}"
  register: image_facts

- name: "Check context dates against image date"
  docker_context_stat:
    path: "{{ path_to_yur_build_context }}"
    base_time: "{{ image_facts.images[0].Created }}"

# Test
'''

RETURN = '''
paths:
    description: List of paths that been modified since base_time
    returned: changed or success
    type: list
    sample: ['path1', 'path2']
'''

import sys
import os
from dateutil import parser
from dateutil import tz
from datetime import datetime
import pytz
import time

from stat import S_ISDIR
from ansible.module_utils.basic import AnsibleModule


def check_stat(path, base_time, excludes, results, tested):
    if path in excludes:
        return
    stats = os.stat(path)
    mode = stats.st_mode
    if S_ISDIR(mode):
        for f in os.listdir(path):
            f_path = os.path.join(path, f)
            check_stat(f_path, base_time, excludes, results, tested)
    else:
        if stats.st_mtime > base_time:
            diff = datetime.fromtimestamp(stats.st_mtime) - datetime.fromtimestamp(base_time)
            results.append({path: str(diff)})
        else:
            tested.append({path: str(datetime.fromtimestamp(stats.st_mtime))})


def convert_utc_to_local(utc_epoch, time_zone):
    ltz = pytz.timezone(time_zone)
    utc_dt = datetime.fromtimestamp(utc_epoch).replace(tzinfo=pytz.utc)
    local_dt = utc_dt.astimezone(ltz)
    return time.mktime(local_dt.timetuple())


def get_utc_epoch(utc_time):

    if isinstance(utc_time, float) or isinstance(utc_time, int):
        return utc_time

    if isinstance(utc_time, str):
        try:
            return int(utc_time)
        except Exception:
            pass
        try:
            return float(utc_time)
        except Exception:
            pass
        try:
            d = datetime.strptime(utc_time[:26], "%Y-%m-%dT%H:%M:%S.%f")
            return time.mktime(d.timetuple())
        except ValueError as e:
            return e

    return Exception("utc_time is not an int, float, or str: %s" % type(utc_time))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(required=True, type='path'),
            base_time=dict(required=False),
            time_zone=dict(default='US/Eastern', type='str'),
            excludes=dict(default=[], type='list')
        )
    )
    utc_time = module.params['base_time']
    time_zone = module.params['time_zone']
    excludes = module.params['excludes']
    path = module.params['path']

    result = {}
    failed_paths = []
    tested_paths = []

    result['changed'] = True
    result['time_provided'] = utc_time
    result['path'] = path
    result['excludes'] = excludes
    result['paths'] = []

    if not os.path.isdir(path):
        module.fail_json(name=path, msg='The directory %s does not exist' % path)

    if utc_time is None or utc_time is '':
        result['base_time'] = None
        module.exit_json(**result)

    utc_epoch = get_utc_epoch(utc_time)
    if isinstance(utc_epoch, Exception):
        module.fail_json(msg="docker_context_stat: failed: %s" % str(utc_epoch))
    base_epoch = convert_utc_to_local(utc_epoch, time_zone)
    result['base_time'] = str(datetime.fromtimestamp(base_epoch))

    check_stat(path, base_epoch, excludes, failed_paths, tested_paths)

    result['changed'] = len(failed_paths) > 0
    result['paths'] = failed_paths
    module.exit_json(**result)


if __name__ == "__main__":
    main()