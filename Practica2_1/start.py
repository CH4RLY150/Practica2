import sys
import subprocess
import logging
import time

s = "s"
lb = "lb"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def start(orden,numero):
	try:
		for j in range(int(numero)):
			if numero == "1":
				nombre = orden
			else:
				nombre = orden + str(j)
			subprocess.run(["lxc", "start", nombre])
			if orden == s:
				comando = "lxc exec " + nombre + " bash"
				subprocess.Popen(["xterm", "-fa", "monaco", "-fs", "13", "-bg", "pink", "-fg", "black", "-e", comando])
				subprocess.Popen(["lxc", "exec", nombre, "--", "forever", "start", "app/rest_server.js"])
			elif orden == lb:
				subprocess.run(["lxc", "exec", lb, "--", "start", "service", "haproxy"])
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden en start.py")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
