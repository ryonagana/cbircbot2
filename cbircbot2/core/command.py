from cbircbot2.core.module_base import CMD_NONE

class Command(object):
    def __init__(self, *args, **kwargs):
        self.cmd = ""
        self.prefix = ""
        self.callback = None
        self.description = ""
        self.access = CMD_NONE

        self.load(**kwargs)

    def load(self, **args):

        if "cmd" in args:
            self.cmd = args["cmd"]

        if 'prefix' in args:
            self.cmd = args['prefix']

        if "access" in args:
            self.cmd = args['access']

        if "callback" in args:
            self.cmd = args['callback']

        if "description" in args:
            self.cmd = args["description"]
