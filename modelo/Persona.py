from abc import ABCMeta, abstractmethod
from persistent import Persistent

class Persona(Persistent):
	''' '''
	__metaclass__ = ABCMeta
	def __init__(self):
		''' '''
		self.nombre = ""
		self.apellido = ""
		self.sexo = ""
		self.fecha_nacimiento = ""