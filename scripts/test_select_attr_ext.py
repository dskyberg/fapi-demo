#!/usr/bin/env python

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

        1. If filter is:
        {{ lst | select_attr_ext('type')}}
        Result is:
        [
            {'type': 'A', 'value': 'A value'},
            {'type': 'B', 'value': 'B value'}
        ]

        2. If filter is:
        {{ lst | select_attr_ext('type', default=True)}}
        Result is:
        [
            { 'value': 'Empty type value'},
            {'type': 'A', 'value': 'A value'},
            {'type': 'B', 'value': 'B value'}
        ]

        3. If filter is:
        {{ lst | select_attr_ext('type', match='A')}}
        Result is:
        [
            {'type': 'A', 'value': 'A value'}
        ]

        4. If filter is:
        {{ lst | select_attr_ext('type', match='A', default='True'}}
        Result is:
        [
            { 'value': 'Empty type value'},
            {'type': 'A', 'value': 'A value'}
        ]
    '''
    if lst is None:
        return
    newLst = []
    match = 'match' in kwargs and kwargs['match'] or None
    default = 'default' in kwargs and kwargs['default'] or False

    for entry in lst:
        if isinstance(entry, dict):
            if attr in entry:
                if match is not None:
                    if type(entry[attr]) == type(match) and entry[attr] is match:
                        newLst.append(entry)
                else:
                    newLst.append(entry)
            elif default:
                newLst.append(entry)

    return newLst


class TestSuite:
    def __init__(self):
        self.tests = 0
        self.failures = 0
        self.passes = 0

    def test(self, label, actual, expected):
        self.tests += 1
        if actual == expected:
            self.passes += 1
        else:
            self.failures += 1
            print('[%s] Failed! ' % label)
            print('\tExpected:', expected)
            print('\tActual:', actual)

    def __str__(self):
        return 'Tests: %d  Passed: %d  Failed: %d' % (self.tests, self.passes, self.failures)


lst = [
    {'type': 'copy', 'src': 'src 1', 'dest': 'dest 1'},
    {'src': 'src 2', 'dest': 'dest 2'},
    {'src': 'src 3', 'dest': 'dest 3'}
]

test_data = [
    {
        'label': 'attr=type, match=None, default=False',
        'attr': 'type',
        'match': None,
        'default': False,
        'result': [
            {'type': 'copy', 'src': 'src 1', 'dest': 'dest 1'}
        ]
    },
    {
        'label': 'attr=type, match=None, default=True',
        'attr': 'type',
        'match': None,
        'default': True,
        'result': [
            {'type': 'copy', 'src': 'src 1', 'dest': 'dest 1'},
            {'src': 'src 2', 'dest': 'dest 2'},
            {'src': 'src 3', 'dest': 'dest 3'}
         ]
    },
    {
        'label': 'attr=type, match="copy", default=False',
        'attr': 'type',
        'match': 'copy',
        'default': False,
        'result': [
            {'type': 'copy', 'src': 'src 1', 'dest': 'dest 1'}
         ]
    },
    {
        'label': 'attr=type, match="copy", default=True',
        'attr': 'type',
        'match': 'copy',
        'default': True,
        'result': [
            {'type': 'copy', 'src': 'src 1', 'dest': 'dest 1'},
            {'src': 'src 2', 'dest': 'dest 2'},
            {'src': 'src 3', 'dest': 'dest 3'}
         ]
    },
    {
        'label': 'attr=type, match="notcopy", default=True',
        'attr': 'type',
        'match': 'notcopy',
        'default': True,
        'result': [
            {'src': 'src 2', 'dest': 'dest 2'},
            {'src': 'src 3', 'dest': 'dest 3'}
         ]
    },
]

tests = TestSuite()
for data in test_data:
    tests.test(data['label'], selectattr_ext(lst, data['attr'], match=data['match'], default=data['default']), data['result'])

#tests.test('attr=type, match=None, default=False', select_attr_ext(lst, 'type'), [{'type': 'A', 'value': 'A value'}, {'type': 'B', 'value': 'B value'}])
#tests.test('attr=type, match=None, default=True', select_attr_ext(lst, 'type', default=True), lst)
#tests.test('attr=type, match="A", default=False', select_attr_ext(lst, 'type', match='A'), [{'type': 'A', 'value': 'A value'}])
#tests.test('attr=type, match="A", default=True', select_attr_ext(lst, 'type', match='A', default=True), [{'value': 'Empty type value'}, {'type': 'A', 'value': 'A value'}])

print(tests)
