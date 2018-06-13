## **Requisitos**
- Tener instalado **python3**
- Tener instalado el modulo **ZODB** (Para instalar el modulo debe instalarse primero **pip3**)
- El puerto **6030** no debe estar ocupado

## **Instalación**
- **Python3:** (Linux) sudo apt-get install python3
- **pip3:** (Linux) sudo apt-get install python3-pip
- **Modulo ZODB:** (Linux) pip3 install ZODB

## **Uso**
- Para iniciar la aplicación debe ejecutarse el script **Aplicacion.py** en la terminal de la siguiente forma
- => $ python3 Aplicacion.py

## **Observaciones**
- Para iniciar la aplicación con la vista tipo consola, se debe importar en el script **Controlador.py** el archivo **Vista.py**
- Para iniciar la aplicación con la vista programada en Tkinter, se debe importar en el script **Controlador.py** el archivo **VistaTk.py**

> Al iniciar la aplicación, el servidor se podrá a la escucha de conexiones entrantes en el puerto 6030, tambien creará o abrirá la base de datos llamada SMIOnlineDATA.fs ubicada en el directorio superior
