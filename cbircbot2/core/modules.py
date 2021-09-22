import os
import sys
import importlib
from importlib.abc import Loader
from cbircbot2.core.colors import *
from cbircbot2.modules.Users import Users
import traceback
from contextlib import suppress

class IrcModules(object):
    namespace = "cbircbot2.modules."
    module_folder_list = []
    module_instances_list = {}

    def __init__(self, modules, *args, **kwargs):
        """init module list, prepare the file to load instances"""
        self.irc_client = None
        if "client" in kwargs:
            self.irc_client = kwargs['client']
        with open("modules.txt", "r") as fp:
            lines = fp.read()
            self.module_folder_list = [l for l in lines.split("\n")]
            fp.close()

        for mod in self.module_folder_list:
            if mod == "__pycache__" or mod == "":
                continue

            inst = self.create_instance(mod)
            #print ("Loaded Module: {module}".format(module=mod))
            if inst:
                self.module_instances_list[mod.lower()] = inst()
                self.module_instances_list[mod.lower()].start(self.irc_client)

    def get_module_instance(self, name):
        """ get the module instance
            need to suppress  exception
            avoid thread break
            just ignore it
        """
        with suppress(IndexError):
            if name.lower() in self.module_instances_list:
                return self.module_instances_list[name.lower()]

    def create_instance(self, module_name):

        if module_name.find('__pycache__') != -1:
            return None

        instance = None
        module = None
        try:
            instance = importlib.import_module(self.namespace + module_name)
            if not instance:
                return None


            return getattr(instance, module_name)
            #getattr(instance, module_name)
            # instance = __import__(self.namespace + module_name, fromlist=module_name)
            #if instance:
            #    return getattr(instance, module_name)

        except Exception as ex:
            exc_info = sys.exc_info()
            print(BG_RED + COLOR_BLACK + "ERROR: Cannot Instantiate {0} - {1}".format(module, str(ex)) + COLOR_RESET + BG_RESET)
            print(BG_RED + COLOR_BLACK + "Exception: {0} - Line Number {1} - Frame: {2}".format(str(ex), str(exc_info[2].tb_lineno),str(exc_info[2].tb_frame)  ) + COLOR_RESET + BG_RESET)
            print(BG_RED + COLOR_BLACK + "Please Check the Log" + COLOR_RESET + BG_RESET)
            print(BG_RED + COLOR_BLACK + "Exception: {e}".format(e=str(ex)) + COLOR_RESET + BG_RESET)

            return None


    def end_all_modules(self):
        for mod in self.module_instances_list.values():
            mod.end()

    def broadcast_message_all_modules(self, *args, **kwargs):

        for m in self.module_instances_list.values():
            if hasattr(m, "on_message"):
                m.on_message(**kwargs)