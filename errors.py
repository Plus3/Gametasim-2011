
class GametasimError(Exception):
	def __init__(self, value): self.value = value
	def __str__(self): return repr(self.value)

class PlayerError(GametasimError): pass
class FatalError(GametasimError): pass
class ItemError(GametasimError): pass