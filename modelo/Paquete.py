from abc import ABCMeta

class Paquete(metaclass=ABCMeta):
	''' a '''
	def __init__(self):
		''' a '''
		self.codigo = 0

class PaqueteContacto(Paquete):
	''' '''
	def __init__(self, contacto, agregar=True):
		''' '''
		self.contacto = contacto
		self.agregar = agregar
		self.codigo = 10

class PaqueteConexion(Paquete):
	''' '''
	def __init__(self, nick, password):
		''' '''
		self.codigo = 1
		self.nick = nick
		self.password = password

class PaqueteMensaje(Paquete):
	''' '''
	def __init__(self, mensaje):
		''' '''
		self.mensaje = mensaje
		self.codigo = 2

class PaqueteNotificacion(Paquete):
	''' '''
	def __init__(self, codigo, extra=None):
		''' '''
		self.codigo = codigo
		self.extra = extra

class PaqueteTest(Paquete):
	''' '''
	def __init__(self):
		''' '''
		self.codigo = 99

class PaqueteRegistro(Paquete):
	''' '''
	def __init__(self, datos_usuario):
		''' '''
		self.codigo = 3
		self.datos_usuario = datos_usuario

class PaqueteRespuesta(Paquete):
	''' '''	
	def __init__(self, respuesta, referencia):
		''' '''		
		self.respuesta = respuesta
		self.codigo = 88
		self.referencia = referencia

class PaqueteHistorial(Paquete):
	''' '''
	def __init__(self, historial_usuario):
		''' '''
		self.historial_usuario = historial_usuario
		self.codigo = 55