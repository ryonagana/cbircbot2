import sys
from enum import Enum, auto
from typing import Any
from cbircbot2.core.fancy_module_handler import irc_cmd
import importlib

class IRCPermission(Enum):
    """Command types"""
    CMD_NONE = auto()
    CMD_PUBLIC = auto()
    CMD_PRIVATE = auto()
    CMD_BOTH = auto()


class IrcType(Enum):
    """type of modules"""
    MODULE_PUBLIC = auto()
    MODULE_INTERNAL = auto()
    MODULE_THREAD = auto()


class IRCPlugin(object):
    
    name: str = ""
    author: str = ""
    permission = IRCPermission.CMD_NONE
    client:object = None
    registered_cmd = {}
    loaded:bool
    
    def __init__(self):
        pass
    
    def privmsg_send(self, *args, **kwargs):
        pass
    
    def init(self, *args, **kwargs):
        self.client = kwargs.get("client")
        self.name = self.__class__.name
        self.author = "Unknown Author"
        self.loaded = True
        return
    
    def end(self):
        pass
    
    @classmethod
    def register_new_method(cls, cmd: str = None, prefix: str = "?",  permission: IRCPermission = IRCPermission.CMD_NONE, callback: object = None, description: str = ""):
        if not cmd or not callback:
            return
        
        data = {
            'command': cmd,
            'prefix': prefix,
            'permission': permission,
            'callback': callback,
            'description': description
        }
        
        cls.registered_cmd[cmd] = irc_cmd.IrcCmd.register_new_command(**data)
        return
    
    def get_command(self, name):
        cmd = self.registered_cmd[name]
        try:
            yield cmd
        except IndexError as index_error:
            sys.stderr.write(f"Exception: {index_error}")
        
    def execute(self, name, *args, **kwargs):
        cmd = self.get_command(name)
        run_cmd = irc_cmd.IrcCmd(cmd)
        run_cmd.run(*args, **kwargs)
        
