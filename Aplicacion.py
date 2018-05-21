from Vista import *
from Controlador import *
from ZODB import DB, FileStorage

import threading
import time
import transaction

class AplicacionServidor:
    ''' '''
    def __init__(self):
        ''' '''
        self.hilos_conexiones = []

    @staticmethod
    def salir():
        ''' '''
        exit()

    def iniciar(self):
        ''' '''
        self.iniciarBD()
        self.controlador = Controlador(self.hilos_conexiones, self.bd, self.conexion, self.root)
        self.controlador.iniciar_vista()

    def iniciarBD(self):
        ''' '''
        self.almacenamiento = FileStorage.FileStorage('SMIOnlineDATA.fs')
        self.bd = DB(self.almacenamiento)
        self.conexion = self.bd.open()
        self.root = self.conexion.root()

if __name__ == "__main__":
    app = AplicacionServidor()
    app.iniciar()