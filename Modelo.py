from ZODB import DB, FileStorage
from datetime import datetime
import transaction
import os
os.chdir("Servidor")

class Modelo:
	''' Clase representativa del modelo (MVC) la cual se encargará de
		de la persistencia de los datos
	 '''

	def abrir_bd(self):
		''' Método que inicia la bd '''
		self.storage = FileStorage.FileStorage('database/SMIOnlineDATA.fs')
		self.bd = DB(self.storage)
		self.conexion = self.bd.open()
		self.root = self.conexion.root()

	def cerrar_bd(self):
		''' Método que cierra la bd '''
		transaction.abort()
		self.conexion.close()

	def buscar_contacto(self, usuario):
		''' Metodo que busca un usuario en la base de datos segun el nick,
		  retorna el usuario buscado y en caso de no existir retorna None
		'''
		coincidencias = []
		if self.verificar_existencia_usuario(usuario) is False:
		  # retornamos los datos del usuario ya que el nick es único
		  coincidencias = self.extraer_historial(usuario)
		else:
		  # buscar por nombre y apellido
		  coincidencias = self.buscar_contacto_por_nombre(usuario)
		return coincidencias

	def buscar_contacto_por_nombre(self, usuario):
		coincidencias = []
		for key in self.root.keys():
			auxiliar = self.root[key]
			if auxiliar.nombre == usuario or \
				(auxiliar.nombre + " " + auxiliar.apellido) == usuario:
				coincidencias.append(self.root[key])
		return coincidencias

	def guardar_usuario(self, usuario):
		''' Método que guarda un usuario nuevo, retorna True
		  en caso de éxito y False en caso de error
		'''
		try:
		  self.root[usuario.nick]
		except Exception as e:
			if self.verificar_campos(usuario):
				self.root[usuario.nick] = usuario
				transaction.commit()
				return True
			else:
				return False
		else:
			return False

	def verificar_campos(self, usuario):
		''' Funcion que valida los datos del usuario que no esten vacios
			y que el formato de fecha sea valido
		'''
		if not(usuario.nick and usuario.nick.strip()):
		  return False
		if not(usuario.password and usuario.password.strip()):
		  return False
		if not(usuario.nombre and usuario.nombre.strip()):
		  return False
		if not(usuario.apellido and usuario.apellido.strip()):
		  return False
		if not(usuario.sexo and usuario.sexo.strip()):
		  return False
		if not self.validar_campo_fecha(usuario.fecha_nacimiento):
		  return False
		return True

	def validar_campo_fecha(self, fecha):
		''' Funcion que valida un campo de fecha dd/mm/aaaa '''
		try:
			datetime.strptime(fecha, "%d/%m/%Y")
		except ValueError:
		  return False
		else:
			return True

	def agregar_contacto(self, nick_usuario, contacto):
		''' metodo que agrega un contacto a la bd '''

		try:
			self.root[contacto.nick]
			if not(contacto.nick and contacto.nick.strip()):
				raise Exception("CadenaVacia")
			if nick_usuario == contacto.nick:
				raise Exception("Autoagregado")
		except Exception as e:
			return False
		else:
			lista_contactos = self.root[nick_usuario].lista_contactos
			contacto.estado = self.root[contacto.nick].online

			for i in lista_contactos:
				if i.nick == contacto.nick:
					# El contacto ya existe
					return False

			lista_contactos.append(contacto)
			self.root[nick_usuario].lista_contactos = lista_contactos
			transaction.commit()
			return True

	def extraer_historial(self, usuario):
		''' metodo que retorna el historial del usuario '''
		historial = self.root[usuario]
		if historial is not None:
		  return historial
		return None

	def extraer_historial_mensajes(self, usuario):
		''' Metodo que retorna el historial de mensajes '''
		mensajes = self.root[usuario].historial_mensajes
		return mensajes

	def extraer_lista_contactos(self, usuario):
		''' Metodo que retorna la lista de contactos del usuario '''
		contactos = self.root[usuario].lista_contactos
		return contactos

	def agregar_mensaje(self, obj_mensaje):
		''' Metodo que retorna true si se agrego el mensaje y false
		  si no se agrego
		'''
		lista_mensajes_emisor = self.root[obj_mensaje.emisor].historial_mensajes
		lista_mensajes_receptor = self.root[obj_mensaje.receptor].historial_mensajes
		lista_mensajes_receptor.append(obj_mensaje)
		lista_mensajes_emisor.append(obj_mensaje)
		self.root[obj_mensaje.emisor].historial_mensajes = lista_mensajes_emisor
		self.root[obj_mensaje.receptor].historial_mensajes = lista_mensajes_receptor
		transaction.commit()
		return True

	def verificar_estado(self, nick):
		''' metodo que retorna el estado del usuario online u offline'''
		estado = self.root[nick].online
		return estado

	def actualizar_perfil_usuario(self, usuario, paquete):
		''' Metodo que actualiza el perfil del usuario, recibe el usuario,
		  sus nuevos datos y retorna True en caso de exito y false en caso
		  de error '''
		try:
		  self.root[usuario].nombre = paquete.datos_usuario[0]
		  self.root[usuario].apellido = paquete.datos_usuario[1]
		  self.root[usuario].sexo = paquete.datos_usuario[2]
		  self.root[usuario].fecha_nacimiento = paquete.datos_usuario[3]
		except Exception as e:
		  return False
		else:
		  transaction.commit()
		  return True

	def actualizar_lista_contactos(self, nick, lista_contactos):
		''' metodo que actualiza la lista de contactos'''
		self.root[nick].lista_contactos = lista_contactos
		transaction.commit()

	def actualizar_estado_usuario(self, nick, estado):
		  ''' metodo que recibe el usuario y su nuevo estado para luego
			 cambiar su estado
		  '''
		  self.root[nick].online = estado
		  transaction.commit()

	def verificar_existencia_usuario(self, nick):
		''' Método que valida que el nickname exista o no en la bd
		  si es que el nickname no existe retorna True y en caso
		  de que exista retorna False
		'''
		try:
		  self.root[nick]
		except Exception as e:
		  return True
		else:
		  return False

	def validar_credenciales(self, nick, password):
		''' Metodo que valida las credenciales, retorna True en caso
		  de que sea un usuario y sus credenciales esten bien, en
		  caso contrario retorna False
		'''
		try:
			self.root[nick]
		except Exception as e:
			return False
		else:
			if self.root[nick].password == password:
				return True
			else:
				return False
