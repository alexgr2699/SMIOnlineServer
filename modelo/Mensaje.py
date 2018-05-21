from persistent import Persistent

class Mensaje(Persistent):
    '''
        Clase que corresponderia al objeto Mensaje, el cual es utilizada
        por el usuario al querer enviar un mensaje, se instancia un objeto de}
        este tipo, se carga, se empaqueta y se envia al servidor segun
        corresponda
    '''
    def __init__(self, emisor, contenido, receptor):
        ''' '''
        self.contenido = contenido
        self.emisor = emisor
        self.receptor = receptor

    def __str__(self):
        ''' '''
        return "De: " + self.emisor + " A: " + self.receptor\
        + " Mensaje: " + self.contenido