import sys
import subprocess
import logging
import pickle
import time

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def configureremoto(db, parametros, IP_B, port, ip_, lxdbr, IP_A, password, s, ip_db, imagen):
	try:
		#Permitir el acceso remoto a las operaciones de LXD en lA + Acreditarse en el sistema remoto. Esto permite al equipo lA conectarse de manera remota al servicio LXD que se ejecuta en el equipo lB
		subprocess.run(["lxc", "config", "set", "core.https_address", ":"+port])
		#subprocess.run(["lxc", "remote", "add", "remoto"+db, IP_B+":"+port])
		subprocess.run(["lxc", "remote", "add", "remoto"+db, IP_B, "--password", password, "--accept-certificate"])
		#configuración de red y bridges en máquina remota lB
		subprocess.run(["lxc", "network", "set", "remoto"+db+":"+lxdbr, "ipv4.address", ip_])
		subprocess.run(["lxc", "network", "set", "remoto"+db+":"+lxdbr, "ipv4.nat", "true" ])
		for i in range(int(parametros)):
			if parametros == "1":
				nombre = db
			else:
				nombre = db + str(i)
			subprocess.run(["lxc", "stop", nombre])
			subprocess.run(["lxc", "init", imagen, "remoto"+db+":"+db])
			#subprocess.run(["lxc", "network", "attach", "remoto"+db+":"+lxdbr, db, "eth0"])
			subprocess.run(["lxc", "config", "device", "override", "remoto"+db+":"+db, "eth0", "ipv4.address="+ip_db+str(i)])
			subprocess.run(["lxc", "start", "remoto"+db+":"+db])
			time.sleep(5)
			subprocess.run(["lxc", "exec", "remoto"+db+":"+db, "--", "apt", "update"])
			subprocess.run(["lxc", "exec", "remoto"+db+":"+db, "--", "apt", "install", "-y", "mongodb"])
			subprocess.run(["lxc", "file", "push", "mongodb/mongodb.conf", "remoto"+db+":"+nombre+"/etc/mongodb.conf"])
			subprocess.run(["lxc", "restart", "remoto"+db+":"+nombre])
			subprocess.run(["lxc", "config", "device", "add", "remoto"+db+":"+db, "miproxy", "proxy", "listen=tcp:"+IP_B+":27017", "connect=tcp:"+ip_db+str(i)+":27017"])
		
		# actualizamos la ip de la db a la IP de la nueva db remota (que es la IP-B)
		# para ello debemos cambiar los documentos de la app instalada en cada servidor 
		lines = list()
		with open("app/md-seed-config.js", "r+") as fichero:
			lines = fichero.readlines()
			lines[3-1]="const mongoURL = process.env.MONGO_URL || 'mongodb://"+IP_B+":27017/bio_bbdd';\n"
		fichero.close()
		with open("app/md-seed-config.js", "w") as files:
			files.writelines(lines)
		files.close()
		with open("app/rest_server.js", "r+") as fichero:
			lines = fichero.readlines()
			lines[12-1]="    await mongoose.connect('mongodb://"+IP_B+"/bio_bbdd',{ useNewUrlParser: true, useUnifiedTopology: true })\n"
		with open("app/rest_server.js", "w") as files:
			files.writelines(lines)
		files.close()

		with open("numero.txt", "rb") as files:
			numero = pickle.load(files)
		for i in range(int(numero)):
			nombre = s + str(i)
			subprocess.run(["lxc", "start", nombre])
			subprocess.run(["lxc", "file", "push", "app/md-seed-config.js", nombre+"/root/app/md-seed-config.js"])
			subprocess.run(["lxc", "file", "push", "app/rest_server.js", nombre+"/root/app/rest_server.js"])
			if i > 0:
				subprocess.run(["lxc", "stop", nombre])
		
		subprocess.run(["lxc", "exec", s+str(0), "--", "chmod", "+x", "install.sh"])
		subprocess.run(["lxc", "exec", s+str(0), "--", "./install.sh"])
		subprocess.run(["lxc", "stop", s+str(0)])
	
	except IndexError:
		logger.error("IndexError, no se ha introducido ninguna orden")
		#raise
	except KeyboardInterrupt:
		logger.error("Terminado")
