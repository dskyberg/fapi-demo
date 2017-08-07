#!/usr/bin/env python3
import os
import sys
from subprocess import run
import json
import argparse
from scripts.list_tags import TagLister
PLAYBOOKS = [
  'ssl_only',
  'docker_only'
]

DEMO_SERVICES = [

]

class AnsibleCommand(object):
    def __init__(self, playbook='main.yml'):
        self.base_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.playbook = playbook
        self.tags = None
        self.services = None
        self.args = None
        self._buildCmd()

    def _buildCmd(self):
        self.cmd = ['ansible-playbook', self.playbook]
        self._addEnv('base_dir', self.base_dir)

    def _addArg(self, opt, key, value=None):
        self.cmd.append('-%s' % opt)
        if value is not None:
            self.cmd.append('%s=%s' % (key, value))
        else:
            self.cmd.append(key)

    def _addEnv(self, key, value):
        self._addArg('e', key, value)

    def _addTags(self):
        if self.tags is not None and len(self.tags) > 0:
            self._addArg('t', ','.join(self.tags))

    def _addServices(self):
        if self.services is not None and len(self.services) > 0:
            self._addEnv('with_services', json.dumps(self.services))
        else:
            self._addEnv('with_services', json.dumps(['all']))

    def run(self):
        os.chdir("%s/ansible" % self.base_dir)
        self._addServices()
        self._addTags()
        if self.args is not None:
            for x in self.args:
                self.cmd.append(x)
        # print(str(self.cmd))
        run(self.cmd)


def main():
    tl = TagLister('ansible')
    parser = argparse.ArgumentParser(description='Build and run the FAPI demo')
    parser.add_argument("-p", "--playbook", default="main", help='The Ansible playbook to run')
    parser.add_argument("-t", "--tag", dest="tags", action="append", choices=tl.tags, help='Determines which tasks in the playbook to execute')
    parser.add_argument('-s', '--service', dest="services", action="append", help='Restrict tasks o specific services')
    args, unknownargs = parser.parse_known_args()

    ansible = AnsibleCommand(playbook='%s.yml' % args.playbook)

    ansible.services = args.services
    ansible.tags = args.tags
    ansible.args = unknownargs
    ansible.run()


if __name__ == "__main__":
    main()