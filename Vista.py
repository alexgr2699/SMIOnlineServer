import os
from threading import Thread
from modelo.Paquete import *
from utils import *

class Vista:
    ''' Clase para armar e imprimir mensajes, y leer los valores '''
    def __init__(self, controlador):
        ''' '''
        self.Controlador = controlador
        Vista.limpiar_pantalla()

    def iniciar(self):
        ''' '''
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
        ''' '''
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
            NOTIF_CONTACTO: self.mostrar_proceso_contacto
        }

    def run(self):
        ''' '''
        while True:
            paquete = self.comunicacion.get()
            if paquete.codigo == NOTIF_CONEXION_ERROR:
                self.manejador_notificaciones[paquete.codigo](paquete.extra)
                break
            self.manejador_notificaciones[paquete.codigo](paquete.extra);

    @staticmethod
    def mostrar_desconexion(direccion):
        ''' '''
        Vista.imprimir("\n# " + str(direccion) + " se ha desconectado")

    def mostrar_proceso_contacto(self, paquete):
        ''' '''
        if paquete.agregar is True:
            Vista.imprimir("\n# Agregar contacto: " + paquete.contacto)
        else:
            Vista.imprimir("\n# Eliminar contacto: " + paquete.contacto)            

    def mostrar_mensaje_proceso(self, mensaje):
        ''' '''
        Vista.imprimir("\n# Paquete de Mensaje recibido")

    def mostrar_error_usuario(self, usuario):
        ''' '''
        Vista.imprimir("\n# Error en inicio de sesión: " + usuario)

    def mostrar_test_conexion(self, direccion):
        ''' '''
        Vista.imprimir("\n# Test de conexión - Dir: " + str(direccion))

    def mostrar_registro_proceso(self, usuario):
        ''' '''
        Vista.imprimir("\n# Paquete Registro:")
        Vista.imprimir(usuario)

    def mostrar_error_registro(self, usuario):
        ''' '''
        Vista.imprimir("\n# Error en el registro: " + usuario.nick)

    @staticmethod
    def mostrar_notificacion(mensaje):
        ''' '''
        Vista.imprimir(mensaje)

    @staticmethod
    def mostrar_bienvenida():
        ''' '''
        Vista.imprimir("____________________________________________________________")
        Vista.imprimir("|||||||||||| BIENVENIDO AL SERVIDOR DEL SMIOnline ||||||||||")
        Vista.imprimir("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")

    @staticmethod
    def mostrar_fin_programa():
        ''' '''
        Vista.imprimir("____________________________________________________________")
        Vista.imprimir("|||||||||||||||||||| FIN DEL SERVIDOR ||||||||||||||||||||||")
        Vista.imprimir("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")

    @staticmethod
    def mostrar_usuario_conectado(extra):
        ''' '''
        Vista.imprimir("\n# " + str(extra) + " se ha conectado.")

    def mostrar_error_conexion(self, extra):
        ''' '''
        Vista.imprimir("\n### Error de conexión ###")
        Notificacion.mostrar_fin_programa()

    @staticmethod
    def mostrar_error_operacion(extra):
        ''' '''
        Vista.imprimir("\n### Hubo un error al realizar la operación ###")

    @staticmethod
    def mostrar_correcta_conexion(extra):
        ''' '''
        Vista.imprimir("\n# Conexión realizada exitosamente !!!")
        Vista.imprimir("# Puerto en escucha: " + str(extra) + "\n")

    @staticmethod
    def mostrar_inicio_sesion(nick):
        ''' '''
        Vista.imprimir("\n# El usuario " + nick + " se ha conectado #")

    @staticmethod
    def mostrar_no_hay_usuarios():
        ''' '''
        Vista.imprimir("\n# No hay usuarios conectados #")


#################################################################################################

class Lista:
    ''' Clase para mostrar las distintas listas del sistema '''
    @staticmethod
    def listar_usuarios_conectados(usuarios):
        ''' '''
        Vista.limpiar_pantalla()
        if usuarios == []:
            Notificacion.mostrar_no_hay_usuarios()
        else:
            for usuario in usuarios:
                Vista.imprimir(usuario)