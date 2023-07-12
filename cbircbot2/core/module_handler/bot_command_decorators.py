import types
from cbircbot2.core.module_handler.irc_plugin import IRCPlugin

def plugin_mode_params(dec):
	def wrapper(*args, **kwargs):
		def repl(f):
			return dec(f, *args, **kwargs)
		return repl
	return wrapper


@plugin_mode_params
def plugin_mode(f, cmd_name, cmd_type, cmd_permission):
	
	#print(cmd_name, cmd_type, cmd_permission)
	print(f)
	def wrapper(*args, **kwargs):
		return f(*args, **kwargs)
	return wrapper


class ModuleRegister(object):
	def __init__(self,f):
		self.f = f
	
	def __call__(self, *args, **kwargs):
		if isinstance(args[0], IRCPlugin) :
			obj = args[0]
		else:
			obj = None
			
		print(obj)
		
		return self.f(*args, **kwargs)
	
	def __get__(self, instance, owner):
		return types.MethodType(self, instance)

class A(IRCPlugin):
	def __init__(self):
		self.a = "A"
		self.b = 1000
		super().__init__()
		
		self.init()
	
	@ModuleRegister
	def test(self, *args, **kwargs):
		pass

if __name__ == "__main__":
	
	a = A()

	
	pass