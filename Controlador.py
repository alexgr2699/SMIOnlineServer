from modelo.HiloCliente import *
from modelo.Paquete import *
from modelo.Servidor import *

from utils import *
from Vista import *

from queue import Queue
from threading import Thread
import socket
import signal

class Controlador:
    '''  '''
    def __init__(self, hilos_conexiones, bd, conexion, root):
        self.hilos_conexiones = hilos_conexiones
        self.datos_servidor = ("", 6030)
        self.comunicador_notificaciones = Queue()
        self.bd = bd
        self.conexion = conexion
        self.root = root

    def iniciar_vista(self):
        ''' '''
        vista = Vista(self)
        vista.iniciar()

    def salir(self):
        ''' '''
        Aplicacion.salir()

    def iniciar_servidor(self):
        ''' '''
        self.servidor = Servidor(self.datos_servidor, self.hilos_conexiones,\
                                        self.comunicador_notificaciones, self.root)
        self.servidor.start()

    def post_comunicador_notificaciones(self):
        ''' '''
        return self.comunicador_notificaciones