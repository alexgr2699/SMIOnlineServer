from abc import ABCMeta

class Paquete(metaclass=ABCMeta):
	''' Clase abstracta Paquete que tendrá un codigo
		el cual sera heredado por todos los hijos
	'''
	def __init__(self):
		self.codigo = 0

class PaqueteActualizacion(Paquete):
	''' Paquete de actualizacion el cual tiene
		un codigo, y los nuevos datos del usuario
	'''
	def __init__(self, datos_usuario):
		self.codigo = 555
		self.datos_usuario = datos_usuario

class PaqueteConexion(Paquete):
	'''Paquete de Conexion el cual tiene un codigo,
		un nick, del que se quiere conectar y su password
	'''
	def __init__(self, nick, password):
		self.codigo = 1
		self.nick = nick
		self.password = password

class PaqueteBusqueda(Paquete):
	'''Paquete de Conexion el cual tiene un codigo,
		un nick, del que se quiere conectar y su password
	'''
	def __init__(self, usuario):
		self.codigo = 707
		self.usuario = usuario

class PaqueteContacto(Paquete):
	'''Paquete de contacto el cual tiene el nombre del
		contacto a agregar, el codigo, y un boolean que
		sera para defiinir si en realidad se quiere agregar o eliminar
	'''
	def __init__(self, contacto, agregar=True):
		self.contacto = contacto
		self.agregar = agregar
		self.codigo = 10

class PaqueteTest(Paquete):
	''' Paquete de test que solo tendra el codigo,
		servira para definir si hay conexion o no
	'''
	def __init__(self):
		self.codigo = 99

class PaqueteMensaje(Paquete):
	''' Clase que corresponde al paquete mensaje que se
		utilizará para la comunicacion de mensajes entre el cliente
		y el servidor, constara de un objeto mensaje y un codigo
	'''
	def __init__(self, mensaje):
		self.mensaje = mensaje
		self.codigo = 2

class PaqueteNotificacion(Paquete):
	''' Clase que corresponde a los paquetes de notificacion,
		los cuales se utilizaran para la comunicacion interna
		del cliente, es decir cuando llegue un mensaje u ocurra alguna
		accion esperada se utilizarán estos paquetes y lo recibira
		el hilo de la notificacion
	'''
	def __init__(self, codigo, extra=None):
		self.codigo = codigo
		self.extra = extra

class PaqueteRegistro(Paquete):
	''' Clase utilizada para el registro de un usuario, contiene el codigo
		del paquete y los datos del usuario, un objeto de tipo Usuario
	'''
	def __init__(self, datos_usuario):
		self.codigo = 3
		self.datos_usuario = datos_usuario

class PaqueteRespuesta(Paquete):
	''' Paquete utilizado para la confirmacion de operaciones de
		agregar contacto, contiene una referencia, una respuesta (True o False)
		que significa si la operacion fue o no exitosa
	'''
	def __init__(self, respuesta, referencia):
		self.respuesta = respuesta
		self.codigo = 88
		self.referencia = referencia

class PaqueteHistorial(Paquete):
	''' Clase que corresponde al paquete del historial del usuario, la cual
		es enviada desde el servidor y recibida por el cliente, que se encargará
		de cargarla en su objeto usuario, contiene el historial y el codigo al que
		corresponde
	'''
	def __init__(self, historial_usuario):
		self.historial_usuario = historial_usuario
		self.codigo = 55
