import uuid
from ansible import errors


def get_uuid(version):
    if version == 1:
        return uuid.uuid1
    elif version == 2:
        return uuid.uuid2
    elif version == 3:
        return uuid.uuid3
    elif version == 5:
        return uuid.uuid5
    else:
        return uuid.uuid4


def get_namespece(name):
    l_name = name.lower()
    if l_name == 'url':
        return uuid.NAMESPACE_URL
    elif l_name == 'oid':
        return uuid.NAMESPACE_OID
    elif l_name == 'x500':
        return uuid.NAMESPACE_X500
    else:
        return uuid.NAMESPACE_DNS


def get_variant(variant):
    l_variant = variant.lower()
    if l_variant == 'ncs':
        return uuid.reserved_NCS
    elif l_variant == 'microsoft':
        return uuid.RESERVED_MICROSOFT
    else:
        return uuid.RFC_4122


def get_param(dict, attr, default=None):
    if dict:
        return getattr(dict, attr, default)
    else:
        return default


def do_uuid(dummy, **kwargs):
    version = get_param(kwargs, 'version', 4)
    uuid_func = get_uuid(version)

    namespace = get_param(kwargs, 'namespace', 'dns')
    name = get_param(kwargs, 'name')

    if version == 3 or version == 5:
        if name is None:
            raise errors.AnsibleFilterError('uuid plugin error: uuid version %d requires a "name" parameter' % version)
        return uuid_func(namespace, name)
    else:
        return uuid_func()


class FilterModule(object):
    ''' A generic random UUID filter '''
    def filters(self):
        return {
            'uuid': do_uuid
        }
