
class Command(object):
    def __init__(self, *args, **kwargs):
        self.cmd = ""
        self.prefix = ""
        self.callback = None
        self.description = ""
        self.access = 0

        self.load(**kwargs)

    def load(self, **args):

        if "cmd" in args:
            self.cmd = args["cmd"]

        if 'prefix' in args:
            self.prefix = args['prefix']

        if "access" in args:
            self.access = args['access']

        if "callback" in args:
            self.callback = args['callback']

        if "description" in args:
            self.description = args["description"]

    def run(self, *args, **kwargs):
        if self.callback:
            self.callback(*args, **kwargs)

    @staticmethod
    def register(*args, **kwargs):
        c = Command(**kwargs)
        return c
