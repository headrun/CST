import sys, traceback
from django.core.exceptions import SuspiciousOperation


class SuppressUnreadablePost(object):
    def filter(self, record):
        _, exception, tb = sys.exc_info()
        if isinstance(exception, IOError):
            for _, _, function, _ in traceback.extract_tb(tb):
                if function == '_read_limited':
                    return False
        return True


class SuppressSuspiciousOperation(object):
    def filter(self, record):
        _, exception, tb = sys.exc_info()
        if isinstance(exception, SuspiciousOperation):
            for _, _, function, _ in traceback.extract_tb(tb):
                if function == 'get_host':
                    return False
        return True
