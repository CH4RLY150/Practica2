import sys
import subprocess
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def delete(orden, numero):
	try:
		for j in range(int(numero)):
			if numero == "1":
				nombre = orden
			else:
				nombre = orden + str(j)
			subprocess.run(["lxc", "delete", nombre])
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden en delete.py")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
