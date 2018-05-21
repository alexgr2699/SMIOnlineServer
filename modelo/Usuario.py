from .Persona import *
from persistent import Persistent

class Usuario (Persona, Persistent):
    '''Clase que corresponde a los datos correpondientes de cada usuario'''
    cantidad_usuarios = 0
    def __init__(self):
        ''' '''
        Persona.__init__(self)   
        self.nick = ""
        self.online = False
        self.password = ""
        self.historial_mensajes = []
        self.lista_contactos = []
        
    def __str__(self):
        ''' '''
        return "Nombre y Apellido: " + self.nombre + " " + self.apellido +\
                "\nSexo: " + self.sexo +\
                "\nFecha de nacimiento: " + self.fecha_nacimiento +\
                "\nNombre de usuario: " + self.nick+\
                "\nOnline: " + str(self.online)