import sys
import subprocess
import logging

db = "db"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def lista(orden, numero):
	try:
		for j in range(int(numero)):
			if numero == "1":
				nombre = orden
			else:
				nombre = orden + str(j)
			subprocess.run(["lxc", "start", nombre])
			subprocess.run(["lxc", "exec", nombre, "ipaddr"])
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden en list.py")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
