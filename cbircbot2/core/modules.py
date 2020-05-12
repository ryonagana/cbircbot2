import os
import sys
import importlib
from importlib.abc import Loader

class IrcModules(object):
    namespace = "cbircbot2.modules."
    module_folder_list = []
    module_instances_list = []
    ROOT_PATH = path = os.path.dirname(sys.modules['__main__'].__file__)
    MODULES_PATH = os.path.join(ROOT_PATH, 'cbircbot2/modules')

    def __init__(self, modules,  *args, **kwargs):
        for (_, d, f) in os.walk(self.MODULES_PATH):
            for folder in d:
                if folder.find('__pycache__') != -1:
                    continue
                self.module_folder_list.append(folder)
                print('-- module: {0} found'.format(folder))

        for mod in self.module_folder_list:
            if mod:
                inst = self.create_instance(mod)

                if inst:
                    self.module_instances_list = {self.module_instances_list.MODULE_NAME : inst}
                    self.module_instances_list[self.module_instances_list.MODULE_NAME].start()


                    pass
                    #self.MOD_INSTANCES.append(inst)

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
            print("ERROR: Cannot Instantiate {0} - {1}".format(module, str(ex)))
            print("Exception: {0} - Line Number {1} - Frame: {2}".format(str(ex), str(exc_info[2].tb_lineno),str(exc_info[2].tb_frame)  ))
            print("Please Check the Log")
            return None


