import sys
import subprocess
import logging
import pickle
import time
import crear_servidores

nom_imagen = "nuevaImagen"

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def crear(orden, imagen, parametros):
	try:
		print("creando " + parametros + " " + orden)
		if parametros == "1":
			subprocess.run(["lxc", "init", imagen, orden])
		elif orden == "s":
			crear_servidores.crear_servidores(orden, imagen, parametros, nom_imagen)
		else:
			for i in range(int(parametros)):
				nombre = orden + str(i)
				subprocess.run(["lxc", "init", imagen, nombre])

	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
