
class IrcCmd(object):
	
	command: str = ""
	prefix: str  = "?"
	callback  = None
	description: str = ""
	permissions = None
	
	def __init__(self, *args, **kwargs):
		
		for key in kwargs:
			setattr(self, key, kwargs[key])
	
	def run(self, *args, **kwargs):
		if self.callback:
			self.callback(*args, **kwargs)
			
			
	@staticmethod
	def register_new_command(*args, **kwargs):
		cmd = IrcCmd(*args, **kwargs)
		return cmd