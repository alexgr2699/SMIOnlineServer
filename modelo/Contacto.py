from .Persona import *
from persistent import Persistent

class Contacto(Persona, Persistent):
	''' '''
	def __init__(self):
		''' '''
		self.nick = ""
		self.estado = False

	def __str__(self):
		''' '''
		return self.nick + " " + ("[⚫]" if self.estado is True else "[⚪]") 