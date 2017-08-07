#!/usr/bin/env python3
from glob import glob
from ruamel.yaml import YAML

ROLE_PATH = 'ansible/roles'
TASK_PATH = 'ansible/tasks'
PATH = 'ansible'


class TagLister():
    def __init__(self, path):
        self.path = path
        self.files = []
        self.tags = []
        self.glob = '*/**/*.yml'
        self.recurse = True
        self.yaml = YAML(typ='safe')

        self._list_files()
        self._parse_files()

    def walk_dict(self, d):
            for key, value in d.items():
                if key == 'tags':
                    for item in value:
                        if item not in self.tags:
                            self.tags.append(item)

    def walk_list(self, l):
        for item in l:
            if isinstance(item, list):
                self.walk_list(item)
            elif isinstance(item, dict):
                self.walk_dict(item)

    def _parse_file(self, file):
        with open(file) as f:
            code = self.yaml.load(f.read())
            if isinstance(code, dict):
                self.walk_dict(code)
            elif isinstance(code, list):
                self.walk_list(code)
            else:
                raise Exception('wrong type')

    def _list_files(self):
        self.files = [file for file in glob(self.path + self.glob, recursive=self.recurse)]

    def _parse_files(self):
        for file in self.files:
            self._parse_file(file)

    def show(self):
        print(self.tags)


def main():
    tl = TagLister('ansible')
    tl.show()


if __name__ == '__main__':
    main()