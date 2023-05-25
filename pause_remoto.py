import sys
import subprocess

def pause_remoto(db, parametros):
	for i in range(int(parametros)):
		if parametros == "1":
			nombre = db
		else:
			nombre = db + str(i)
		subprocess.run(["lxc", "stop", "remoto"+db+":"+nombre])
