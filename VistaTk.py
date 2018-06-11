from threading import Thread
from tkinter import *
from tkinter import ttk
from utils import *
import datetime
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmsgbox

class Vista:
	def __init__(self, controlador):
		self.Controlador = controlador

	def iniciar(self):

		self.ventana_principal = Ventana('Servidor SMIOnline | v1.0', self.Controlador)
		self.mostrar_ventana_principal(self.ventana_principal.ventana)

		self.comunicador = self.Controlador.post_comunicador_notificaciones()
		self.notificador = Notificacion(self.comunicador, self)
		self.notificador.start()
		self.Controlador.iniciar_servidor()

		self.ventana_principal.invocar()

	def mostrar_ventana_principal(self, principal):
		self.etiqueta1 = Etiqueta(ventana=principal,
								 nombre="Servidor SMIOnline", color= "black",
								fuente='Ubuntu', tamano=20)
		self.etiqueta1.invocar_pack()

		self.textoScroll1 = TextoScroll(master=principal,
									envoltorio=WORD,
									ancho=100, alto=10)

		self.textoScroll1.invocar_pack(padx=10, pady=10, llenar=BOTH, expandir=True)

		boton1 = Boton(ventana=principal,
						nombre="Guardar Log", color="white",
						bg="blue", evento=lambda: self.evento_guardar_log())
		boton1.invocar_pack(posicion="derecha")

		boton2 = Boton(ventana=principal,
						nombre="Cerrar servidor", color="white",
						bg="red", evento=lambda: self.evento_cerrar_servidor())
		boton2.invocar_pack(posicion="derecha")

	def evento_guardar_log(self):
		nombre_archivo = "logs/log-" + str(datetime.datetime.now()) + ".dat"
		archivo = open(nombre_archivo, "w")
		archivo.write(self.textoScroll1.get())
		archivo.close()

	def evento_cerrar_servidor(self):
		self.evento_guardar_log()
		self.ventana_principal.salir()
		self.controlador.salir()

class Boton():
	''' Clase que representa un botón de Tkinter (Button)'''
	def __init__(self, ventana, nombre, color, bg, evento):
		self.boton = Button(ventana, text=nombre,
							fg=color, bg=bg, command=evento,
							cursor="hand1")

	def invocar_place(self, pos_x=100, pos_y=100):
		self.boton.place(x=pos_x, y=pos_y)

	def invocar_grid(self,fila=0,columna=0,comb_fila=1,comb_columna=1):
		self.boton.grid(row=fila, column=columna,
						rowspan=comb_fila, columnspan=comb_columna)

	def invocar_pack(self, posicion = "centro"):
		if posicion == "centro" :
			self.boton.pack()
		elif posicion == "derecha" :
			self.boton.pack(side=RIGHT)
		elif posicion == "izquierda" :
			self.boton.pack(side=LEFT)

class Etiqueta():
	'''	Clase que representa las etiquetas de Tkinter (Label) '''
	def __init__(self, ventana, nombre, color, fuente, tamano):
		self.etiqueta = Label(ventana, text=nombre,
								fg= color, font=(fuente,tamano))

	def invocar_place(self, pos_x=100, pos_y=100):
		self.etiqueta.place(x=pos_x, y=pos_y)

	def invocar_grid(self,fila=0,columna=0,comb_fila=1,comb_columna=1):
		self.etiqueta.grid(row=fila, column=columna,
							rowspan=comb_fila, columnspan=comb_columna)

	def invocar_pack(self, posicion = "centro"):
		if posicion == "centro" :
			self.etiqueta.pack()
		elif posicion == "derecha" :
			self.etiqueta.pack(side=RIGHT)
		elif posicion == "izquierda" :
			self.etiqueta.pack(side=LEFT)


class Ventana():
	'''	Clase que representa una ventana principal de Tkinter '''
	def __init__(self, nombre, controlador):
		self.ventana = Tk()
		self.ventana.title(nombre)
		self.ventana.geometry("500x500")
		self.controlador = controlador

	def invocar(self):
		self.ventana.mainloop()

	def salir(self):
		self.ventana.destroy()
		self.controlador.salir()

class TextoScroll():
	def __init__(self, master, envoltorio, ancho, alto ):
		self.textoScroll = tkst.ScrolledText( master = master, wrap = envoltorio,
												width  = ancho, height = alto )

	def invocar_pack(self, padx, pady, llenar, expandir):
		self.textoScroll.pack(padx=padx, pady=pady, fill=llenar, expand=expandir)

	def insertar(self, mensaje):
		self.textoScroll.insert(INSERT, mensaje)

	def configurar_estado(self, estado):
		self.textoScroll.configure(state=estado)

	def get(self):
		return self.textoScroll.get(1.0,END)

class Notificacion(Thread):
	''' Clase para mostrar las notificaciones del sistema '''

	def __init__(self, comunicacion, vista):
		''' Recibe el comunicador y crea el diccionario de funciones
			manejadores de los paquetes de notificacion
		'''
		Thread.__init__(self)
		self.vista = vista
		self.comunicacion = comunicacion
		self.manejador_notificaciones = {
			NOTIF_CONEXION_OK: self.mostrar_correcta_conexion,\
			NOTIF_CONEXION_ERROR: self.mostrar_error_conexion,\
			NOTIF_USUARIO_CONECTADO: self.mostrar_usuario_conectado,\
			NOTIF_USUARIO_DESCONECTADO: self.mostrar_desconexion,\
			NOTIF_CONEXION_TEST: self.mostrar_test_conexion,\
			NOTIF_MENSAJE: self.mostrar_mensaje_proceso,\
			NOTIF_REGISTRO: self.mostrar_registro_proceso,\
			NOTIF_ERROR_REGISTRO: self.mostrar_error_registro,\
			NOTIF_USUARIO_ERROR: self.mostrar_error_usuario,\
			NOTIF_CONTACTO: self.mostrar_proceso_contacto,\
			NOTIF_ACTUALIZACION: self.mostrar_proceso_actualizacion,\
			NOTIF_ACTUALIZACION_EXITO: self.mostrar_exito_actualizacion,\
			NOTIF_ACTUALIZACION_ERROR: self.mostrar_error_actualizacion,\
		}

	def run(self):
		''' Método que se pone a la recepcion de paquetes de notificacion
			los cuales los recibe a través del comunicador (pila)
		'''
		while True:
			paquete = self.comunicacion.get()
			if paquete.codigo == NOTIF_CONEXION_ERROR:
				self.manejador_notificaciones[paquete.codigo](paquete.extra)
				break
			elif paquete.codigo == NOTIF_SALIR:
				break
			self.manejador_notificaciones[paquete.codigo](paquete.extra);

	def mostrar_proceso_actualizacion(self, nick):
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Edicion de perfil : " + nick)

	def mostrar_exito_actualizacion(self, nick):
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Perfil de " + nick + " editado exitosamente")

	def mostrar_error_actualizacion(self, nick):
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Error al editar el perfil de " + nick)

	def mostrar_desconexion(self, direccion):
		''' Método que muestra que un usuario se ha desconectado'''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # " + str(direccion) + " se ha desconectado")

	def mostrar_proceso_contacto(self, paquete):
		''' Método que muestra el proceso de agregar o eliminar contacto '''
		if paquete.agregar is True:
			self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Agregar contacto: " + paquete.contacto)
		else:
			self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Eliminar contacto: " + paquete.contacto)

	def mostrar_mensaje_proceso(self, mensaje):
		''' Método que informa que se recibió un paquete de mensaje '''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Paquete de Mensaje recibido")

	def mostrar_error_usuario(self, usuario):
		''' Ḿétodo que muestra el error de inicio de sesion de un usario'''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Error en inicio de sesión: " + usuario)

	def mostrar_test_conexion(self, direccion):
		''' Método que informa que se ha recibido un paquete de test de
			conexión de X dirección
		'''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Test de conexión - Dir: " + str(direccion))

	def mostrar_registro_proceso(self, usuario):
		''' Muestra que se recibio un paquete de registro, listando los datos
		'''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Paquete Registro:\n")
		self.vista.textoScroll1.insertar(usuario)

	def mostrar_error_registro(self, usuario):
		''' Metodo que informa que hubo un error en el registro de x usuario
		'''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Error en el registro: " + usuario.nick)

	@staticmethod
	def mostrar_bienvenida(self):
		''' Método estático que muestra el mensaje de bienvenida al admin
			del servidor
		'''
		self.vista.textoScroll1.insertar("____________________________________________________________")
		self.vista.textoScroll1.insertar("|||||||||||| BIENVENIDO AL SERVIDOR DEL SMIOnline ||||||||||")
		self.vista.textoScroll1.insertar("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
		self.vista.textoScroll1.insertar("# Control + C para cerrar el servidor #")

	@staticmethod
	def mostrar_fin_programa(self):
		''' Método estático que imprime un mensaje que informa que el servidor
			fue cerrado
		'''
		self.vista.textoScroll1.insertar("____________________________________________________________")
		self.vista.textoScroll1.insertar("|||||||||||||||||||| FIN DEL SERVIDOR ||||||||||||||||||||||")
		self.vista.textoScroll1.insertar("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")

	def mostrar_usuario_conectado(self, extra):
		''' Método que muestra que un usuario se ha contacto '''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # " + str(extra) + " se ha conectado.")

	def mostrar_error_conexion(self, extra):
		''' Método que informa que  no se ha podido iniciar el servidor
			debido a conflicto de puertos
		'''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" ### Error: Puerto ya utilizado ###")

	def mostrar_correcta_conexion(self, extra):
		''' Método que informa que la conexión ha sido realizada correctamente
			ademas muestra el puerto a la escucha
		'''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Conexión realizada exitosamente !!!")
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # Puerto en escucha: " + str(extra) + "\n")

	@staticmethod
	def mostrar_no_hay_usuarios(self):
		''' Método que muestra que no hay usuarios conectados '''
		self.vista.textoScroll1.insertar("\n"+str(datetime.datetime.now())+" # No hay usuarios conectados #")
