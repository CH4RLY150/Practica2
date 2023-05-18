import sys
import subprocess
import logging

lxdbr = "lxdbr"
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
	orden = sys.argv[1] 
	ip0 = sys.argv[2]
	ip1 = sys.argv[3]
	for i in range(int(orden)):
		nombre = lxdbr + str(i)
		ip = ip0 + str(i) + ip1
		# creación de los bridges
		if i == 0:
			subprocess.run(["lxc", "network", "set", nombre, "ipv4.nat", "true"])
			subprocess.run(["lxc", "network", "set", nombre, "ipv4.address", ip])
			subprocess.run(["lxc", "network", "set", nombre, "ipv6.nat", "false"])
			subprocess.run(["lxc", "network", "set", nombre, "ipv6.address", "none"])
		else:
			subprocess.run(["lxc", "network", "create", nombre])
			subprocess.run(["lxc", "network", "set", nombre, "ipv4.nat", "true"])
			subprocess.run(["lxc", "network", "set", nombre, "ipv4.address", ip])
			subprocess.run(["lxc", "network", "set", nombre, "ipv6.nat", "false"])
			subprocess.run(["lxc", "network", "set", nombre, "ipv6.address", "none"])	
except IndexError:
	logger.error("IndexError, no se ha introducido ninguna orden")
	#raise
except KeyboardInterrupt:
	logger.error("Terminado")
