import sys
import subprocess
import logging
import pickle

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
#Función que instala y configura la base de datos:
#Parámetros:
#	db: nombe del contenedor

def configure(db):
	try:
		#configuración del db
		subprocess.run(["lxc", "exec", db, "--", "apt", "update"])
		subprocess.run(["lxc", "exec", db, "--", "apt","install", "-y", "mongodb"])
		subprocess.run(["lxc", "file", "push", "mongodb.conf", db+"/etc/mongodb.conf"])
		subprocess.run(["lxc", "restart", db])
	
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
