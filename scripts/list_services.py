#!/usr/bin/env python3
import argparse
from glob import glob
from ruamel.yaml import YAML

PATH = 'conf.d/services.d'


def file_from_path(path):
    path_parts = path.split('/')
    name_parts = path_parts[-1:][0].split('.')
    filename = name_parts[-2:][:1][0]
    return filename


def key_from_path(config_path, path):
    filename = file_from_path(path)
    result = []
    path_parts = path.replace(config_path + '/', '').split('/')[:-1]
    for part in path_parts:
        pieces = part.split('.')
        if pieces[-1:][0] == 'd':
            pieces = pieces[:-1]
        result.append(pieces[-1:][0])
    result.append(filename)
    return '_'.join(result)


class ServiceEntry():
    def __init__(self, path, filename, key, name):
        self.path = path
        self.filename = filename
        self.key = key
        self.name = name


class ServiceLister():
    def __init__(self, args):
        self.path = args.path
        self.runnable = args.runnable
        self.verbose = args.verbose

        self.files = []
        self.services = []
        self.glob = '*/**/*.yml'
        self.recurse = True
        self.yaml = YAML(typ='safe')

        self._list_files()
        self._parse_files()

    def _parse_file(self, path):
        with open(path) as f:
            filename = file_from_path(path)
            path_key = key_from_path(self.path, path)
            code = self.yaml.load(f.read())

            # There should only be one entry:
            if len(code.keys()) > 1:
                raise Exception('Service file - {}: Malformed file.  Too many items.', path)
            key = list(code.keys())[0]
            service = code[key]
            if not isinstance(service, dict):
                raise Exception('Wrong type.  Needed dict, but found', type(service))

            runnable = True
            if 'runnable' in service:
                runnable = service['runnable']

            name = 'name' in service and service['name'] or None

            if self.verbose is True:
                if key != name:
                    print('Warning: {}\n\tKey  and "name" value are different: [{}] [{}]'.format(path, key, name))
                if path_key != key:
                    print('Warning: {}\n\tFilename  and key are different: [{}] [{}]'.format(path, path_key, key))

            if name is None:
                raise Exception('Service file - {}: Malformed file.  No name present.', path)

            if self.runnable and runnable is False:
                return

            entry = ServiceEntry(path, filename, key, name)
            self.services.append(entry)

    def _list_files(self):
        self.files = [file for file in glob(self.path + self.glob, recursive=self.recurse)]

    def _parse_files(self):
        for file in self.files:
            self._parse_file(file)

    def show(self):
        for entry in self.services:
            if self.verbose is True:
                print('{}'.format(entry.filename))
                print('\tService Key: {}'.format(entry.key))
                print('\tName: {}'.format(entry.name))
            else:
                print(entry.name)


def main():
    parser = argparse.ArgumentParser(description='Display a list of FAPI Demo services')
    parser.add_argument("-v", "--verbose", default="False", action='store_true', help='Show more info.')
    parser.add_argument("-r", "--runnable", default="False", action='store_true', help='Only show runnable services (ie, not base docker images')
    parser.add_argument("-p", "--path", default=PATH, help='Path to search for service description files')
    args, unknownargs = parser.parse_known_args()

    sl = ServiceLister(args)
    sl.show()


if __name__ == '__main__':
    main()