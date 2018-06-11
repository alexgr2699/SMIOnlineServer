from abc import ABCMeta
from persistent import Persistent

class Persona(Persistent, metaclass=ABCMeta):
	''' Clase abstracta que corresponde a la persona, contiene los
		datos personales del usuario
	'''	
	def __init__(self, nombre, apellido, sexo, fecha_nacimiento):
		self.nombre = nombre
		self.apellido = apellido
		self.sexo = sexo
		self.fecha_nacimiento = fecha_nacimiento