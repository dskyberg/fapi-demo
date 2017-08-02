from ansible import errors


def convert_volumes(lst, base=None):
    '''
        This routine is specially tailored to convert our service volume
        descriptions into standard docker volume descriptions.  The service
        descriptions are of the form:
            volumes:
                -
                 host: path
                 container: path
        These must be converted to
            - host_path:container_path
    '''
    if lst is None:
        return
    newLst = []
    try:
        base_path = base and "%s/" % base or ''
        for entry in lst:
            mode = 'mode' in entry and ":%s" % entry['mode'] or ''
            newLst.append("%s%s:%s%s" % (base_path, entry['host'], entry['container'], mode))
        return newLst
    except Exception as e:
        raise errors.AnsibleFilterError('convert_volumes plugin error: %s, list=%s, base_path=%s' % (str(e), str(lst), base_path))


class FilterModule(object):
    ''' A filter to convert a datetime string to an epoch time. '''
    def filters(self):
        return {
            'convert_volumes': convert_volumes
        }
