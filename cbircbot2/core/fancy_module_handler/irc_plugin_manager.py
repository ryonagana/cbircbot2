import importlib
import sys
import os
from cbircbot2.core.colors import *
from dataclasses import dataclass
from cbircbot2.core.fancy_module_handler.irc_plugin import IRCPlugin


@dataclass
class PluginInstance:
	name: str
	path: str
	instance: object


class IRCPluginManager(object):
	
	namespace: str = "cbircbot2.modules."
	module_list = {}
	module_file: str = "modules.txt"
	irc = None
	
	def __init__(self, irc):
		self.irc = irc

	def create_plugin_instance(self, plugin_name: str):
		
		try:
			instance: object = importlib.import_module(f"{self.namespace}{plugin_name}", plugin_name)
			if not instance:
				return None
			
			return getattr(instance, plugin_name)
			
		except Exception as ex:
			exc_info = sys.exc_info()
			print(BG_RED + COLOR_BLACK + "ERROR: Cannot Instantiate {0} - {1}".format(plugin_name, str(ex)) + COLOR_RESET + BG_RESET)
			print(BG_RED + COLOR_BLACK + "Exception: {0} - Line Number {1} - Frame: {2}".format(str(ex), str(exc_info[2].tb_lineno), str(exc_info[2].tb_frame)) + COLOR_RESET + BG_RESET)
			print(BG_RED + COLOR_BLACK + "Please Check the Log" + COLOR_RESET + BG_RESET)
			print(BG_RED + COLOR_BLACK + "Exception: {e}".format(e=str(ex)) + COLOR_RESET + BG_RESET)
		
	def load(self):
		with open(self.module_file, "r") as fp:
			lines = fp.read()
			for line in lines.split("\n"):
				if line.startswith("#") or line.startswith(";") or not line:
					continue
					
				root_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
				folder = root_folder + f"/cbircbot2/modules/" + line
				inst = self.create_plugin_instance(line)
				
				if not inst:
					continue
				
				plugin_instance = PluginInstance(line, folder, inst())
				plugin_instance.instance.init()
				self.module_list[line] = plugin_instance

	def get_plugin(self, name: str):
		if name.lower() not in self.module_list:
			return None
		return self.module_list[name.lower()]
	
	def broadcast_message(self, *args, **kwargs):
		
		for mod in self.module_list.values():
			module: IRCPlugin = mod
			data = kwargs.get("message")
			module.privmsg_send(message=data)
	
			
			
	
	def issue_command(self, *args, **kwargs):
		
		
		for mod in self.module_list.items():
			for cmd in mod[1].instance.registered_cmd.items():
				if cmd.name == kwargs.get("command"):
					cmd_exec: IRCPlugin = yield cmd
					cmd_exec.execute(**kwargs)
			
			
		
		
		
		"""
		for m in self.module_list.items():
			if m[0] == kwargs.get("module"):
				mod = yield m
				instance:IRCPlugin = mod[1]
				instance.execute(**kwargs)
		"""