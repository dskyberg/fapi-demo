from ansible import errors


def list_to_dict(lst, keyname):
    result = {}
    for item in lst:
        try:
            if keyname not in item:
                raise errors.AnsibleFilterError('merge_nv_liss: keyname not found')
            key = item[keyname]
            del item[keyname]
            result[key] = item
        except Exception as err:
            raise errors.AnsibleFilterError('merge_nv_lists failed: list_to_dict: {!r}'.format(err))
    return result


def merge_dicts(d1, d2, replace):
    result = {}
    for key in d1.keys():
        result[key] = d1[key]
    for key in d2.keys():
        if key not in result or replace:
            result[key] = d2[key]
    return result


def dict_to_list(dct, keyname):
    result = []
    for key in dct.keys():
        value = dct[key]
        value[keyname] = key
        result.append(value)
    return result


def do_merge_nv_lists(lst1, lst2, replace=False, keyname='name'):
    if len(lst2) == 0:
        return lst1
    if len(lst1) == 0:
        return lst2

    dict1 = list_to_dict(lst1, keyname)
    dict2 = list_to_dict(lst2, keyname)
    merged = merge_dicts(dict1, dict2, replace)
    return dict_to_list(merged, keyname)


class FilterModule(object):
    ''' A filter to join a path '''
    def filters(self):
        return {
            'merge_nv_lists': do_merge_nv_lists
        }
