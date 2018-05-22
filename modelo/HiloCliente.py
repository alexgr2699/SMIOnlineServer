from threading import Thread
from modelo.Paquete import *
from modelo.Usuario import *
from modelo.Contacto import *
from utils import *
import pickle
import transaction

class HiloCliente(Thread):
	'''Hilo del cliente que se ha conectado'''

	def __init__(self, conn, addr, comunicador_notificaciones, root, hilos_conexiones):
		''' '''
		Thread.__init__(self)
		self.hilos_conexiones = hilos_conexiones
		self.root = root
		self.conn = conn
		self.addr = addr
		self.nick = ''
		self.comunicador = comunicador_notificaciones
		self.manejador_codigos_paquete = {
			PAQ_CONEXION: self.realizar_conexion,\
			PAQ_TEST: self.realizar_test,\
			PAQ_MENSAJE: self.enviar_mensaje,\
			PAQ_REGISTRO: self.registrar_usuario,\
			PAQ_CONTACTO: self.agregar_contacto
		}

	def run(self):
		''' funcion que inicia el hilo y se pone a la recepcion de paquetes'''
		while True:
			try:
				input_data = self.conn.recv(1024)
				input_data = pickle.loads(input_data)
			except Exception as e:
				paquete = PaqueteNotificacion(NOTIF_USUARIO_DESCONECTADO, self.addr)
				self.comunicador.put(paquete)

				if self.validar_nickname(self.nick) is False:
					datos = self.root[self.nick]
					datos.online = False
					self.root[self.nick] = datos
					transaction.commit()
					self.enviar_historial_contactos(self.nick, self.root[self.nick].lista_contactos, False)
				break;
			else:
				self.manejador_codigos_paquete[input_data.codigo](input_data)

	def enviar_historial_contactos(self, usuario, contactos, estado):
		for contacto in contactos:
			lista_contactos = self.root[contacto.nick].lista_contactos
			iterador = 0
			for lista in lista_contactos:
				if lista.nick == usuario:
					lista_contactos[iterador].estado = estado
					self.root[contacto.nick].lista_contactos = lista_contactos
					transaction.commit()
					break
				iterador = iterador + 1
			for hilo in self.hilos_conexiones:
				if hilo.is_alive() is True and hilo.nick == contacto.nick:
					hilo.enviar_historial()
					
	def realizar_conexion(self, paquete_recibido):
		''' funcion encargada '''
		self.nick = paquete_recibido.nick
		self.password = paquete_recibido.password

		if self.validar_usuario(self.nick, self.password):
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
			self.root[self.nick].online = True
			transaction.commit()
			self.enviar_historial()
			self.enviar_historial_contactos(self.nick, self.root[self.nick].lista_contactos, True)

	def realizar_test(self, paquete_recibido):
		''' '''
		paquete = PaqueteNotificacion(NOTIF_CONEXION_TEST, self.addr)
		self.comunicador.put(paquete)

	def enviar_historial(self):
		''' '''
		print(self.root[self.nick])
		paquete_historial = PaqueteHistorial(self.root[self.nick])
		paquete_historial = pickle.dumps(paquete_historial)
		self.conn.sendall(paquete_historial)

	def enviar_mensaje(self, paquete_recibido):
		''' '''
		paquete = PaqueteNotificacion(NOTIF_MENSAJE, paquete_recibido.mensaje)
		self.comunicador.put(paquete)

		historial_mensajes_receptor = self.root[paquete_recibido.mensaje.receptor].historial_mensajes
		historial_mensajes_receptor.append(paquete_recibido.mensaje)
		self.root[paquete_recibido.mensaje.receptor].historial_mensajes = historial_mensajes_receptor
		transaction.commit()

		if self.root[paquete_recibido.mensaje.receptor].online is True:
			for hilo in self.hilos_conexiones:
				if hilo.is_alive():
					if hilo.nick == paquete_recibido.mensaje.receptor:
						print(hilo.nick)
						print(hilo.addr)
						print(hilo.conn)
						hilo.conn.send(pickle.dumps(paquete_recibido))

		historial_mensajes = self.root[self.nick].historial_mensajes
		historial_mensajes.append(paquete_recibido.mensaje)
		self.root[self.nick].historial_mensajes = historial_mensajes
		transaction.commit()

		self.enviar_historial()

		return NOTIF_EXITO

	def agregar_contacto(self, paquete_contacto):
		''' '''
		paquete = PaqueteNotificacion(NOTIF_CONTACTO, paquete_contacto)
		self.comunicador.put(paquete)

		if paquete_contacto.agregar is True:
			if self.validar_nickname(paquete_contacto.contacto):
				respuesta = False				
				## esta mal ##
			else:
				contacto = Contacto()
				contacto.nick = paquete_contacto.contacto
				contacto.estado = self.root[contacto.nick].online
				lista_contactos = self.root[self.nick].lista_contactos
				lista_contactos.append(contacto)
				print(contacto)
				self.root[self.nick].lista_contactos = lista_contactos
				transaction.commit()
				respuesta = True
		else:
			# eliminar contacto
			pass
		paquete_sesion = PaqueteRespuesta(respuesta, REF_CONTACTO)
		paquete_sesion = pickle.dumps(paquete_sesion)
		self.conn.send(paquete_sesion)
		self.enviar_historial()

	def validar_usuario(self, nickname, password):
		''' '''
		try:
			self.root[nickname]
		except Exception as e:
			return False
		else:
			if self.root[nickname].password == password:
				return True
			else:
				return False

	def validar_nickname(self, nickname):
		''' '''
		try:
			self.root[nickname]
		except Exception as e:
			return True
		else:
			return False

	def registrar_usuario(self, paquete_recibido):
		''' '''
		if self.validar_nickname(paquete_recibido.datos_usuario.nick):
			self.root[paquete_recibido.datos_usuario.nick] = paquete_recibido.datos_usuario
			transaction.commit()
			paquete = PaqueteNotificacion(NOTIF_REGISTRO, paquete_recibido.datos_usuario)
			self.comunicador.put(paquete)
			respuesta = True
		else:
			paquete = PaqueteNotificacion(NOTIF_ERROR_REGISTRO, paquete_recibido.datos_usuario)
			self.comunicador.put(paquete)
			respuesta = False

		paquete_respuesta = PaqueteRespuesta(respuesta, REF_REGISTRO)
		paquete_respuesta = pickle.dumps(paquete_respuesta)
		self.conn.send(paquete_respuesta)