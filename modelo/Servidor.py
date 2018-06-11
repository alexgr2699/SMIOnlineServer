from threading import Thread
from queue import Queue

import socket
import os

os.chdir("..")

from utils import *
from modelo.HiloCliente import HiloCliente
from modelo.Paquete import *

class Servidor(Thread):
    ''' Clase que corresponde al hilo del servidor el cual recibe los datos
        del servidor, recibo los hilos de conexiones, el comunicador , el
        modelo
    '''
    def __init__(self, datos_servidor, hilos_conexiones, comunicador_notificaciones, modelo):
        Thread.__init__(self)
        self.modelo = modelo
        self.datos_servidor = datos_servidor
        self.hilos_conexiones = hilos_conexiones
        self.comunicador_notificaciones = comunicador_notificaciones

    def cerrar(self):
        for i in self.hilos_conexiones:
            i.conn.shutdown(0)
            i.conn.close()
        self.stream.shutdown(0)
        self.stream.close()

    def run(self):
        ''' Funcion que crea un socket y lo pone a la escucha de conexiones
            entrantes en el ip y puerto establecidos en datos del servidor,
            cada vez que se conecta un usuario se le vincula a un hilo de
            conexion, pasandole el comunicador, la bd y los demas hilos,
            el servidor puede recibir a la vez a CONEXION_MAX clientes
            establecidos en el archivo utils.py
        '''
        self.stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
                try:
                    conn, addr = self.stream.accept()
                except OSError as e:
                    paquete = PaqueteNotificacion(NOTIF_SALIR)
                    self.comunicador_notificaciones.put(paquete)
                    break

                self.hilos_conexiones.append(HiloCliente(conn, addr,\
                self.comunicador_notificaciones, self.hilos_conexiones,\
                self.modelo))

                ### ACTUALIZAR LOS CONTACTOS CONECTADOS EN TODOS LOS USUARIOS CONECTADOS ###
                ### for hilo in self.hilos_conexiones : hilo.send( vector de todos los contactos )
                self.hilos_conexiones[len(self.hilos_conexiones)-1].start()
