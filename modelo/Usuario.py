from .Persona import Persona
from persistent import Persistent

class Usuario (Persona, Persistent):
    ''' Clase que corresponde a los datos correpondientes de cada usuario y sus
        acciones
    '''
    def __init__(self, nombre="", apellido="", sexo="", fecha_nacimiento=""):
        Persona.__init__(self, nombre, apellido, sexo, fecha_nacimiento)
        self.nick = ""
        self.online = False
        self.password = ""
        self.historial_mensajes = []
        self.lista_contactos = []

    def __str__(self):
        ''' toString del usuario '''
        return "Nombre y Apellido: " + self.nombre + " " + self.apellido +\
                "\nSexo: " + self.sexo +\
                "\nFecha de nacimiento: " + self.fecha_nacimiento +\
                "\nNombre de usuario: " + self.nick+\
                "\nOnline: " + str(self.online)
