
def plugin_mode_params(dec):
	def wrapper(*args, **kwargs):
		def repl(f):
			return dec(f, *args, **kwargs)
		return repl
	return wrapper


@plugin_mode_params
def plugin_mode(f, cmd_name, cmd_type, cmd_permission):
	def wrapper(*args, **kwargs):
		return f(*args, **kwargs)
	return wrapper
