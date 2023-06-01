import sys
import subprocess
import pickle
import ipremoto

s = "s"

try:
	b = sys.argv[1]
	ipremoto.guess_ip(b)
except IndexError:
	with open("numero.txt", "rb") as files:
		numero = pickle.load(files)
	for i in range(int(numero)):
		nombre = s + str(i)
		subprocess.run(["lxc", "file", "push", "/home/c.mbarros/Práctica_2/app/md-seed-config.js", nombre+"/app/md-seed-config.js"])
		subprocess.run(["lxc", "file", "push", "/home/c.mbarros/Práctica_2/app/rest_server.js", nombre+"/app/rest_server.js"])

