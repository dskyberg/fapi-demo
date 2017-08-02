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
module: print_docker_cmd
author: "David Skyberg <davidskyberg@gmail.com>"
version_added: "2.3"
short_description: Print the docker run or build command from args
description:
    - "This module simply displays what a docker build/run command would be base on inputs "
options:
    args:
        required: true
        description:
            - dict of args from a service file.
    base
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
from ansible.module_utils.basic import AnsibleModule


def getelem(d, name, default=None):
    if name in d:
        return d[name]
    else:
        return default


def do_build(args, base):
    cmd = 'docker build '

    cmd += ' -t {!s}'.format(getelem(args, 'imageName'))

    if 'dockerfile' in args:
        cmd += ' -f {!s}'.format(args['dockerfile'])

    for k, v, in getelem(args, 'build_args', {}).items():
        cmd += " --build-arg {!s}='{!s}'".format(k, v)

    cmd += ' {!s}'.format(base)

    result = {}
    result['changed'] = False
    result['cmd'] = cmd
    return result


def do_run(args, base):
    cmd = 'docker run '

    if 'detach' in args and args['detach'] is True:
        cmd += ' -d'
    else:
        cmd += ' -it'

    if 'rm' not in args or args['rm'] is True:
        cmd += ' --rm'

    cmd += ' --name %s' % args['name']

    for c in getelem(args, 'capabilities', []):
            cmd += ' --cap-add=%s' % c

    for k, v in getelem(args, 'env', {}).items():
        cmd += ' -e %s=%s' % (k, v)

    if 'hostname' in args:
        cmd += ' --hostname %s' % args['hostname']
    if 'dns' in args:
        cmd += ' --dns=%s' % args['dns']

    if 'networks' in args:
        cmd += ' --network=%s' % args['networks'][0]['name']
        cmd += ' --ip=%s' % args['networks'][0]['ipv4_address']

    for p in getelem(args, 'ports', []):
        cmd += ' -p %s:%s' % (p['host'], p['container'])

    for v in getelem(args, 'volumes', []):
        cmd += ' -v %s/%s:%s' % (base, v['host'], v['container'])

    cmd += ' %s' % args['imageName']

    result = {}
    result['changed'] = False
    result['cmd'] = cmd
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cmd=dict(required=True, type='str', choices=['build', 'run']),
            args=dict(required=True, type='dict'),
            base=dict(required=True, type='str')
        )
    )
    cmd = module.params['cmd']
    args = module.params['args']
    base = module.params['base']
    if cmd == 'run':
        result = do_run(args, base)
    else:
        result = do_build(args, base)

    module.exit_json(**result)


if __name__ == "__main__":
    main()