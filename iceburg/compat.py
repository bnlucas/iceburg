import sys


_version = sys.version_info

is_py2 = (_version[0] == 2)
is_py3 = (_version[0] == 3)


if is_py2:
    string_type = basestring

else:
    string_type = str
