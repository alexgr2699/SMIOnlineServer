from threading import Thread
import socket
from queue import Queue

import os
os.chdir("..")
from utils import *
from modelo.HiloCliente import *
from modelo.Paquete import *

class Servidor(Thread):
    ''' '''
    def __init__(self, datos_servidor, hilos_conexiones, comunicador_notificaciones, root):
        ''' '''
        Thread.__init__(self)
        self.root = root
        self.datos_servidor = datos_servidor
        self.hilos_conexiones = hilos_conexiones
        self.comunicador_notificaciones = comunicador_notificaciones

    def run(self):
        ''' '''
        self.stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.stream.bind(self.datos_servidor)
        except OSError as e:
            paquete = PaqueteNotificacion(NOTIF_CONEXION_ERROR)
            self.comunicador_notificaciones.put(paquete)
        else:
            paquete = PaqueteNotificacion(NOTIF_CONEXION_OK, self.datos_servidor[1])
            self.comunicador_notificaciones.put(paquete)
            self.stream.listen(CONEXION_MAX)

            while True:
                conn, addr = self.stream.accept()
                self.hilos_conexiones.append(HiloCliente(conn, addr, self.comunicador_notificaciones, self.root, self.hilos_conexiones))
                ### ACTUALIZAR LOS CONTACTOS CONECTADOS EN TODOS LOS USUARIOS CONECTADOS ###
                ### for hilo in self.hilos_conexiones : hilo.send( vector de todos los contactos )
                self.hilos_conexiones[len(self.hilos_conexiones)-1].start()