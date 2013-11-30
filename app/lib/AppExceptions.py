class ParameterInvalidException(Exception):
	def __init__(self, parameter, message):
		self.parameter = parameter
		self.message = message
	def __str__(self):
		return "parameter(s) '{0}' is invalid: {1}".format(message)

class ParameterMissingException(Exception):
	def __init__(self, provided, expected):
		self.provided = set(provided)
		self.expected = set(expected)
	def __str__(self):
		missing = reduce(lambda x,y: x+', '+y, list(self.expected - self.provided) )
		return "missing parameter(s) '{0}'".format(missing)