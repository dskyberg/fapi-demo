from ansible import errors


def parts(elem):
    ''' Split a string that contains an '=' sign. '''
    if elem.find('=') > 0:
        parts = elem.split('=')
        return (parts[0], parts[1])
    else:
        return (elem, None)


def find_value_in_list(lst, value):
    ''' Simple list lookup to find a primative value in a list.'''
    try:
        idx = lst.index(value)
        return lst[idx]
    except ValueError:
        return None


def find_obj_by_value(lst, elem, value):
    ''' Looks in a list of objects for a dict that contains elem,
        and elem as the given value.'''
    for sub in lst:
        if elem in sub and sub[elem] == value:
            return sub
    return None


def find_in_list(lst, elem):
    if lst is None or elem is None:
        return None
    elem, value = parts(elem)
    if value is None:
        return find_value_in_list(lst, elem)
    else:
        return find_obj_by_value(lst, elem, value)


def find_in_dict(target, elem):
    if elem in target:
        return target[elem]
    return None


def get_from_list_or_dict(target, elem):
    if isinstance(target, list):
        return find_in_list(target, elem)
    if isinstance(target, dict):
        return find_in_dict(target, elem)
    return None


def do_getattr(target, path, default=None):

    if target is None:
        raise errors.AnsibleFilterError('getattr: initial list or dict cannot be None')

    if path is None:
        raise errors.AnsibleFilterError('getattr: path cannot be None')

    if not isinstance(path, list):
        paths = [path]
    else:
        paths = path

    for p in paths:
        target = get_from_list_or_dict(target, p)
        if target is None:
            return default
    return target


class FilterModule(object):
    ''' A filter to join a path '''
    def filters(self):
        return {
            'getattr': do_getattr
        }
