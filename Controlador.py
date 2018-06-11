from modelo.HiloCliente import *
from modelo.Paquete import *
from modelo.Servidor import *
from Modelo import Modelo

from utils import *
from VistaTk import *

from queue import Queue
from threading import Thread
import socket
import signal

class Controlador:
    ''' Clase representativa del controlador el cual servira como proveedor
        de las acciones del servidor
    '''
    def __init__(self, hilos_conexiones, salir_app):
        ''' Inicializador que recibe la lista de los hilos
            tambien define los datos del servidor por defecto
            (localhost y puerto 6030 y crea el comunicador de las noti
            ficaciones Queue)
        '''
        self.salir_app = salir_app
        self.hilos_conexiones = hilos_conexiones
        self.datos_servidor = ("", 6030)
        self.comunicador_notificaciones = Queue()

    def iniciar(self):
        ''' Método que inicia la vista pasandole a sí mismo es decir
            pasandole el objeto controlador que tiene las funciones
        '''
        self.modelo = Modelo()
        self.modelo.abrir_bd()
        vista = Vista(self)
        vista.iniciar()

    def salir(self):
        ''' Método para salir del programa '''
        self.servidor.cerrar()
        self.salir_app()

    def iniciar_servidor(self):
        ''' Método que crea un objeto de servidor y luego lo inicia pasandole
            los datos del servidor, los hilos, el comunicador y la bd
        '''
        self.servidor = Servidor(self.datos_servidor, self.hilos_conexiones,\
                                        self.comunicador_notificaciones, self.modelo)
        self.servidor.start()

    def post_comunicador_notificaciones(self):
        ''' Método que retorna el comunicador de notificaciones '''
        return self.comunicador_notificaciones
