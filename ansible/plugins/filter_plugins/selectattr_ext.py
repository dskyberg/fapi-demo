from ansible import errors


def selectattr_ext(lst, attr, **kwargs):
    '''
        This function filters a list of dicts, based on an attribute of
        the dict.

        If match is None then a simple presence test is conducted on the attribute.

        If match is provided, then the dict is included only if the attr is present
        and the attr value matches the match value.

        If default is set to True, then the presence test is reversed, and the
        dict is included if the attribute is absent.

        Example:
        lst = [
            {'value': 'Empty type value'},
            {'type': 'A', 'value': 'A value'},
            {'type': 'B', 'value': 'B value'}
        ]

        If filter is:
        {{ lst | selectattr_ext('type')}}
        Result is:
        [
            {'type': 'A', 'value': 'A value'},
            {'type': 'B', 'value': 'B value'}
        ]

        If filter is:
        {{ lst | selectattr_ext('type', default=True)}}
        Result is:
        [
            { 'value': 'Empty type value'},
            {'type': 'A', 'value': 'A value'},
            {'type': 'B', 'value': 'B value'}
        ]

        If filter is:
        {{ lst | selectattr_ext('type', match='A')}}
        Result is:
        [
            {'type': 'A', 'value': 'A value'}
        ]

        If filter is:
        {{ lst | selectattr_ext('type', match='A', default='True'}}
        Result is:
        [
            { 'value': 'Empty type value'},
            {'type': 'A', 'value': 'A value'}
        ]
    '''

    if lst is None:
        return
    newLst = []
    value = 'value' in kwargs and kwargs['value'] or None
    default = 'default' in kwargs and kwargs['default'] or False

    try:
        for entry in lst:
            if not isinstance(entry, dict):
                continue
            if attr not in entry:
                if default:
                    newLst.append(entry)
            elif value is None:
                newLst.append(entry)
            elif entry[attr] == value:
                newLst.append(entry)
        return newLst
    except Exception as e:
        raise errors.AnsibleFilterError('selectattr_ext plugin error: %s, attr=%s, kwargs=%s' % (str(e), str(lst), attr, str(kwargs)))


class FilterModule(object):
    ''' A filter to select dicts in a list based on an attribute '''
    def filters(self):
        return {
            'selectattr_ext': selectattr_ext
        }
