VERSION = (0, 0, 1, '2a0')
PROJECT = 'pieterraform'


def get_version(version=VERSION):
    return '.'.join([str(x) for x in version])
