from VistaTk import Vista
from Controlador import Controlador

class AplicacionServidor:
    ''' Clase que se encarga de iniciar el programa '''
    def __init__(self):
        ''' inicializador que crea la lista de conexiones'''
        self.hilos_conexiones = []

    def salir(self):
        ''' Metodo para cerrar el programa '''
        exit()

    def iniciar(self):
        ''' Método que crea el controlador e inicia la vista '''
        self.controlador = Controlador(self.hilos_conexiones, self.salir)
        self.controlador.iniciar()

if __name__ == "__main__":
    app = AplicacionServidor()
    app.iniciar()
