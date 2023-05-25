import sys
import subprocess


def delete_remoto(db, parametros):
	for i in range(int(parametros)):
		if parametros == "1":
			nombre = db
		else:
			nombre = db + str(i)
		subprocess.run(["lxc", "delete", "remoto"+db+":"+nombre])


