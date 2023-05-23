import sys
import subprocess
import logging
import pickle
import time

nom_imagen = "nuevaImagen"

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def crear(orden, imagen, parametros):
	try:
		print("creando " + parametros + " " + orden)
		if parametros == "1":
			subprocess.run(["lxc", "init", imagen, orden])
		elif orden == "s":
			nombre = orden + str(0)
			subprocess.run(["lxc", "init", imagen, nombre])
			subprocess.run(["lxc", "start", nombre])		
			time.sleep(5)
			subprocess.run(["lxc", "file", "push", "install.sh", nombre+"/root/install.sh"])
			subprocess.run(["lxc", "exec", nombre, "--", "chmod", "+x", "install.sh"])
			subprocess.run(["lxc", "file", "push", "-r", "app", nombre+"/root"])
			subprocess.run(["lxc", "exec", nombre, "--", "./install.sh"])
			subprocess.run(["lxc", "restart", nombre])
			subprocess.run(["lxc", "stop", nombre])
			subprocess.run(["lxc", "publish", nombre, "--alias", nom_imagen])
			with open("nom_imagen.txt", "wb") as fich:
				pickle.dump(nom_imagen, fich)
		else:
			for i in range(int(parametros)):
				nombre = orden + str(i)
				subprocess.run(["lxc", "init", imagen, nombre])

	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
