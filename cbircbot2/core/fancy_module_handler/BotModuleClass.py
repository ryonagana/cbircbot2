from textwrap import wrap
from functools import wraps


def bot_command(method):
    @wraps(method)
    def __impl(self, *method_args, **method_kwargs):
        out = method(self, *method_args, **method_kwargs)
        return f"OUT: {out}" 
    
    return __impl
        

class BotModuleClass(object):
    def __init__(self, *args, **kwargs):
        pass