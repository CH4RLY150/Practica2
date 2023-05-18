import sys
import subprocess
import logging
import pickle

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
	db = sys.argv[1]
	parametros = sys.argv[2]
	#configuración del db
	for i in range(int(parametros)):
		nombre = db + str(i)
		subprocess.run(["lxc", "exec", nombre, "--", "apt", "update"])
		subprocess.run(["lxc", "exec", nombre, "--", "apt","install", "-y", "mongodb"])
		subprocess.run(["lxc", "file", "push", "/home/c.mbarros/Práctica_2/mongodb/mongodb.conf", nombre+"/etc/mongodb.conf"])
		subprocess.run(["lxc", "restart", nombre])
	
except IndexError:
	logger.error("IndexError, no se ha introducido ninguna orden")
	#raise
except KeyboardInterrupt:
	logger.error("Terminado")
