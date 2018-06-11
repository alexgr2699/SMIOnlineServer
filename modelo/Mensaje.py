from persistent import Persistent

class Mensaje(Persistent):
    '''
        Clase que corresponde al mensaje en el cual se carga
        el contenido del mensaje, el que va a recibir el mensaje
        y el que lo envia
    '''
    def __init__(self, emisor, contenido, receptor):
        ''' inicalizador de la clase '''
        self.contenido = contenido
        self.emisor = emisor
        self.receptor = receptor

    def __str__(self):
        ''' toString del mensaje '''
        return "De: " + self.emisor + " A: " + self.receptor\
        + " Mensaje: " + self.contenido