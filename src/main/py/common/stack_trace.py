__author__ = 'Amit Mohapatra'

import sys
import traceback


class StackTrace(object):
    @staticmethod
    def get_stack_trace():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        trace_err = ''.join('!! ' + line for line in lines)
        return trace_err
