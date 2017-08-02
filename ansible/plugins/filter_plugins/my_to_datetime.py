from ansible import errors
import dateutil.parser
import time


def my_to_datetime(string, format='%Y-%m-%dT%H:%M:%S.%fZ'):
    try:
        d = dateutil.parser.parse(string)
        return time.mktime(d.timetuple())
    except Exception as e:
        raise errors.AnsibleFilterError('my_to_date plugin error: %s, string=%s' % (str(e), str(string)))


class FilterModule(object):
    ''' A filter to convert a datetime string to an epoch time. '''
    def filters(self):
        return {
            'my_to_datetime': my_to_datetime
        }
