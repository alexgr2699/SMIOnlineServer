from .Persona import Persona
from persistent import Persistent
import os

class Contacto(Persona, Persistent):
	''' Clase que representa a un contacto, con sus datos limitados
		nick y estado, el estado representa si esta o no conectado
	'''	
	def __init__(self, nombre="", apellido="", sexo="", fecha_nacimiento=""):
		Persona.__init__(self, nombre, apellido, sexo, fecha_nacimiento)
		self.nick = ""
		self.estado = False

	def __str__(self):
		''' toString de la clase '''
		return self.nick + " " + ("ON" if os.name == 'nt' else "⚫"\
		if self.estado is True else "OFF" if os.name == 'nt' else '⚪') 