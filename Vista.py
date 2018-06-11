import os
from threading import Thread
from modelo.Paquete import *
from utils import *

class Vista:
    ''' Clase para armar e imprimir mensajes, y leer los valores '''
    def __init__(self, controlador):
        ''' Método iniciializador de la vista el cual recibe el controlador
            y limpia la pantalla
        '''
        self.Controlador = controlador
        Vista.limpiar_pantalla()

    def iniciar(self):
        ''' Método utilizado para iniciar la vista el cual muestra el mensaje
            de bienvenida, inicia el hilo de notificaciones e inicia el
            servidor
        '''
        Notificacion.mostrar_bienvenida()
        self.comunicador = self.Controlador.post_comunicador_notificaciones()
        self.notificador = Notificacion(self.comunicador)
        self.notificador.start()
        self.Controlador.iniciar_servidor()

    @staticmethod
    def limpiar_pantalla():
        '''Limpia la pantalla'''
        os.system('cls' if os.name =='nt' else 'clear')

    @staticmethod
    def imprimir(mensaje):
        '''Imprime lo que se le envia por parametro'''
        print(mensaje)

#################################################################################################

class Notificacion(Thread):
    ''' Clase para mostrar las notificaciones del sistema '''

    def __init__(self, comunicacion):
        ''' Recibe el comunicador y crea el diccionario de funciones
            manejadores de los paquetes de notificacion
        '''
        Thread.__init__(self)
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
            self.manejador_notificaciones[paquete.codigo](paquete.extra);

    def mostrar_proceso_actualizacion(self, nick):
        Vista.imprimir("\n# Edicion de perfil : " + nick)

    def mostrar_exito_actualizacion(self, nick):
        Vista.imprimir("\n# Perfil de " + nick + " editado exitosamente")

    def mostrar_error_actualizacion(self, nick):
        Vista.imprimir("\n# Error al editar el perfil de " + nick)

    @staticmethod
    def mostrar_desconexion(direccion):
        ''' Método que muestra que un usuario se ha desconectado'''
        Vista.imprimir("\n# " + str(direccion) + " se ha desconectado")

    def mostrar_proceso_contacto(self, paquete):
        ''' Método que muestra el proceso de agregar o eliminar contacto '''
        if paquete.agregar is True:
            Vista.imprimir("\n# Agregar contacto: " + paquete.contacto)
        else:
            Vista.imprimir("\n# Eliminar contacto: " + paquete.contacto)

    def mostrar_mensaje_proceso(self, mensaje):
        ''' Método que informa que se recibió un paquete de mensaje '''
        Vista.imprimir("\n# Paquete de Mensaje recibido")

    def mostrar_error_usuario(self, usuario):
        ''' Ḿétodo que muestra el error de inicio de sesion de un usario'''
        Vista.imprimir("\n# Error en inicio de sesión: " + usuario)

    def mostrar_test_conexion(self, direccion):
        ''' Método que informa que se ha recibido un paquete de test de
            conexión de X dirección
        '''
        Vista.imprimir("\n# Test de conexión - Dir: " + str(direccion))

    def mostrar_registro_proceso(self, usuario):
        ''' Muestra que se recibio un paquete de registro, listando los datos
        '''
        Vista.imprimir("\n# Paquete Registro:")
        Vista.imprimir(usuario)

    def mostrar_error_registro(self, usuario):
        ''' Metodo que informa que hubo un error en el registro de x usuario
        '''
        Vista.imprimir("\n# Error en el registro: " + usuario.nick)

    @staticmethod
    def mostrar_bienvenida():
        ''' Método estático que muestra el mensaje de bienvenida al admin
            del servidor
        '''
        Vista.imprimir("____________________________________________________________")
        Vista.imprimir("|||||||||||| BIENVENIDO AL SERVIDOR DEL SMIOnline ||||||||||")
        Vista.imprimir("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
        Vista.imprimir("# Control + C para cerrar el servidor #")

    @staticmethod
    def mostrar_fin_programa():
        ''' Método estático que imprime un mensaje que informa que el servidor
            fue cerrado
        '''
        Vista.imprimir("____________________________________________________________")
        Vista.imprimir("|||||||||||||||||||| FIN DEL SERVIDOR ||||||||||||||||||||||")
        Vista.imprimir("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")

    @staticmethod
    def mostrar_usuario_conectado(extra):
        ''' Método que muestra que un usuario se ha contacto '''
        Vista.imprimir("\n# " + str(extra) + " se ha conectado.")

    def mostrar_error_conexion(self, extra):
        ''' Método que informa que  no se ha podido iniciar el servidor
            debido a conflicto de puertos
        '''
        Vista.imprimir("\n### Error: Puerto ya utilizado ###")
        Notificacion.mostrar_fin_programa()

    @staticmethod
    def mostrar_correcta_conexion(extra):
        ''' Método que informa que la conexión ha sido realizada correctamente
            ademas muestra el puerto a la escucha
        '''
        Vista.imprimir("\n# Conexión realizada exitosamente !!!")
        Vista.imprimir("# Puerto en escucha: " + str(extra) + "\n")

    @staticmethod
    def mostrar_no_hay_usuarios():
        ''' Método que muestra que no hay usuarios conectados '''
        Vista.imprimir("\n# No hay usuarios conectados #")


#################################################################################################

class Lista:
    ''' Clase para mostrar las distintas listas del sistema '''
    @staticmethod
    def listar_usuarios_conectados(usuarios):
        ''' Método estatico que recibe la lista de usuarios
            registrados y la imprime
        '''
        Vista.limpiar_pantalla()
        if usuarios == []:
            Notificacion.mostrar_no_hay_usuarios()
        else:
            for usuario in usuarios:
                Vista.imprimir(usuario)
