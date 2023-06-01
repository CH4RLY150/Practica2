import sys
import time
import subprocess
import pickle
import ipremoto

# configuramos el lxd
	# sudo usermod -a -G lxd $USER
	# newgrp lxd
subprocess.run(["lxd", "init", "--auto"])

#snap services lxd

port = "8443"
lb = sys.argv[1]
mypass = sys.argv[2]
# conectamos los servidores con una DDBB remota
IP_B = ipremoto.guess_ip(lb)
subprocess.run(["lxc", "config", "set", "core.https_address", IP_B+":"+port]) 
subprocess.run(["lxc", "config", "set", "core.trust_password", mypass]) 
