
def mkpath(lst, ext=None):
    if lst is None:
        return
    extPart = ext is not None and '' or '.%s' % ext
    return '%s%s' % ('/'.join(lst), extPart)


class FilterModule(object):
    ''' A filter to join a path '''
    def filters(self):
        return {
            'mkpath': mkpath
        }
