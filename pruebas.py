import sys
import subprocess
import pickle
import ipremoto

s = "s"
db = "db"
lxdbr = "lxdbr0"
ip_db = "134.3.0.2"

try:
	b = sys.argv[1]
	ipremoto.guess_ip(b)
except IndexError:
	subprocess.run(["lxc", "config", "device", "override", "remoto"+db+":"+db, "eth0", "ipv4.address="+ip_db+str(0)])
	subprocess.run(["lxc", "restart", "remoto"+db+":"+db])

