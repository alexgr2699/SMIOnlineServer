from threading import Thread
from modelo.Paquete import *
from modelo.Usuario import Usuario
from modelo.Contacto import Contacto
from utils import *
import pickle
import transaction

class HiloCliente(Thread):
	'''Hilo del cliente que se ha conectado'''

	def __init__(self, conn, addr, comunicador_notificaciones, hilos_conexiones, modelo):
		''' Inicializador de la clase, recibe todos los demas hilos,
			la conexion a la base de datos, la conexión al servidor,
			el comunicador de notificaciones y crea un diccionario de
			funciones para manejar los paquetes entrantes.
		'''
		Thread.__init__(self)
		self.modelo = modelo
		self.hilos_conexiones = hilos_conexiones
		self.conn = conn
		self.addr = addr
		self.nick = ''
		self.comunicador = comunicador_notificaciones
		self.manejador_codigos_paquete = {
			PAQ_CONEXION: self.realizar_conexion,\
			PAQ_TEST: self.realizar_test,\
			PAQ_MENSAJE: self.enviar_mensaje,\
			PAQ_REGISTRO: self.registrar_usuario,\
			PAQ_CONTACTO: self.agregar_contacto,\
			PAQ_BUSQUEDA: self.buscar_contacto,\
			PAQ_ACTUALIZACION: self.actualizar_perfil,\
		}

	def run(self):
		''' Funcion que inicia el hilo y se pone a la recepcion de paquetes'''
		while True:
			try:
				input_data = self.conn.recv(1024)
				input_data = pickle.loads(input_data)
			except Exception as e:
				# Se lanza cuando un usuario se desconecta o pierde conexion
				# por motivos externos, lo que pasa cuando se lanza esta
				# excepcion es guardar el log de la desconexion y luego
				# informar a sus contactos que el se ha desconectado
				paquete = PaqueteNotificacion(NOTIF_USUARIO_DESCONECTADO, self.addr)
				self.comunicador.put(paquete)
				if self.modelo.verificar_existencia_usuario(self.nick) is False:
					self.modelo.actualizar_estado_usuario(self.nick, False)
					self.enviar_historial_contactos(self.nick,\
						self.modelo.extraer_lista_contactos(self.nick), False)
				break;
			else:
				self.manejador_codigos_paquete[input_data.codigo](input_data)

	def actualizar_perfil(self, paquete):
		paquete_notificacion = PaqueteNotificacion(NOTIF_ACTUALIZACION, self.nick)
		self.comunicador.put(paquete_notificacion)

		res = self.modelo.actualizar_perfil_usuario(self.nick, paquete)
		if res is True:
			paquete_notificacion = PaqueteNotificacion(NOTIF_ACTUALIZACION_EXITO, self.nick)
			self.comunicador.put(paquete_notificacion)
		else:
			paquete_notificacion = PaqueteNotificacion(NOTIF_ACTUALIZACION_ERROR, self.nick)
			self.comunicador.put(paquete_notificacion)

	def buscar_contacto(self, paquete):
		resultado = self.modelo.buscar_contacto(paquete.usuario)
		paquete_resultado = PaqueteBusqueda(resultado)
		paquete_resultado = pickle.dumps(paquete_resultado)
		self.conn.send(paquete_resultado)

	def enviar_historial_contactos(self, usuario, contactos, estado):
		''' Método que avisa a los contactos del usuario que se ha conectado
			o que se ha desconectado, recibe el nombre del usuario en cuestión
			, su lista de contactos y el estado actual del usuario (True = ON)
			(False = Offline)
		'''
		for contacto in contactos:
			lista_contactos = self.modelo.extraer_lista_contactos(contacto.nick)
			iterador = 0
			for lista in lista_contactos:
				if lista.nick == usuario:
					lista_contactos[iterador].estado = estado
					self.modelo.actualizar_lista_contactos(contacto.nick, lista_contactos)
					break
				iterador = iterador + 1
			for hilo in self.hilos_conexiones:
				if hilo.is_alive() is True and hilo.nick == contacto.nick:
					hilo.enviar_historial()

	def realizar_conexion(self, paquete_recibido):
		''' Función encargada de realizar el inicio de sesión de un usuario,
			para tal efecto, recibe el paquete de conexion con el nick y la
			contraseña, los valida y de ser validos los datos cambia el esta
			do a Online, se le envia su historial y se le avisa a sus
			contactos que el está online
		'''
		self.nick = paquete_recibido.nick
		self.password = paquete_recibido.password

		if self.modelo.validar_credenciales(self.nick, self.password):
			paquete = PaqueteNotificacion(NOTIF_USUARIO_CONECTADO, self.addr)
			self.comunicador.put(paquete)
			respuesta = True

		else:
			paquete = PaqueteNotificacion(NOTIF_USUARIO_ERROR, self.nick)
			self.comunicador.put(paquete)
			respuesta = False

		paquete_sesion = PaqueteRespuesta(respuesta, REF_INICIO_SESION)
		paquete_sesion = pickle.dumps(paquete_sesion)

		self.conn.send(paquete_sesion)

		if respuesta is True:
			self.modelo.actualizar_estado_usuario(self.nick, True)
			self.enviar_historial()
			self.enviar_historial_contactos(self.nick,\
			self.modelo.extraer_lista_contactos(self.nick), True)

	def realizar_test(self, paquete_recibido):
		''' Método que maneja el paquete de test conexión, registrando
			el log de que tal ip envio un paquete de test conexión
		'''
		paquete = PaqueteNotificacion(NOTIF_CONEXION_TEST, self.addr)
		self.comunicador.put(paquete)

	def enviar_historial(self):
		''' Método que extrae de la bd el historial del usuario conectado,
			lo empaqueta en un PaqueteHistorial, lo serializa y lo envia al
			Cliente el cual lo va a recibir y lo debe cargar en su Usuario
		'''
		historial = self.modelo.extraer_historial(self.nick)
		if historial is not None:
			paquete_historial = PaqueteHistorial(historial)
			paquete_historial = pickle.dumps(paquete_historial)
			self.conn.sendall(paquete_historial)

	def enviar_mensaje(self, paquete_recibido):
		''' Método que recibe el paquete de mensaje, lo guarda en la base de
			datos, verifica que el receptor del mensaje esté en linea y si
			lo está se lo envía a traves de su respectivo hilo
		'''
		paquete = PaqueteNotificacion(NOTIF_MENSAJE, paquete_recibido.mensaje)
		self.comunicador.put(paquete)

		respuesta = self.modelo.agregar_mensaje(paquete_recibido.mensaje)

		if respuesta is True:
			if self.modelo.verificar_estado(paquete_recibido.mensaje.receptor) is True:
				for hilo in self.hilos_conexiones:
					if hilo.is_alive():
						if hilo.nick == paquete_recibido.mensaje.receptor:
							hilo.conn.send(pickle.dumps(paquete_recibido))

		self.enviar_historial()
		return NOTIF_EXITO

	def agregar_contacto(self, paquete_contacto):
		''' Método manejador del PaqueteContacto, el cual verifica si
			el paquete es para agregar usuario o para eliminar, en el
			primer caso, se valida que el nick del contacto a agregar
			exista, si no existe se envia al cliente False y en caso
			contrario, se guarda en la base de datos dicho contacto se
			envia al cliente true y se le envia su historial con el
			nuevo contacto agregado
		'''
		paquete = PaqueteNotificacion(NOTIF_CONTACTO, paquete_contacto)
		self.comunicador.put(paquete)

		if paquete_contacto.agregar is True:
			contacto = Contacto()
			contacto.nick = paquete_contacto.contacto
			respuesta = self.modelo.agregar_contacto(self.nick, contacto)
		else:
			respuesta = self.modelo.eliminar_contacto(self.nick, contacto)

		paquete_contacto = PaqueteRespuesta(respuesta, REF_CONTACTO)
		paquete_contacto = pickle.dumps(paquete_contacto)
		self.conn.send(paquete_contacto)

		if respuesta is True:
			self.enviar_historial()

	def registrar_usuario(self, paquete_recibido):
		''' Método encargado de registrar al usuario recibido en el paquete,
			primero se valida que el nickname no exista en la base de datos,
			se muestra el log en la bd de la operacion, luego se guarda en la
			bd al usuario registrado y se envia la respuesta al cliente
			de que la operacion fue exitosa, en caso contrario se muestra el
			log de error en el registro y se le envia al cliente el error en
			la operacion
		'''
		respuesta = self.modelo.guardar_usuario(paquete_recibido.datos_usuario)

		if respuesta is True:
			paquete = PaqueteNotificacion(NOTIF_REGISTRO, paquete_recibido.datos_usuario)
			self.comunicador.put(paquete)
		else:
			paquete = PaqueteNotificacion(NOTIF_ERROR_REGISTRO, paquete_recibido.datos_usuario)
			self.comunicador.put(paquete)

		paquete_respuesta = PaqueteRespuesta(respuesta, REF_REGISTRO)
		paquete_respuesta = pickle.dumps(paquete_respuesta)
		self.conn.send(paquete_respuesta)
