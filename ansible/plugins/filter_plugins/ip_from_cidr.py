from ansible import errors


def do_ip_from_cidr(cidr, ips=None):
    if cidr is None:
        return None

    if cidr.find('/') < 0:
        raise errors.AnsibleFilterError("ip_from_cidr: value is not a cidr: {!s}".format(cidr))
    parts = cidr.split('/')

    mask = int(parts[1])
    cnt = int(mask/8)

    if parts[0].find('.') < 0:
        raise errors.AnsibleFilterError("ip_from_cidr: value is not a cidr: {!s}".format(cidr))

    cidr_ips = parts[0].split('.')

    unmasked = '.'.join(cidr_ips[:cnt])

    if not ips:
        return unmasked

    if isinstance(ips, list):
        if len(ips) > 4 - cnt:
            raise errors.AnsibleFilterError("ip_from_cidr: {!s} IPs provided for the given cidr mask: {!s}.  Only roo for {!s}".format(len(ips), cidr, 4-cnt))
        for i in ips:
            unmasked = '{!s}.{!s}'.format(unmasked, str(i))
        return unmasked

    else:
        return '{!s}.{!s}'.format(unmasked, ips)


class FilterModule(object):
    ''' A filter to join a path '''
    def filters(self):
        return {
            'ip_from_cidr': do_ip_from_cidr
        }
