from cbircbot2.core.module_handler.irc_plugin import IRCPlugin


class Hello2(IRCPlugin):
	
	def __init__(self):
		IRCPlugin.__init__(self)
		self.register_new_method("hello")
		
		