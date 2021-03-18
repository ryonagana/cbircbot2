import os
import sys
import importlib
from importlib.abc import Loader
from cbircbot2.core.colors import *
from cbircbot2.modules.Users import Users

class IrcModules(object):
    namespace = "cbircbot2.modules."
    module_folder_list = []
    module_instances_list = {}
    ROOT_PATH = path = os.path.dirname(sys.modules['__main__'].__file__)
    MODULES_PATH = os.path.join(ROOT_PATH, 'cbircbot2/modules')


    def __init__(self, modules, *args, **kwargs):

        self.irc_client = None

        if "client" in kwargs:
            self.irc_client = kwargs['client']

        #self.module_folder_list = [folder for folder in next(os.walk(self.MODULES_PATH))][1]

        with open("modules.txt", "r") as fp:
            lines = fp.read()
            self.module_folder_list = [l for l in lines.split("\n")]
            fp.close()






        for mod in self.module_folder_list:
            if mod == "__pycache__":
                continue

            inst = self.create_instance(mod)
            print ("Loaded Module: {module}".format(module=mod))
            if inst:
                self.module_instances_list[mod] = inst
                self.module_instances_list[mod].start(inst, {'client': self.irc_client})




        """
            inst = self.create_instance(p)
            if inst:
                self.module_instances_list[p] = inst
                self.module_instances_list[p].start(inst, {'client': self.irc_client})
                pass
        """




        """
        for d in next(os.walk(self.MODULES_PATH)):
            for folder in d:
                if folder.find('__pycache__') != -1:
                    continue
                self.module_folder_list.append(folder)
                print('-- module: {0} found'.format(folder))

        for mod in self.module_folder_list:
            if mod:
                inst = self.create_instance(mod)
                if inst:

                    self.module_instances_list[mod] = inst
                    self.module_instances_list[mod].start(inst, {'client': self.irc_client })
                    pass
        """


    def get_module_instance(self, name):
        try:

            if name in self.module_instances_list:
                return self.module_instances_list[name]
            else:
                return None
        except Exception as e:
            print('module not found - {0}'.format(e))
            return None

        return None

    def create_instance(self, module_name):

        if module_name.find('__pycache__') != -1:
            return None

        instance = None
        module = None
        try:
            instance = __import__(self.namespace + module_name, fromlist=module_name)
            if instance:
                return getattr(instance, module_name)

        except Exception as ex:
            exc_info = sys.exc_info()
            print(BG_RED + COLOR_BLACK + "ERROR: Cannot Instantiate {0} - {1}".format(module, str(ex)) + COLOR_RESET + BG_RESET)
            print(BG_RED + COLOR_BLACK + "Exception: {0} - Line Number {1} - Frame: {2}".format(str(ex), str(exc_info[2].tb_lineno),str(exc_info[2].tb_frame)  ) + COLOR_RESET + BG_RESET)
            print(BG_RED + COLOR_BLACK + "Please Check the Log" + COLOR_RESET + BG_RESET)
            print(BG_RED + COLOR_BLACK + "Exception: {e}".format(e=str(ex)) + COLOR_RESET + BG_RESET)

            return None


