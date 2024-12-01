import io
import sys

def format_exception(exc):
    o = io.StringIO()
    sys.print_exception(exc, o)
    return o.getvalue()